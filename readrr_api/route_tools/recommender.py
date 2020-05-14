from pickle import load, dump
import os

import pandas as pd
from psycopg2 import sql
from psycopg2.extras import DictCursor
from sklearn.neighbors import NearestNeighbors

from connection import Connection
from gb_search import GBWrapper
from populate import execute_queries, get_value


class Book:

    def __init__(self, book):
        self.googleId = book['googleId']
        self.title = book['title']
        self.conn = Connection().connection
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)

    def book_check(self):
        # CURRENTLY THE GOOGLE BOOKS DATA TAKES PRECENDENCE
        # DEVELOPMENT OPPORTUNITY: MERGE TWO TABLES TO ONE?

        # CHECKS IF BOOK IS IN 'gb_data' TABLE
        gb_query = sql.SQL(
            "SELECT * "
            "FROM gb_data "
            "WHERE googleid = %s LIMIT 1;"
        )
        self.cursor.execute(gb_query, (self.googleId,))
        self.data = self.cursor.fetchone()
        if self.data is not None:
            return True

        # CHECKS IF BOOK IS IN 'goodbooks_books_xml' TABLE
        goodbooks_query = sql.SQL(
            "SELECT * "
            "FROM goodbooks_books_xml "
            "WHERE title = %s LIMIT 1;"
        )
        self.cursor.execute(goodbooks_query, (self.title,))
        self.data = self.cursor.fetchone()
        if self.data is not None:
            return True

        # RETURNING FALSE MEANS OUR BOOK IS NOT IN EITHER THE XML OR GB
        return False

    def db_insert(self):
        api = GBWrapper()
        google_books_response = api.search(self.googleId)
        
        # INSERTS GB_QUERY INTO DATABASE
        db_data = get_value(google_books_response['items'][0])
        # execute_queries(db_data, self.conn, self.cursor)
        execute_queries(db_data, self.conn)
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
        with open('nlp.pkl', 'rb') as nlp:
            nlp = load(nlp)
        STOP_WORDS = ["new", "book", "author", "story", "life", "work", "best", 
                    "edition", "readers", "include", "provide", "information"]
        STOP_WORDS = nlp.Defaults.stop_words.union(STOP_WORDS)
        with open('tfidf_model.pkl', 'rb') as tfidf:
            tfidf = load(tfidf)
        # with open('dtm.pkl', 'rb') as dtm:
        #     dtm = load(dtm)
        with open('nn.pkl', 'rb') as nn:
            nn = load(nn)

        # MAKE PREDICTIONS
        self.prediction = tfidf.transform([self.description])

        # RETURN TOP "N" NEARESTNEIGHBORS RECOMMENDATIONS
        self.distances, self.neighbors = nn.kneighbors(
            self.prediction.todense(),
            n_neighbors=top_n
        )
        return

    def runner(self):
        if self.book_check():
            self.description = self.data['description']
        else:
            self.db_insert()
            self.book_check()
            self.description = self.data['description']
            # BE AWARE OF EXCEPTION OF RETURNING NO DESCRIPTION 
        self.content_recommendations()

    def hybrid_recommendations(self):
        # WEIGHT COLLABORATIVE / CONTENT RECOMMENDATIONS
        return

    # TO DO: SNIPPET QUERY IF DESCRIPTION UNAVAILABLE
    # cursor.close()
    # self.conn.close()


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
        "googleId": "4e43zQEACAAJ",
        "title": "Data Science in Production",
        "authors": "Ben Weber",
        }
        ]
    
    with open('nlp.pkl', 'rb') as nlp:
        nlp = load(nlp)

    STOP_WORDS = ["new", "book", "author", "story", "life", "work", "best", 
            "edition", "readers", "include", "provide", "information"]
    STOP_WORDS = nlp.Defaults.stop_words.union(STOP_WORDS)

    def tokenize(text):
        '''
        Input: String
        Output: list of tokens
        '''
        doc = nlp(text)

        tokens = []
        
        for token in doc:
            if ((token.text.lower() not in STOP_WORDS) & 
                (token.is_punct == False) & 
                (token.pos_ != 'PRON') & 
                (token.is_alpha == True)):
                tokens.append(token.text.lower())
                # tokens.append(token.lemma_.lower())
        return tokens

    for i in bookshelf:
        book = Book(i)
        book.runner()
        print(book.distances, book.neighbors)
        # print(book.title)