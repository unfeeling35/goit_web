import configparser
import pathlib
import os

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from dotenv import load_dotenv
load_dotenv()

file_config = pathlib.Path(__file__).parent.parent.joinpath('conf/config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = os.getenv('USER')
password = os.getenv('PASSWORD')
domain = os.getenv('DOMAIN')
port = os.getenv('PORT')
database = os.getenv('DB_NAME')

URI = f'postgresql://{username}:{password}@{domain}:{port}/{database}'

engine = create_engine(URI, echo=True)
DBSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()


if __name__ == '__main__':
    print(URI)