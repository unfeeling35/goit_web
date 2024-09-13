import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "great_quotes.settings")
django.setup()
from quotes.models import Author, Quote, Tag



load_dotenv()
user = os.getenv("USER")
password = os.getenv("PASS")
uri = f"mongodb+srv://{user}:{password}@cluster0.ybyottf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#connect(host=uri, tlsCAFile=certifi.where(), ssl=True)
# CONNECTION = connect(host=uri, tlsCAFile=certifi.where(), ssl=True)
client = MongoClient(uri, tlsCAFile=certifi.where(), ssl=True)

db = client['test']  # name of MongoDB database

collection = db['author']  # the name of MongoDB collection

cursor = collection.find()


for document in cursor:
    #print(document)
    Author.objects.get_or_create(
        fullname=document['fullname'],
        born_date=document['born_date'],
        born_location=document['born_location'],
        description=document['description']
    )
quotes = db.quote.find()

for quote in quotes:
    tags = []
    for tag in quote['tags']:
        print(tag)
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    print(quote)
    is_quote = bool(len(Quote.objects.filter(quote=quote['quote'])))
    print(is_quote)
    if not is_quote:
        author = db.author.find_one({'_id': quote['author']})
        if author is not None:
            a = Author.objects.get(fullname=author['fullname'])
            q = Quote.objects.create(
                quote=quote['quote'],
                author=a
            )

        else:
            print(f"Author {quote['author']} not found")
        for tag in tags:
            print(tags)
            q.tags.add(tag)
client.close()