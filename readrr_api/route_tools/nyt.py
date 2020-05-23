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
        results = []
        date = response['results']['bestsellers_date']
        for book in response['results']['books']:
            results.append({
                'rank': book['rank'],
                'isbn': [i['isbn13'] for i in book['isbns']],
                'date': date,
                'list': list_type
            })
        return results

    def gb_query(self, isbn):
        gb_response = self.gb.search(str(isbn))
        if gb_response['totalItems'] >= 1:
            gb_values = get_value(gb_response['items'][0])
            print(gb_response['items'][0]['volumeInfo']['title'])
            execute_queries(gb_values, self.connection)
            return True
        return False

    def update_list(self, list_type):
        results = self.get_rank(list_type)
        for i in results:
            for j in i['isbn']:
                print(f'ISBN: {j}')
                status = self.gb_query(j)
                # if gb_query function above was successful, we break from
                # looping over isbn's
                if status:
                    break

    def update(self):
        self.update_list('combined-print-and-e-book-nonfiction')
        self.update_list('combined-print-and-e-book-fiction')
        self.connection.close()
        return


    def get(self, book_list):
        # GET CURRENT RESULTS FROM DB
        return

if __name__ == "__main__":
    nyt = NYT()
    nyt.update()