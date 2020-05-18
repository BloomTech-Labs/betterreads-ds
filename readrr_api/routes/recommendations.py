import logging
import threading

from flask import request, jsonify, Blueprint
from .. route_tools.recommender import Book
# may need cross origin resource sharing (CORS)

FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
# logging.disable(logging.CRITICAL)

recommendations = Blueprint("recommendations", __name__)


def fetch_recs(output_list, target_book):
    """
    Gets recommendations from the Book class
    and appends the list that will be part of
    the response body.

    output_list: list of books to send in response
    target_book: book in user bookshelf
    """
    book = Book(target_book)
    recs = book.recommendations()
    output_list.append(recs)


@recommendations.route('/recommendations', methods=['POST'])
def recommend():
    """
    Provide recommendations based on user bookshelf.
    """
    user_books = request.get_json()

    output = []
    thread_list = []

    for b in user_books:
        # start a thread for each book to get recs
        thread_obj = threading.Thread(target=fetch_recs,
                                      args=(output, b))

        thread_list.append(thread_obj)
        thread_obj.start()

    # wait for threads to end
    for thread in thread_list:
        thread.join()

    return jsonify(output)
