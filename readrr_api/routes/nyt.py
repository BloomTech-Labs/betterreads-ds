from flask import Flask, jsonify, Blueprint

nyt = Blueprint('nyt', __name__)

@nyt.route('/nyt', methods=['GET'])
def nyt_recommendations():
    return