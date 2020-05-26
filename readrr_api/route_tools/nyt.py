from datetime import datetime
from json import loads, dumps

from decouple import config
from psycopg2 import sql
from psycopg2.extras import DictCursor
from requests import get

from connection import Connection
from gb_search import GBWrapper
from populate import execute_queries, get_value


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

    def get_books(self, list_type, date="current"):
        request_url = (
            f"https://api.nytimes.com/svc/books/v3/lists/{date}/"
            f"{list_type}.json?api-key={self.NYT_KEY}"
        )
        request = get(request_url)
        return loads(request.text)

    def get_rank(self, list_type):
        response = self.get_books(list_type)
        results = []
        date = response["results"]["published_date"]
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
            "INSERT INTO nyt (googleid, rank, isbn, nyt_date, nyt_list) "
            "VALUES (%s, %s, %s, %s, %s);"
        )
        try:
            cursor.execute(query, data)
        except Exception as err:
            self.connection.rollback()
        else:
            self.connection.commit()
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
                    self.nyt_insert(
                        [gb_values[0], i["rank"], j, i["date"], i["list"]]
                        )
                    # once complete updating db, break from inner isbn loop
                    break

    def update(self):
        self.update_list("combined-print-and-e-book-nonfiction")
        self.update_list("combined-print-and-e-book-fiction")
        self.connection.close()
        return

    def get(self, book_list):
        """
        List: "combined-print-and-e-book-nonfiction"
        """
        cursor = self.connection.cursor(cursor_factory=DictCursor)

        nyt_query = sql.SQL(
            "SELECT gb_data.* "
            "FROM gb_data "
            "INNER JOIN ( "
            "SELECT googleid, MAX(nyt_date), nyt_list, rank "
            "FROM nyt "
            "WHERE nyt_list = %s "
            "GROUP BY googleid, nyt_date, nyt_list, rank "
            "ORDER BY rank "
            ") nyt "
            "ON gb_data.googleid = nyt.googleid "
        )

        cursor.execute(nyt_query, (book_list,))
        books = cursor.fetchall()
        output = {"based_on": book_list, "recommendations": []}
        for book in books:
            output["recommendations"].append(dict(book.items()))

        cursor.close()
        self.connection.close()
        return output
