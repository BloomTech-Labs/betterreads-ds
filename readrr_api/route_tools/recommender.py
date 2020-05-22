from pickle import load
import os
import logging

# removed pandas import, replace if necessary
import spacy
from psycopg2 import sql
from psycopg2.extras import DictCursor
from sklearn.neighbors import NearestNeighbors

from .. route_tools.connection import Connection
from .. route_tools.gb_search import GBWrapper
from .. route_tools.populate import execute_queries, get_value
from .. route_tools.gb_funcs import retrieve_details

FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logging.disable(logging.DEBUG)

r_tools_path = os.path.join(os.path.dirname(__file__), '..', 'route_tools')

# load model dependencies
with open(os.path.join(r_tools_path, 'nlp.pkl'), 'rb') as vocab:
    nlp = load(vocab)

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
                (token.is_punct is False) &
                (token.pos_ != 'PRON') &
                (token.is_alpha is True)):
            tokens.append(token.text.lower())

    return tokens


class Book:

    def __init__(self, book):
        self.googleId = book['googleId']
        if type(book['authors']) == list:
            self.author = book['authors'][0]
        else:
            self.author = book['authors']
        self.title = book['title']
        self.conn = Connection().connection
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        self.pickle_path = os.path.dirname(__file__)

    def book_check(self, check_isbn=False, isbn=None):
        # CURRENTLY THE GOOGLE BOOKS DATA TAKES PRECENDENCE
        # DEVELOPMENT OPPORTUNITY: MERGE TWO TABLES TO ONE?

        # CHECKS IF BOOK IS IN 'gb_data' TABLE
        gb_isbn_query = sql.SQL(
            "SELECT * "
            "FROM gb_data "
            "WHERE isbn = %s LIMIT 1;"
        )
        gb_query = sql.SQL(
            "SELECT * "
            "FROM gb_data "
            "WHERE googleid = %s LIMIT 1;"
        )

        if check_isbn:
            self.cursor.execute(gb_query, (isbn,))
            response = self.cursor.fetchone()
            if response is not None:
                return response
            else:
                return False

        self.cursor.execute(gb_query, (self.googleId,))
        self.data = self.cursor.fetchone()
        if self.data is not None and self.data['description'] is not None:
            return True

        # CHECKS IF BOOK IS IN 'goodbooks_books_xml' TABLE
        goodbooks_query = sql.SQL(
            "SELECT * "
            "FROM goodbooks_books_xml "
            "WHERE title = %s LIMIT 1;"
        )
        self.cursor.execute(goodbooks_query, (self.title,))
        self.data = self.cursor.fetchone()
        if self.data is not None and self.data['description'] is not None:
            return True

        # RETURNING FALSE MEANS OUR BOOK IS NOT IN EITHER THE XML OR GB
        return False

    def db_insert(self, isbn=None):
        api = GBWrapper()
        if isbn is not None:
            google_books_response = api.search(isbn)
        else:
            google_books_response = api.search(self.googleId)

        # INSERTS GB_QUERY INTO DATABASE
        logging.debug("GETTING API DATA...")
        api_data = get_value(google_books_response['items'][0])
        if isbn is not None:
            gid = api_data[0]
            details = retrieve_details(google_books_response)
        else:
            gid = None
            details = None
        # execute_queries(api_data, self.conn, self.cursor)
        execute_queries(api_data, self.conn)
        return gid, details

    def collaborative_recommendations(self, top_n=10):
        # LOAD MODEL/MATRIX HERE
        # IF BOOK IS IN XML DATA,
        # LOOK UP BOOK ON COMPARISON MATRIX
        # RETURN TOP "N" NEARESTNEIGHBORS RECOMMENDATIONS
        # REFERENCE routes/recommendations.py
        return

    def content_recommendations(self, nn, tfidf, top_n=10):
        # USE get_description FUNCTION OR self.description
        # LOAD THE MODEL/MATRIX HERE

        # MAKE PREDICTIONS
        self.prediction = tfidf.transform([self.description])

        # RETURN TOP "N" NEARESTNEIGHBORS RECOMMENDATIONS
        self.distances, self.neighbors = nn.kneighbors(
            self.prediction.todense(),
            n_neighbors=top_n
        )
        return

    def gb_query(self, gid):
        gb_query = sql.SQL(
            "SELECT * "
            "FROM gb_data "
            "WHERE googleid = %s LIMIT 1;"
        )
        self.cursor.execute(gb_query, (gid,))
        return self.cursor.fetchone()

    def gb_id_query(self, isbn):
        """Queries DB using isbn"""
        gb_isbn_query = sql.SQL(
            "SELECT * "
            "FROM gb_data "
            "WHERE isbn = %s LIMIT 1;"
        )
        self.cursor.execute(gb_isbn_query, (isbn,))
        return self.cursor.fetchone()

    def gb_title_query(self, title):
        """Queries DB using title"""
        gb_title_query = sql.SQL(
            "SELECT * "
            "FROM gb_data "
            "WHERE title = %s LIMIT 1;"
        )
        self.cursor.execute(gb_title_query, (title,))
        return self.cursor.fetchone()

    def recommendations(self, model, vectorizer, sim_matrix, sim_index,
                        s_vectorizer, s_neighbors, bk_srch_idx):
        """
        Get recommendations for either type of model

        vectorizer: If content model, this may be something like TF-IDF
        model: The algorithm used for recommendations (i.e. NN, SVD)
        """
        # It seems the intent here was to provide various sorts of
        # recommendations here. In the interest of time, the hybrid
        # approach is directly implemented here
        THRESH = 0.5
        search_title = self.title + ' ' + self.author
        title_transformed = s_vectorizer.transform([search_title])
        dist, ind = s_neighbors.kneighbors(title_transformed)
        dist = dist.flatten()
        ind = ind.flatten()
        close_titles = list(zip(dist, ind))[0]

        if close_titles[0] > THRESH:
            i = close_titles[1]
            hybrid_title = bk_srch_idx[i]
        else:
            hybrid_title = None

        if hybrid_title:
            # get the index of the title in relation to sim_index
            idx = sim_index.index.tolist().index(hybrid_title)
            sim_scores = list(enumerate(sim_matrix[idx].toarray().flatten()))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:11]
            indices = [i[0] for i in sim_scores]
            titles = sim_index.iloc[indices].index
            # set an iterable for filling in data structure later
            iterable = titles
            model_type = "hybrid"
        else:
            # continue on to content attempt
            if self.book_check():
                self.description = self.data['description']
            else:
                self.db_insert()
                if self.book_check():
                    self.description = self.data['description']
                else:
                    logging.debug(
                        f"No description attainable for {self.title}. " +
                        "Suggest alternatives."
                    )
                    self.description = "Mock testing description"
                # BE AWARE OF EXCEPTION OF RETURNING NO DESCRIPTION
                # TO DO: SNIPPET QUERY IF DESCRIPTION UNAVAILABLE

            self.content_recommendations(model, vectorizer)
            iterable = self.neighbors[0][1:]
            model_type = "content"

            with open(os.path.join(self.pickle_path, 'googleIdMap.pkl'),
                      'rb') as lkp:
                lookup = load(lkp)
                logging.debug("Loaded lookup")

        book_details = []
        self.output = {
            'based_on': self.title,
            'recommendations': book_details
        }

        logging.debug("Model Type: " + model_type)
        for i in iterable:
            if model_type is "hybrid":
                # get industry_identifier
                logging.debug(
                        f"Starting hybrid output with \"{i}\" from iterable"
                )
                ii = sim_index.loc[i]['isbn13']
                i_results = self.gb_id_query(ii)
                if i_results is None:
                    # if results are none, make gbapi call on isbn
                    gid, api_details = self.db_insert(isbn=ii)
                    logging.debug("GOOGLE ID ACQUIRED: " + gid)
                    # switch to google id for reference to avoid empty data
                    i_results = self.gb_query(gid)
                    if i_results is None:
                        # use title to query db if gid fails
                        i_results = self.gb_title_query(i)
                        if i_results is None:
                            # failing that, simply send back api data
                            # change 'id' to 'googleId' before sending
                            for item in api_details:
                                item['googleId'] = item.pop('id')
                            book_details.append(api_details)
                            logging.debug("DETAILS ACQUIRED VIA API")
                            continue

            else:
                logging.debug(f"Using lookup with {model_type}")
                i_gid = lookup[i]
                i_results = self.gb_query(i_gid)

            recommendation_output = {
                "authors": i_results['authors'],
                "averageRating": i_results['averagerating'],
                "categories": i_results['categories'],
                "description": i_results['description'],
                "googleId": i_results['googleid'],
                "industryIdentifiers": [
                    {
                        "identifier": i_results['isbn'],
                        "type": "ISBN"
                    }
                    ],
                "isEbook": i_results['isebook'],
                "language": i_results['lang'],
                "pageCount": i_results['pagecount'],
                "publishedDate": i_results['publisheddate'],
                "publisher": i_results['publisher'],
                "smallThumbnail": i_results['smallthumbnail'],
                "textSnippet": i_results['textsnippet'],
                "thumbnail": i_results['thumbnail'],
                "title": i_results['title'],
                "webReaderLink": i_results['webreaderlink']
            }

            if recommendation_output['authors'] is not None:
                for i, a in enumerate(recommendation_output['authors']):
                    recommendation_output['authors'][i] = a.replace("'", "")

            if recommendation_output['categories'] is not None:
                for i, c in enumerate(recommendation_output['categories']):
                    recommendation_output['categories'][i] = c.replace("'", "")

            book_details.append(recommendation_output)

        self.cursor.close()
        self.conn.close()

        return self.output
