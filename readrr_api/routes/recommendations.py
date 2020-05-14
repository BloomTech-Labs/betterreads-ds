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

    # to add some randomness
    random.shuffle(favorites)

    # if there are no favorites, recommend based on first book
    if len(favorites) >= 1:
        for i in range(len(favorites)):
            try:
                target_book = favorites[i]
                neighbors = get_recommendations(target_book)
                acquired = True
                break
            except ValueError:
                continue

    else:
        neighbors, acquired, target_book = shelf_iterate(user_books)

    # if book is not in known titles, recommend an alternative
    if not acquired:
        neighbors, acquired, target_book = shelf_iterate(user_books)
        if neighbors is None:
            target_book = "#GIRLBOSS"
            neighbors = get_recommendations(target_book)
    else:
        neighbors = get_recommendations(target_book)

    output_recs = []
    logging.info("Neighbors:" + str(neighbors))

    # skip first book
    for book in neighbors[1:]:
        book_data = api.search(book)
        target_data = book_data['items'][0]
        target_json = retrieve_details(target_data)
        output_recs.append(target_json)

    # change 'id' to 'googleId' at every list index
    for item in output_recs:
        item['googleId'] = item.pop('id')

    output = {'based_on': target_book,
              'recommendations': output_recs}

    return jsonify(output)
