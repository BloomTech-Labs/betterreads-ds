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
