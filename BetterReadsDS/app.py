# from decouple import config #<-- not sure what this does yet
from flask import Flask, render_template, request
import

def create_app():
    app = Flask(__name__)

    # Whenever we output a list of books the json format of the
    # list should be the same. Lets call this format
    # OUT_LIST format for now. This format is what the Web team is
    # currently using to render book list results.


    @app.route('/')
    # some details about the api and some references
    # to api documentation
    def root():
        return render_template('base.html',page_name='home')

    @app.route('/search')
    # the input is going to be a string
    # output will be a list of books from the google api
    # formatting of the output should be in OUT_LIST format
    def search():
        return render_template('base.html',page_name='search')


    @app.route('/subject_list')
    # input will be subject heading (this should be a valid value)
    # We need to give BE/FE a list of valid subject headings
    # output is going to be a list of books in the OUT_LIST format
    def subjects():
        return render_template('base.html',page_name='subjects')


    @app.route('/recommendations')
    # input is ???
    # The input might include parameters that aid in the model
    # selection process. We may have different models depending on
    # the different types of recommendations we need to provide.
    # output is a list of books.
    def recommendations():
        return render_template('base.html',page_name='recommendations')


    return app
