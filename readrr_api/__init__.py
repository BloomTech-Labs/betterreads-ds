import os

from flask import Flask
from readerr_api.routes.recommendations import recommendations


def create_app():
    app = Flask(__name__)

    app.register_blueprint(primary_routes)

    return app
