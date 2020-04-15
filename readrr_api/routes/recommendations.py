import os
import json

import requests
from flask import Flask, request, jsonify
from readrr_tools.gb_funcs import retrieve_details
# may need cross origin resource sharing (CORS)

# TODO: add a way to communicate with google books api
# TODO: add pickled model for use within reccomendations route


@recomendations.route('/recommendations/<int:userid>', methods=['GET'])
def recommend():
    """
    Provide recommendations based on user bookshelf.

    userid - integer user id
    """

    # This could probably just get sent straight to us by web
    shelf_endpoint = 'https://api.readrr.app/api/'\
                     'datasciencetogetasecretand'\
                     'pineapplepizzaandbrocolli/'

    user_data_url = (shelf_endpoint + userid)
    user_books = requests.get(user_data_url)
    user_books = json.loads(user_books.text)

    # TODO: take one random book where "favorite" == True
    #       (or some other method), and use the book to
    #       provide recommendations. Include the book
    #       title in the response so that web and iOS
    #       can reflect this back to the user (transparency)

    # TODO: call google books API for data on recommendations
    #       use ISBN if possible

    # TODO: correct output and include book used for recommendation
    output = {'interest': 'hardcoded_reccs',
              'recommendations': output_reccs}

    return jsonify(output)
