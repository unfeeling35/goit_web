from mongoengine import *

# uri = f"mongodb+srv://{user}:{password}@cluster0.ybyottf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# connection = connect(host=uri,  tlsCAFile=certifi.where(), ssl=True)


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()