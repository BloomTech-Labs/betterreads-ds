import os
import json
import random
import pickle
import logging

import requests
from flask import Flask, request, jsonify, Blueprint
from sklearn.neighbors import NearestNeighbors
from ..route_tools.gb_funcs import retrieve_details
from ..route_tools.recommender import Book,
# may need cross origin resource sharing (CORS)

FORMAT = "%(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
# logging.disable(logging.CRITICAL)

recommendations = Blueprint("recommendations", __name__)

file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'notebooks')
# path to Book class dependencies
r_tools_path = os.path.join(os.path.dirname(__file__), 'route_tools')

# instantiate api from wrapper
api = GBWrapper()

# load model dependencies
with open(os.path.join(file_path, 'nlp.pkl'), 'rb') as vocab:
    nlp = vocab


@recommendations.route('/recommendations', methods=['POST'])
def recommend():
    """
    Provide recommendations based on user bookshelf.
    """
    user_books = request.get_json()

    for book in user_books:
        if book['favorite']:
            favorites.append(book['title'])


    return jsonify(output)
