from datetime import datetime
from json import loads
from pprint import pprint

from decouple import config
from requests import get

from gb_search import GBWrapper
# IMPORT CONNECTION

class NYT:

    def __init__(self):
        self.NYT_KEY = config('NYT_KEY')

    def get_lists(self):
        request_url = f'https://api.nytimes.com/svc/books/v3/lists/names.json?'\
            f'api-key={self.NYT_KEY}'
        request = get(request_url)
        return loads(request.text)

    def get_books(self, list_type):
        request_url = f'https://api.nytimes.com/svc/books/v3/lists/current/'\
            f'{list_type}.json?api-key={self.NYT_KEY}'
        request = get(request_url)
        return loads(request.text)
    
    def get_results(self, list_type):
        response = self.get_books(list_type)

        return {
            'rank': response['results']['books'][0]['rank'],
            'isbn': response['results']['books'][0]['primary_isbn13']
        }

    def gb_query(self, isbn):
        gb = GBWrapper(method='isbn')
        # request_url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:'\
        #     f'{isbn}'
        # request = get(request_url)
        # return request.json()
        return gb.search(str(isbn))

    def gb_insert(self, response):
        return

    def get(self, book_list):
        # GET CURRENT RESULTS FROM DB
        return

if __name__ == "__main__":
    nyt = NYT()
    # pprint(nyt.get_books('combined-print-and-e-book-fiction')[0])
    results = nyt.get_results('combined-print-and-e-book-nonfiction')
    pprint(nyt.gb_query('9781984801258'))