import csv
import os

from connection import connection

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


def create_query(table_name, schema_dict):
    '''
    see datatypes documentation here:
    https://www.postgresql.org/docs/11/datatype.html
    '''
    columns = db_schema[table_name]
    columns_str = ''
    for column, value in columns.items():
        columns_str += f'"{column}" {value}, '
    columns_str = columns_str[:-2]
    return f'''CREATE TABLE IF NOT EXISTS goodbooks_{table_name} (
    {columns_str})'''


if __name__ == "__main__":

    engine = connection()
    path = 'goodbooks-10k/'

    for file in os.listdir(path):
        if file.endswith(".csv"):
            table = file.split(".")[0]
            print(f'CREATING TABLE {table}')
            create = create_query(table, db_schema)

            print(f'INSERTING ROWS TO {table}')
            with open(path + file) as csvfile:
                rows = csv.reader(csvfile, delimiter=',')
                for i, row in enumerate(rows):
                    # NEED TO FIGURE OUT INSERT STATEMENT WITHIN SQLALCHEMY
                    if i >= 5:
                        break
