from psycopg2 import sql

from connection import Connection
from gb_search import GBWrapper


class Book:

    def __init__(self, book):
        self.googleId = book['googleId']
        self.title = book['title']
        self.conn = Connection().connection

    def book_check(self):
        # CURRENTLY THE GOOGLE BOOKS DATA TAKES PRECENDENCE
        # DEVELOPMENT OPPORTUNITY: MERGE TWO TABLES TO ONE?
        cursor = self.conn.cursor()

        # CHECKS IF BOOK IS IN 'gb_data' TABLE
        gb_query = sql.SQL(
            "SELECT * "
            "FROM gb_data "
            "WHERE googleid = %s LIMIT 1;"
        )
        cursor.execute(gb_query, (self.googleId,))
        self.data = cursor.fetchone()
        if self.data is not None:
            return True

        # CHECKS IF BOOK IS IN 'goodbooks_books_xml' TABLE
        goodbooks_query = sql.SQL(
            "SELECT * "
            "FROM goodbooks_books_xml "
            "WHERE title = %s LIMIT 1;"
        )
        cursor.execute(goodbooks_query, (self.title,))
        self.data = cursor.fetchone()
        if self.data is not None:
            return True

        # RETURNING FALSE MEANS OUR BOOK IS NOT IN EITHER THE XML OR GB
        return False

    def db_insert(self):
        api = GBWrapper()
        self.google_books_response = api.search(self.googleId)
        # INSERTS GB_QUERY INTO DATABASE

        # IF THIS RUNS, WE STILL NEED TO SET self.data
        return

    def get_description(self):
        # BASED ON BOOK_CHECK FUNCTION, GET DESCRIPTION
        # BE AWARE OF EXCEPTION OF RETURNING NO DESCRIPTION 
        # self.description = description
        # IF THIS DOES NOT WORK, LOOK AT TEXT SNIPPET
        return

    def collaborative_recommendations(self, top_n=10):
        # LOAD MODEL/MATRIX HERE
        # IF BOOK IS IN XML DATA,
        # LOOK UP BOOK ON COMPARISON MATRIX
        # RETURN TOP "N" NEARESTNEIGHBORS RECOMMENDATIONS
        # REFERENCE routes/recommendations.py
        return

    def content_recommendations(self, top_n=10):
        # USE get_description FUNCTION OR self.description
        # LOAD THE MODEL/MATRIX HERE
        # MAKE PREDICTIONS
        # RETURN TOP "N" NEARESTNEIGHBORS RECOMMENDATIONS
        # REFERENCE recs.py deleted
        return

    def hybrid_recommendations(self):
        # WEIGHT COLLABORATIVE / CONTENT RECOMMENDATIONS
        return

if __name__ == "__main__":
    bookshelf = [
    {
        "googleId": "MQeHAAAAQBAJ",
        "title": "The Martian",
        "authors": 	"Andy Weir",
        },
    {
        "googleId": "OG0e6djUgUYC",
        "title": "The Brothers Karamazov",
        "authors": "Fyodor Dostoevsky",
        },
    {
        "googleId": "-25.0756",
        "title": "Data Science in Production",
        "authors": "Ben Weber",
        }
        ]

    for i in bookshelf:
        book = Book(i)
        book.runner()
