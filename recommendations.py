class Recommender():
    def __init__(self, books):
        self.books = books

    def recommend(self):
        for book in self.books:
            print(book.title)
        return self.books

'''
from random import shuffle
from pickle import load
from requests import get_json
from sklearn.neighbors import NearestNeighbors
from readrr_api.route_tools.gb_funcs import retrieve_details
from readrr_api.route_tools.gb_search import GBWrapper

api = GBWrapper()

with open('notebooks/knn_model.pkl', 'rb') as model:
    knn = load(model)

with open('notebooks/compressed_matrix.pkl', 'rb') as matrix:
    compressed = load(matrix)

with open('notebooks/book_titles.pkl', 'rb') as books:
    titles = load(books)

def get_recommendations(book_name, title_reference=titles,
                        matrix=compressed, model=knn, topn=5):
    """Returns a list of recommendations based on book title"""
    recs = []
    distances, indices = model.kneighbors(
        matrix[titles.index(book_name)].reshape(1, -1),
        n_neighbors=topn+1
    )
    for neighbor in indices[0]:
        title = title_reference[neighbor]
        recs.append(title)

    return recs


@recommendations.route('/recommendations', methods=['POST'])
def recommend():
    """
    Provide recommendations based on user bookshelf.
    """
    user_books = get_json()
    acquired = False

    favorites = []

    def shelf_iterate(shelf):
        """Checks shelf for a valid book title"""
        acquired = False
        for i in range(len(shelf)):
            try:
                target_book = shelf[i]['title']
                neighbors = get_recommendations(target_book)
                acquired = True
                break
            except ValueError:
                neighbors = None
                continue

        return neighbors, acquired, target_book

    for book in user_books:
        if book['favorite']:
            favorites.append(book['title'])

    shuffle(favorites)

    # if there are no favorites, recommend based on first book
    if len(favorites) >= 1:
        for i in range(len(favorites)):
            try:
                target_book = favorites[i]
                neighbors = get_recommendations(target_book)
                acquired = True
                break
            except ValueError:
                continue

    else:
        neighbors, acquired, target_book = shelf_iterate(user_books)

    # if book is not in known titles, recommend an alternative
    if not acquired:
        neighbors, acquired, target_book = shelf_iterate(user_books)
        if neighbors is None:
            target_book = "#GIRLBOSS"
            neighbors = get_recommendations(target_book)
    else:
        neighbors = get_recommendations(target_book)

    output_recs = []

    # skip first book
    for book in neighbors[1:]:
        book_data = api.search(book)
        target_data = book_data['items'][0]
        target_json = retrieve_details(target_data)
        output_recs.append(target_json)

    # change 'id' to 'googleId' at every list index
    for item in output_recs:
        item['googleId'] = item.pop('id')

    output = {'based_on': target_book,
              'recommendations': output_recs}

    return jsonify(output)
'''