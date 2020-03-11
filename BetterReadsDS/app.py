# Inbuild Modules
import os
import json

# Third Party Modules
import requests
from flask import Flask, render_template, request, jsonify
# from decouple import config #<-- not sure what this does yet

# Custom Modules
from google_books_hf import process_list

# Retreive Google API key from environment


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

    @app.route('/test',methods=['POST'])
    def test():
        print('test')
        test_val = request.get_json(force=True)
        print(test_val)
        return "3"

    @app.route('/search', methods=['GET','POST'])
    def search():
        # variables used throughout the function
        GOOGLE_KEY = os.environ['GOOGLE_KEY']
        relevant_details=['id','title','authors','publisher',
                  'publishedDate','description','industryIdentifiers',
                  'pageCount','categories','thumbnail','smallThumbnail',
                  'language','webReaderLink','textSnippet','isEbook']

        # Retreive the information from the POST request body

        # try:
        #     input_data = request.get_json()
        # except:
        #     print("that didn't work")
        # print(input_data)

        input_data = request.get_json(force=True)

        # Try to access keys from the post request
        try:
            if input_data['type'] == 'googleId':
                search_id = input_data['query']
                response = requests.get('https://www.googleapis.com/books/v1/volumes/'
                                        + search_id
                                        + '?key='
                                        + GOOGLE_KEY)
                # If invalid google id, then display/return an error message
                result = json.loads(response.text)
                output = process_list([result],relevant_details)
                return jsonify(output)

            elif input_data['type'] == 'search':
                search_term = input_data['query']
                response = requests.get('https://www.googleapis.com/books/v1/volumes?q='
                    + search_term
                    + '&key='
                    + GOOGLE_KEY)
                result = json.loads(response.text)
                output = process_list(result['items'],relevant_details)
                return jsonify(output)
            else:
                message = """ The value for the 'type' key was invalid.
                 Please change the value to 'googleId', or 'search' """
                return render_template('echo.html',page_name='error',
                                        echo=message)

        # If you can't access keys from the post request display error message
        except KeyError:
            message = """ The key wasn't in the request body"""
            return render_template('echo.html',page_name='error', echo=message)

        return render_template('echo.html',page_name='search')

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

if __name__=="__main__":
    print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
