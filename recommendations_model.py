import pickle
import re

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from surprise import Dataset, Reader
from surprise import KNNBasic
from surprise import accuracy
from surprise.model_selection import cross_validate, train_test_split
from surprise.model_selection import train_test_split

def data_import():
    books = pd.read_csv('https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/books.csv')
    ratings = pd.read_csv('https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/ratings.csv')
    return books, ratings

def clean_book_titles(title):
  title = re.sub(r'\([^)]*\)', '', title)
  title = re.sub(' + ', ' ', title)
  title = title.strip()
  return title

# should input be set to None by default?
def book_cleaning(books):
    books = books.copy()

    books = books[~books['isbn'].isna()]
    books = books[books['language_code'].str.startswith('en', na=False)]
    books = books[['book_id', 'title']]
    books['title'] = books['title'].apply(clean_book_titles)
    return books

def create_matrix(books, ratings):
    books = books.copy()
    ratings = ratings.copy()

    df = pd.merge(ratings, books, on='book_id')
    df  = df.drop_duplicates(['user_id', 'title'])

    matrix = df.pivot(index='title', columns='user_id', values='rating').fillna(0)
    return df

def create_model(df):
    df = df.copy()

    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['user_id', 'book_id', 'rating']], reader)
    sim_options = {
        'name': 'cosine',
        'user_based': False,
        'min_support': 5}
    algo = KNNBasic(sim_options=sim_options)

    # trainset, testset = train_test_split(data, test_size=.25)
    # algo.fit(trainset)
    # predictions = algo.test(testset)
    # print(accuracy.rmse(predictions))

    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
    return

if __name__ == "__main__":
    books, ratings = data_import()
    books = book_cleaning(books)
    matrix = create_matrix(books, ratings)
    create_model(matrix)
    