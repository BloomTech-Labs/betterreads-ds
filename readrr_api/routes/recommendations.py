import os
import json

import requests
from flask import Flask, request, jsonify

# TODO: add pickled model for use within reccomendations route

@recomendations.route('/recommendations/<int:userid>',methods=['GET'])
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

    output = {'interest':'hardcoded_reccs',
              'recommendations':output_reccs}
    
    return jsonify(output)
