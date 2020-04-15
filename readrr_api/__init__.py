import os

from flask import Flask
from readerr_api.routes.primary import primary_routes


def create_app():
    app = Flask(__name__)

    app.register_blueprint(primary_routes)

    return app
