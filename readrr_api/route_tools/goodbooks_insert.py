import csv
import os
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from psycopg2 import sql

from connection import Connection

db_schema = {
    'book_tags': {
        'goodreads_book_id': 'integer',
        'tag_id': 'integer',
        'count': 'integer'
    },
    'books': {
        'book_id': 'integer',
        'goodreads_book_id': 'integer',
        'best_book_id': 'integer',
        'work_id': 'integer',
        'books_count': 'integer',
        'isbn': 'text',
        'isbn13': 'text',
        'authors': 'text',
        'original_publication_year': 'text',
        'original_title': 'text',
        'title': 'text',
        'language_code': 'text',
        'average_rating': 'numeric(3)',
        'ratings_count': 'integer',
        'work_ratings_count': 'integer',
        'work_text_reviews_count': 'integer',
        'ratings_1': 'integer',
        'ratings_2': 'integer',
        'ratings_3': 'integer',
        'ratings_4': 'integer',
        'ratings_5': 'integer',
        'image_url': 'text',
        'small_image_url': 'text'
    },
    'ratings': {
        'user_id': 'integer',
        'book_id': 'integer',
        'rating': 'integer'
    },
    'tags': {
        'tag_id': 'integer',
        'tag_name': 'text'
    },
    'to_read': {
        'user_id': 'integer',
        'book_id': 'integer'
    }
}


def book_parser(path=None):
    tree = ET.parse(path)
    root = tree.getroot()

    ignore = {
        'reviews_widget', 'popular_shelves', 'book_links', 'buy_links',
        'series_works', 'similar_books'
        }

    row = {}
    for element in root.find('book'):
        if element.tag in ignore:
            continue
        if element.tag == 'description' and element.text is not None:
            soup = BeautifulSoup(element.text, 'html.parser')
            row[element.tag] = soup.text
            continue
        row[element.tag] = element.text
        if len(list(element.iter())) > 1:
            for child in element.iter():
                row[f'{element.tag}_{child.tag}'] = child.text
    return row


def xml_insert():
    path = 'goodbooks-10k/books_xml/books_xml/books_xml/'
    books = os.listdir(path)

    data = {}
    for i, book in enumerate(books):
        row = book_parser(path + book)
        data[book.split('.')[0]] = row
    return data


def create_query(table_name, schema_dict):
    '''
    see datatypes documentation here:
    https://www.postgresql.org/docs/11/datatype.html
    '''
    columns = db_schema[table_name]
    return (
        f"goodbooks_{table_name}",
        [f'{column} {value}' for column, value in columns.items()]
        )


def goodbooks_insert(conn):
    cursor = conn.cursor()
    path = 'goodbooks-10k/'
    for file in os.listdir(path):
        if file.endswith(".csv"):
            table = file.split(".")[0]
            columns = [
                f'{column} {value}' for column, value in db_schema[table]
                .items()
                ]
            command = (
                f'CREATE TABLE IF NOT EXISTS goodbooks_{table} ('
                f'{",".join(columns)});'
            )
            cursor.execute(command)

            with open(path + file, 'r') as f:
                next(f)
                cursor.copy_from(f, f'goodbooks_{table}', sep=',')
                cursor.execute(command)

    cursor.close()
    conn.commit()

    return


if __name__ == "__main__":
    conn = Connection()
    conn = conn.connection
    goodbooks_insert(conn)
    conn.close()
