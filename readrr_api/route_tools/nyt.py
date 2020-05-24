from datetime import datetime
from json import loads

from decouple import config
from requests import get

from connection import Connection
from gb_search import GBWrapper
from populate import execute_queries, get_value
from psycopg2 import sql


class NYT:
    def __init__(self):
        self.NYT_KEY = config("NYT_KEY")
        self.gb = GBWrapper(method="isbn")
        conn = Connection()
        self.connection = conn.connection

    def get_lists(self):
        request_url = (
            f"https://api.nytimes.com/svc/books/v3/lists/names.json?"
            f"api-key={self.NYT_KEY}"
        )
        request = get(request_url)
        return loads(request.text)

    def get_books(self, list_type):
        request_url = (
            f"https://api.nytimes.com/svc/books/v3/lists/current/"
            f"{list_type}.json?api-key={self.NYT_KEY}"
        )
        request = get(request_url)
        return loads(request.text)

    def get_rank(self, list_type):
        response = self.get_books(list_type)
        results = []
        date = response["results"]["bestsellers_date"]
        for book in response["results"]["books"]:
            results.append(
                {
                    "rank": book["rank"],
                    "isbn": [i["isbn13"] for i in book["isbns"]],
                    "date": date,
                    "list": list_type,
                }
            )
        return results

    def nyt_insert(self, data):
        cursor = self.connection.cursor()
        query = sql.SQL(
            "INSERT INTO nyt VALUES "
            "(%s, %s, %s, %s, %s)"
        )
        try:
            cursor.execute(query, data)
        except Exception as err:
            connection.rollback()
        else:
            connection.commit()
        cursor.close()
        
    def gb_query(self, isbn):
        gb_response = self.gb.search(str(isbn))
        if gb_response["totalItems"] >= 1:
            return get_value(gb_response["items"][0])
        return None

    def update_list(self, list_type):
        results = self.get_rank(list_type)
        for i in results:
            for j in i["isbn"]:
                gb_values = self.gb_query(j)
                if gb_values is not None:
                    execute_queries(gb_values, self.connection)
                    print(gb_values[0])
                    # self.nyt_insert(gb_values[0])
                    # once complete updating db, break from inner isbn loop
                    break

    def update(self):
        self.update_list("combined-print-and-e-book-nonfiction")
        self.update_list("combined-print-and-e-book-fiction")
        self.connection.close()
        return

    def get(self, book_list):
        # GET CURRENT RESULTS FROM DB
        return


if __name__ == "__main__":
    nyt = NYT()
    nyt.update()
