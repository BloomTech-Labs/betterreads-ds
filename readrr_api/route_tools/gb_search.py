# a simple wrapper for the google books search API
import requests
import logging
from urllib.parse import quote

logging.basicConfig(level=logging.DEBUG, format="%(message)s")
class GBWrapper:
    """
    Provides functions to search using all
    available simple methods
    """
    def __init__(self, method=''):
        """API instance constructor

        :reference: https://developers.google.com/books/docs/v1/using
        :param method: search method for api, defaults to no method
        """
        self.method = method

    def search(self, terms):
        """Gets json response for search terms"""
        numeric_methods = ['isbn', 'lccn', 'oclc', 'isbn13']

        if self.method not in numeric_methods:
            terms = quote(terms.lower())
        else:
            terms = terms.lower()
        
        if self.method != '':
            method = self.method + ":"
        else:
            method = self.method


        base_url = 'https://www.googleapis.com/books/v1/volumes?q='
        res = requests.get(base_url + method + terms)
        try:
            res.raise_for_status()

        except Exception as err:
            msg = "An exception occurred," \
                  "check search terms and try again?"
            print(msg)

        return res.json()
