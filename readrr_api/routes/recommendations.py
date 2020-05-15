import os
import json
import random
import pickle
import logging

import requests
from flask import Flask, request, jsonify, Blueprint
from sklearn.neighbors import NearestNeighbors
from .. route_tools.gb_funcs import retrieve_details
from .. route_tools.recommender import Book, tokenize
# may need cross origin resource sharing (CORS)

FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
# logging.disable(logging.CRITICAL)

recommendations = Blueprint("recommendations", __name__)

file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'notebooks')
# path to Book class dependencies
# r_tools_path = os.path.join(os.path.dirname(__file__), '..', 'route_tools')
#
# # load model dependencies
# with open(os.path.join(r_tools_path, 'nlp.pkl'), 'rb') as vocab:
#     nlp = pickle.load(vocab)

# STOP_WORDS = ["new", "book", "author", "story", "life", "work", "best",
#               "edition", "readers", "include", "provide", "information"]
# STOP_WORDS = nlp.Defaults.stop_words.union(STOP_WORDS)


@recommendations.route('/recommendations', methods=['POST'])
def recommend():
    """
    Provide recommendations based on user bookshelf.
    """
    user_books = request.get_json()

    output = []

    for b in user_books:
        book = Book(b)
        recs = book.recommendations()
        output.append(recs)

    return jsonify(output)
