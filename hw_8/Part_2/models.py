import certifi
from mongoengine import *
from dotenv import load_dotenv
import os
from mongoengine import connect

load_dotenv()
user = os.getenv("USER")
password = os.getenv("PASS")
uri = f"mongodb+srv://{user}:{password}@cluster0.ybyottf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
CONNECTION = connect(host=uri, tlsCAFile=certifi.where(), ssl=True)


class Contact(Document):
    name = StringField(required=True)
    email = StringField(required=True)
    is_email = BooleanField(default=False)