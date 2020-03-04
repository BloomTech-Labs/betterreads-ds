"""Entry point for our twitoff flask app"""

from app import create_app

application = create_app()

if __name__ == '__main__':
    application.run(debug=True)
