import os

from flask import Flask
from .routes.nyt import nyt
from .routes.recommendations import recommendations


def create_app():
    a = Flask(__name__)

    a.register_blueprint(recommendations)
    a.register_blueprint(nyt)

    return a
