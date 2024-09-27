import hashlib

from fastapi import Depends, HTTPException, status, APIRouter, Security, BackgroundTasks, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.repository import users as repository_users
from app.schemas import UserModel, UserResponse, TokenModel, RequestEmail
from app.services.auth import auth_service
from app.services.mail import send_email

router = APIRouter(prefix="/auth", tags=['auth'])
security = HTTPBearer()


def get_gravatar_url(email: str, size: int = 200) -> str:
    """
    Generate a Gravatar URL for the given email address.

    :param email: str - The email address of the user.
    :param size: int - The size of the Gravatar image. Default is 200.
    :return: str - The Gravatar URL.
    """
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    """
    Register a new user.

    :param body: UserModel - The user model containing user details.
    :param background_tasks: BackgroundTasks - The background tasks for sending confirmation email.
    :param request: Request - The request object to get the base URL.
    :param db: Session - The database session dependency.
    :return: UserResponse - The response model for the created user.
    :raises HTTPException: If the user already exists.
    """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    avatar_url = get_gravatar_url(body.email)
    new_user_data = body.dict()
    new_user_data['avatar'] = avatar_url
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, request.base_url)
    return new_user


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user and return JWT tokens.

    :param body: OAuth2PasswordRequestForm - The form containing username and password.
    :param db: Session - The database session dependency.
    :return: TokenModel - The response model containing the access and refresh tokens.
    :raises HTTPException: If the email or password is invalid.
    """
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
    Refresh the JWT tokens using the refresh token.

    :param credentials: HTTPAuthorizationCredentials - The security credentials containing the refresh token.
    :param db: Session - The database session dependency.
    :return: TokenModel - The response model containing the new access and refresh tokens.
    :raises HTTPException: If the refresh token is invalid.
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    Confirm the user's email address using the provided token.

    :param token: str - The token for email confirmation.
    :param db: Session - The database session dependency.
    :return: dict - A message indicating the result of the confirmation process.
    :raises HTTPException: If the verification fails.
    """
    email = auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed_email:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    """
    Request a confirmation email to be sent to the user.

    :param body: RequestEmail - The request body containing the email address.
    :param background_tasks: BackgroundTasks - The background tasks for sending the email.
    :param request: Request - The request object to get the base URL.
    :param db: Session - The database session dependency.
    :return: dict - A message indicating the email has been sent.
    """
    user = await repository_users.get_user_by_email(body.email, db)
    if user:
        if user.confirmed_email:
            return {"message": "Your email is already confirmed"}
        background_tasks.add_task(send_email, user.email, user.username, request.base_url)
    return {"message": "Check your email for confirmation."}