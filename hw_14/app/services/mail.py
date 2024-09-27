from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr
from dotenv import load_dotenv
from pathlib import Path
import asyncio
import os

from app.services.auth import auth_service

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_USERNAME'),
    MAIL_PORT=os.getenv('MAIL_PORT'),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_email(email: EmailStr, username: str, host: str):
    """
    The send_email function sends an email to the user with a link to confirm their email address.

    :param email: EmailStr: Specify the email address of the recipient
    :param username: str: Pass the username of the user to be registered
    :param host: str: Pass the hostname of the server to the template
    :return: A coroutine, which is an object that can be awaited
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="mail.html")
    except ConnectionErrors as err:
        print(err)


async def main():
    test_email = "test@example.com"
    test_username = "testuser"
    test_host = "http://localhost:8000"
    try:
        await send_email(test_email, test_username, test_host)

    except Exception as err:
        print(err)


if __name__ == "__main__":
    asyncio.run(main())