from datetime import datetime
from json import loads

from decouple import config
from requests import get

from connection import Connection
from gb_search import GBWrapper
from populate import execute_queries, get_value
# IMPORT CONNECTION

class NYT:

    def __init__(self):
        self.NYT_KEY = config('NYT_KEY')
        self.gb = GBWrapper(method='isbn')
        conn = Connection()
        self.connection = conn.connection

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
    
    def get_rank(self, list_type):
        response = self.get_books(list_type)

        return {
            'rank': response['results']['books'][0]['rank'],
            'isbn': response['results']['books'][0]['primary_isbn13']
        }

    def gb_query(self, isbn):
        gb_response = self.gb.search(str(isbn))
        gb_values = get_value(gb_response['items'][0])
        print(gb_values)
        execute_queries(gb_values, self.connection)
        return

    def get(self, book_list):
        # GET CURRENT RESULTS FROM DB
        return

if __name__ == "__main__":
    nyt = NYT()
    # fiction = nyt.get_rank('combined-print-and-e-book-fiction')
    # nonfiction = nyt.get_rank('combined-print-and-e-book-nonfiction')
    query = nyt.gb_query('9781524763138')
    print('success')