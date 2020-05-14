import os
import csv
import time
import shelve
import requests
import logging
import threading
from urllib.parse import urljoin, quote

import psycopg2
from psycopg2 import sql

FORMAT = "%(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


def gb_url(search_term, index=None):
    """
    Creates a valid url for request

    search_term: the terms to search for via the specified parameter

    index: defaults to None, can be used to paginate results
    """
    base_url = "https://www.googleapis.com/books/v1/"
    volumes = "volumes?q="
    parameter = "inpublisher:"
    max_results = "&maxResults=40"

    if index:
        tail = (volumes +
                parameter +
                quote(search_term) +
                max_results +
                f"&startIndex={index}")
    else:
        tail = (volumes +
                parameter +
                quote(search_term) +
                max_results)

    url = urljoin(base_url, tail)

    return url


def get_value(book):
    """
    Compiles book data from json response into an iterable
    for use in SQL command

    book: one individual item in googleAPIresponse['items']
    """
    try:
        googleId = book['id']
    except KeyError:
        googleId = None

    try:
        title = book['volumeInfo']['title']
    except KeyError:
        title = None

    try:
        authors = book['volumeInfo']['authors']
        authors = str(set(authors))
    except KeyError:
        authors = None

    try:
        pub = book['volumeInfo']['publisher']
    except KeyError:
        pub = None

    try:
        publishedDate = book['volumeInfo']['publishedDate']
    except KeyError:
        publishedDate = None

    try:
        description = book['volumeInfo']['description']
    except KeyError:
        description = None

    try:
        isbn = book['volumeInfo']['industryIdentifiers'][0]['identifier']
    except KeyError:
        isbn = None

    try:
        pageCount = book['volumeInfo']['pageCount']
    except KeyError:
        pageCount = None

    try:
        categories = book['volumeInfo']['categories']
        categories = str(set(categories))
    except KeyError:
        categories = None

    try:
        thumbnail = book['volumeInfo']['imageLinks']['thumbnail']
    except KeyError:
        thumbnail = None

    try:
        smallThumbnail = book['volumeInfo']['imageLinks']['smallThumbnail']
    except KeyError:
        smallThumbnail = None

    try:
        lang = book['volumeInfo']['language']
    except KeyError:
        lang = None

    try:
        webReaderLink = book['accessInfo']['webReaderLink']
    except KeyError:
        webReaderLink = None

    try:
        textSnippet = book['searchInfo']['textSnippet']
    except KeyError:
        textSnippet = None

    try:
        isEbook = book['saleInfo']['isEbook']
    except KeyError:
        isEbook = None

    try:
        averageRating = book['volumeInfo']['averageRating']
    except KeyError:
        averageRating = None

    try:
        maturityRating = book['volumeInfo']['maturityRating']
    except KeyError:
        maturityRating = None

    try:
        ratingsCount = book['volumeInfo']['ratingsCount']
    except KeyError:
        ratingsCount = None

    try:
        subtitle = book['volumeInfo']['subtitle']
    except KeyError:
        subtitle = None

    value = [googleId, title, authors, pub, publishedDate,
             description, isbn, pageCount, categories, thumbnail,
             smallThumbnail, lang, webReaderLink, textSnippet,
             isEbook, averageRating, maturityRating, ratingsCount,
             subtitle]

    return value


def execute_queries(data, connection):
    """Creates SQL connection, execute query, close connection"""
    cursor = connection.cursor()
    query = sql.SQL(
        "INSERT INTO gb_data VALUES "
        "(%s, %s, %s, %s, %s, %s, %s, "
        "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    try:
        cursor.execute(query, data)

    except Exception as err:
        logging.error(f"Error: {err}")
        connection.rollback()
    else:
        connection.commit()
    cursor.close()

def request_and_execute(search_term, starting_index):
    """
    Creates a GET request to google books API, collects data, then uses
    this data to execute a SQL query with connection to database
    """
    # GET request
    url = gb_url(search_term, index=starting_index)
    response = requests.get(url)

    try:
        response.raise_for_status()
    except Exception as err:
        logging.error(err)

        return None

    data = response.json()

    if 'items' not in data.keys():
        logging.info(
            f"No items for {search_term} at index {starting_index}"
        )

        return None

    execute_queries(data)

    return True


def get_all_books(search_term, search_index):
    """Gets books data from index 0 of API request pages, starts
    necessary threads to collect other pages

    search_term: the term used in the url call to API

    search_index: the index on which the function begins search
    """
    initial_url = gb_url(search_term)
    response = requests.get(initial_url)

    # main connection
    DATABASE_URL = os.environ["DATABASE_URL"]

    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    try:
        response.raise_for_status()
    except Exception as err:
        logging.error(err)

        # return search_index to shelf and begin on this
        # index upon next pass
        return search_index

    data = response.json()

    if 'items' not in data.keys():
        logging.info(f"No items for {search_term}")

        return None

    # reduce unnecessary calls by using 'totalItems' to approximate
    total_items = (data['totalItems'] // 100) * 100

    execute_queries(data)

    threads = []

    for index in range(40, total_items, 40):
        thread_obj = threading.Thread(target=request_and_execute,
                                      args=(search_term, index))

        threads.append(thread_obj)
        thread_obj.start()

    # wait for all threads to finish
    for thread in threads:
        thread.join()

    return None


def run(term_csv):
    """
    Gets list of search terms from csv and run book retrieval process.
    Upon an http error, search index will be stored and process
    will pick back up from last index on next pass
    """
    shelf = shelve.open('index_shelf')

    # read in search data
    with open(term_csv) as search_data:
        reader = csv.reader(search_data)
        terms = [row for row in reader]

    try:
        start = shelf['start_position']
    except KeyError:
        shelf['start_position'] = 0
        start = shelf['start_position']

    for i in range(start, len(terms)):
        complete_process = get_all_books(terms[i][0], i)

        if complete_process is not None:
            shelf['start_position'] = i
            shelf.close()
            exit()

    shelf.close()


if __name__ == "__main__":
    run('significant_publishers.csv')
