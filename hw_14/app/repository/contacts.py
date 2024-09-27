from datetime import date, timedelta, datetime

from sqlalchemy.orm import Session

from app.database.models import Contact
from app.schemas import ContactModel


async def get_contacts(db: Session):
    """
    The get_contacts function returns a list of contacts from the database.

    :param db: Session: Pass in the database session to the function
    :return: A list of contacts in the database
    """
    contacts = db.query(Contact).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    """
    The get_contact_by_id function returns a contact object from the database based on its id.

    :param contact_id: int: Identify the contact that is being requested
    :param db: Session: Get the database session
    :return: The contact object associated with the given id
    """
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_email(email: str, db: Session):
    """
    The get_contact_by_email function returns a contact object from the database based on the email address provided.

    :param email: str: Specify the email of the contact to be returned
    :param db: Session: Pass the database session to the function
    :return: The contact with the given email
    """
    contact = db.query(Contact).filter_by(email=email).first()
    return contact


async def create(body: ContactModel, db: Session):
    """
    The create function creates a new contact in the database.

    :param body: ContactModel: Get the data from the request body
    :param db: Session: Access the database
    :return: The contact object that was created
    """
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    """
    The update function updates a contact in the database.

    :param contact_id: int: Get the contact by id
    :param body: ContactModel: Pass the contact data to update
    :param db: Session: Create a connection to the database
    :return: The updated contact
    """
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    """
    The remove function removes a contact from the database.

    :param contact_id: int: Specify the id of the contact to be removed
    :param db: Session: Pass the database session to the function
    :return: The contact that was removed, or none if no such contact exists
    """
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def find_contact_by_email(contact_email: str, db: Session):
    """
    The find_contact_by_email function takes in a contact_email and db as parameters.
    It then queries the database for all contacts with that email address, and returns them.

    :param contact_email: str: Specify the email of the contact that we want to find
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    """
    contacts = db.query(Contact).filter_by(last_name=contact_email).all()
    return contacts


async def find_contact_by_firstname(contact_firstname: str, db: Session):
    """
    The find_contact_by_firstname function takes in a contact_firstname and db as parameters.
    It then queries the database for all contacts with that first name, and returns them.

    :param contact_firstname: str: Pass in the first name of a contact to search for
    :param db: Session: Pass in a database session object
    :return: A list of contacts with the given first name
    """
    contacts = db.query(Contact).filter_by(first_name=contact_firstname).all()
    return contacts


async def find_contact_by_lastname(contact_lastname: str, db: Session):
    """
    The find_contact_by_lastname function takes in a contact_lastname and db as parameters.
    It then queries the database for all contacts with that last name, and returns them.

    :param contact_lastname: str: Pass in the last name of a contact
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    """
    contacts = db.query(Contact).filter_by(last_name=contact_lastname).all()
    return contacts


async def find_contacts_birthday(db: Session):
    """
    The find_contacts_birthday function returns a list of contacts whose birthday is within the next week.

    :param db: Session: Pass the database session into the function
    :return: A list of contacts with a birthday in the next 7 days
    """
    today = date.today()
    end_date = today + timedelta(days=7)
    birthday_list = []
    contacts = db.query(Contact).all()
    for contact in contacts:
        current_year_birthdays: datetime = contact.birthday.replace(year=today.year)
        if today <= current_year_birthdays.date() <= end_date:
            birthday_list.append(contact)
    return birthday_list