import logging
import threading
import os
import pickle
import random

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
with open(os.path.join(
          r_tools_path, "compressed_sim_matrix.pkl"), "rb") as csm:
    compsim = pickle.load(csm)

# open main lookup index
with open(os.path.join(
          r_tools_path, "master_hybrid_index.pkl"), "rb") as mhi:
    master_index = pickle.load(mhi)

# open vectorizer for search
with open(os.path.join(
          r_tools_path, "search_vectorizer.pkl"), "rb") as sv:
    vectorizer = pickle.load(sv)

# open nearest neighbor for title search
with open(os.path.join(
          r_tools_path, "search_neighbors.pkl"), "rb") as sn:
    search_nn = pickle.load(sn)

with open(os.path.join(
          r_tools_path, "book_search_index.pkl"), "rb") as bsi:
    book_search_index = pickle.load(bsi)


def fetch_recs(output_list, target_book, nn, tfidf, sim_matrix,
               sim_index, s_vectorizer, s_neighbors, bk_srch_idx):
    """
    Gets recommendations from the Book class
    and appends the list that will be part of
    the response body.

    output_list: list of books to send in response
    target_book: book in user bookshelf
    """
    book = Book(target_book)
    recs = book.recommendations(nn, tfidf, sim_matrix, sim_index,
                                s_vectorizer, s_neighbors, bk_srch_idx)
    output_list.append(recs)


@recommendations.route('/recommendations', methods=['POST'])
def recommend():
    """
    Provide recommendations based on one book in user bookshelf
    or a single book
    """
    user_books = request.get_json()

    favorites = []

    # try to select favorites
    for book in user_books:
        if book['favorite']:
            favorites.append(book)
    # if there are no favorites, just select any book
    if favorites == []:
        b = random.choice(user_books)
    else:
        b = random.choice(favorites)

    with open(os.path.join(r_tools_path, 'tfidf_model.pkl'),
              'rb') as tfidf:
        tfidf = pickle.load(tfidf)

    with open(os.path.join(r_tools_path, 'nn.pkl'),
              'rb') as nn:
        nn = pickle.load(nn)

    book = Book(b)
    recs = book.recommendations(nn, tfidf, compsim, master_index,
                                vectorizer, search_nn, book_search_index)

    return jsonify(recs)


@recommendations.route('/recommendations/bookshelf', methods=['POST'])
def recommend_all():
    """
    Provide recommendations based on entire user bookshelf.
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
                                      args=(output, b, nn, tfidf,
                                            compsim, master_index,
                                            vectorizer, search_nn,
                                            book_search_index))

        thread_list.append(thread_obj)
        thread_obj.start()

    # wait for threads to end
    for thread in thread_list:
        thread.join()

    return jsonify(output)
