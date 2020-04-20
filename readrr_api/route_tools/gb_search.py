# a simple wrapper for the google books search API
import requests
from urllib.parse import quote

class GBWrapper:
    """
    Provides functions to search using all
    available simple methods
    """
    def __init__(self, method=''):
        """API instance constructor

        :reference: https://developers.google.com/books/docs/v1/using
        :param method: search method for api, default: 'intitle'
        """
        self.method = method

    def search(self, terms):
        """Gets json response for search terms"""
        numeric_methods = ['isbn', 'lccn', 'oclc']

        if self.method not in numeric_methods:
            terms = quote(terms.lower())
        else:
            terms = terms.lower()



        base_url = 'https://www.googleapis.com/books/v1/volumes?q='
        res = requests.get(base_url + terms + self.method)
        try:
            res.raise_for_status()

        except Exception as err:
            msg = "An exception occurred," \
                  "check search terms and try again?"
            print(msg)

        return res.json()
