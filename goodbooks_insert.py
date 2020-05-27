import csv
import os
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

# from readrr_api.route_tools.connection import Connection

db_schema = {
    'book_tags': {
        'goodreads_book_id': 'integer PRIMARY KEY',
        'tag_id': 'integer',
        'count': 'integer'
    },
    'books': {
        'book_id': 'integer',
        'goodreads_book_id': 'integer',
        'best_book_id': 'integer',
        'work_id': 'integer',
        'books_count': 'integer',
        'isbn': 'bigint',
        'isbn13': 'numeric(13)',
        'authors': 'text',
        'original_publication_year': 'integer',
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
    columns_str = ''
    for column, value in columns.items():
        columns_str += f'\n{column} {value}, '
    columns_str = columns_str[:-2]
    return f"CREATE TABLE goodbooks_{table_name} ({columns_str});"


def goodbooks_insert():
    path = 'goodbooks-10k/'

    for file in os.listdir(path):
        if file.endswith(".csv"):
            table = file.split(".")[0]
            # print(f'CREATING TABLE {table}')
            # create = create_query(table, db_schema)
            # EXECUTE SQL COMMAND HERE

            with open(path + file) as csvfile:
                rows = csv.reader(csvfile, delimiter=',')
                header = next(rows)
                for row in rows:
                    cursor = connection.cursor()
                    query = sql.SQL(
                        "INSERT INTO table () "
                        "VALUES (%s, %s, %s, %s, %s);"
                    )
                    break

    return


if __name__ == "__main__":
    goodbooks_insert()

    # CONNECTION GOES HERE

    # XML INSERT
    # GOODBOOKS REPO MUST BE CLONED INTO MAIN REPO
    # GOODBOOKS INSERT