import xml.etree.ElementTree as ET
import os

from bs4 import BeautifulSoup
import pandas as pd

from connection import connection


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


if __name__ == "__main__":
    path = 'goodbooks-10k/books_xml/books_xml/books_xml/'
    books = os.listdir(path)

    data = {}
    for i, book in enumerate(books):
        if i % 1000 == 0:
            print(f'Parsing book {i}')
        row = book_parser(path + book)
        data[book.split('.')[0]] = row

    df = pd.DataFrame.from_dict(data=data, orient='index')
    engine = connection()
    df.to_sql(
        'goodbooks_books_xml',
        con=engine,
        if_exists='replace',
        index=False
    )
