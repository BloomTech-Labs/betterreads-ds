from json import loads

from decouple import config
from requests import get

# IMPORT CONNECTION

class NYT:

    def __init__(self):
        super().__init__()

    def all_lists(self):
        # https://api.nytimes.com/svc/books/v3/lists/names.json?api-key=
        return

    def get_books(self, list_type):
        NYT_KEY = config('NYT_KEY')
        request_url = f'https://api.nytimes.com/svc/books/v3/lists/current/{list_type}.json?api-key={NYT_KEY}'
        results = get(request_url)
        # WE MAY NEED TO PARSE DATA HERE
        return loads(results.text)
    
    def update(self):
        # MAY WANT TO IMPORT FROM ELSEWHERE
        return

    def get(self, book_list):
        # GET CURRENT RESULTS FROM DB
        return
