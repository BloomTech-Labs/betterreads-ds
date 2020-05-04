import pickle
import re

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

def data_import():
    books = pd.read_csv('https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/books.csv')
    ratings = pd.read_csv('https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/ratings.csv')

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