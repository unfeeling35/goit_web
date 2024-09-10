from models import Quote, Author
import json
from connect import CONNECTION as connection


def load_quotes_to_database(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            author_name = item['author']
            author = Author.objects(fullname=author_name).first()
            print(author, type(author))
            if not author:
                author = Author(fullname=author_name)
                author.save()

            quote = Quote(author=author, quote=item['quote'], tags=item['tags'])
            quote.save()


def load_authors_to_database(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            document = Author(**item)
            document.save()


if __name__ == '__main__':
    load_authors_to_database('authors.json')
    load_quotes_to_database('quotes.json')
