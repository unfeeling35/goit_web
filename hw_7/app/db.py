from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
class Base(DeclarativeBase):
    pass

# Base = declarative_base()
pg_pass = os.getenv("POSTGRES_PASS")
pg_user = os.getenv("POSTGRES_USER")

DB_URL = f"postgresql://{pg_user}:{pg_pass}@localhost:5432/postgres"

engine = create_engine(DB_URL)

DBSession = sessionmaker(bind=engine)
session = DBSession()