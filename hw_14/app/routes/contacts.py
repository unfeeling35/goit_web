from typing import List
from fastapi import Depends, Query, Path, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import User
from app.repository import contacts as repository_contacts
from app.schemas import ContactResponse, ContactModel
from app.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts.

    :param db: Session: Pass the database connection to the function
    :param current_user: User: Get the current user from the token
    :return: A list of contacts
    """
    contacts = await repository_contacts.get_contacts(db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function is a GET request that returns the contact with the given ID.
    If no such contact exists, it raises an HTTP 404 error.

    :param contact_id: int: Specify the contact_id of the contact to be retrieved
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Check if the user is logged in
    :return: A contact object
    """
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
    It takes an email, first_name, last_name and phone number as input parameters.
    The function returns the newly created contact object.

    :param body: ContactModel: Get the data from the request body
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A ContactModel object
    """
    contact = await repository_contacts.get_contact_by_email(body.email, db)
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is existed!")
    contact = await repository_contacts.create(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
    The function takes an id and a body as input, and returns the updated contact.
    If no contact is found with that id, it raises an HTTPException.

    :param body: ContactModel: Specify the data that will be sent in the request body
    :param contact_id: int: Get the id of the contact to be updated
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the database
    :return: A ContactModel object, which is the same as what we use for creating contacts
    """
    contact = await repository_contacts.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The delete_contact function deletes a contact from the database.
    The function takes in an integer as a parameter, which is the ID of the contact to be deleted.

    :param contact_id: int: Specify the contact id to be deleted
    :param db: Session: Access the database
    :param current_user: User: Get the current user from the database
    :return: The deleted contact
    """
    contact = await repository_contacts.remove(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/birthdays/", response_model=List[ContactResponse])
async def find_contacts_birthday(db: Session = Depends(get_db),
                                 current_user: User = Depends(auth_service.get_current_user)):
    """
    The find_contacts_birthday function returns a list of contacts that have birthdays in the current month.

    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A list of contacts with upcoming birthdays
    """
    contacts = await repository_contacts.find_contacts_birthday(db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


@router.get("/find/{contact_firstname}", response_model=List[ContactResponse])
async def find_contact_by_firstname(contact_firstname: str, db: Session = Depends(get_db),
                                    current_user: User = Depends(auth_service.get_current_user)):
    """
    The find_contact_by_firstname function is used to find a contact by their first name.
    The function takes in the contact's first name as an argument and returns the contact object if found.

    :param contact_firstname: str: Get the firstname of the contact to be deleted
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the current user from the database
    :return: A contact object
    """
    contact = await repository_contacts.find_contact_by_firstname(contact_firstname, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/find/{contact_lastname}", response_model=List[ContactResponse])
async def find_contact_by_lastname(contact_lastname: str, db: Session = Depends(get_db),
                                   current_user: User = Depends(auth_service.get_current_user)):
    """
    The find_contact_by_lastname function is used to find a contact by their last name.
    The function takes in the contact's last name as an argument and returns the contact object if found.

    :param contact_lastname: str: Find the contact by lastname
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A contact object
    """
    contact = await repository_contacts.find_contact_by_lastname(contact_lastname, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact