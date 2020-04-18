import os

from flask import Flask
from .routes.recommendations import recommendations


def create_app():
    a = Flask(__name__)

    a.register_blueprint(recommendations)

    return a
