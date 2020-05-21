import logging
import threading
import os
import pickle

from flask import request, jsonify, Blueprint
from .. route_tools.recommender import Book, tokenize
# may need cross origin resource sharing (CORS)

FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
# logging.disable(logging.CRITICAL)

if tokenize:
    logging.info('"tokenize" loaded in ' + str(__name__))

recommendations = Blueprint("recommendations", __name__)

r_tools_path = os.path.join(os.path.dirname(__file__), '..', 'route_tools')

# open compressed hybrid matrix
with open("compressed_sim_matrix.plk", "rb") as csm:
    compsim = pickle.load(csm)

# open main lookup index
with open("master_hybrid_index.pkl", "rb") as mhi:
    master_index = pickle.load(mhi)

def fetch_recs(output_list, target_book, nn, tfidf):
    """
    Gets recommendations from the Book class
    and appends the list that will be part of
    the response body.

    output_list: list of books to send in response
    target_book: book in user bookshelf
    """
    book = Book(target_book)
    recs = book.recommendations(nn, tfidf)
    output_list.append(recs)


@recommendations.route('/recommendations', methods=['POST'])
def recommend():
    """
    Provide recommendations based on user bookshelf.
    """
    user_books = request.get_json()

    with open(os.path.join(r_tools_path, 'tfidf_model.pkl'),
              'rb') as tfidf:
        tfidf = pickle.load(tfidf)

    with open(os.path.join(r_tools_path, 'nn.pkl'),
              'rb') as nn:
        nn = pickle.load(nn)

    output = []
    thread_list = []

    for b in user_books:
        # start a thread for each book to get recs
        thread_obj = threading.Thread(target=fetch_recs,
                                      args=(output, b, nn, tfidf))

        thread_list.append(thread_obj)
        thread_obj.start()

    # wait for threads to end
    for thread in thread_list:
        thread.join()

    return jsonify(output)
