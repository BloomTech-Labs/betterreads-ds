"""Entry point for our twitoff flask app"""

from app import create_app

# This is a global variable
APP = create_app()
