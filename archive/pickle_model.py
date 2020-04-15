import pandas as pd
import pickle


from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

import re

books = pd.read_csv('https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/books.csv')

ratings = pd.read_csv('https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/ratings.csv')

cols = ['book_id', 'title']
books = books[cols]

def clean_book_titles(title):
  title = re.sub(r'\([^)]*\)', '', title) # handles brackets
  title = re.sub(' + ', ' ', title) #compresses multi spaces into a single space
  title = title.strip() # handles special characters
  return title

books['title'] = books['title'].apply(clean_book_titles)

books_ratings = pd.merge(ratings, books, on='book_id')

user_ratings = books_ratings.drop_duplicates(['user_id', 'title'])

user_matrix = user_ratings.pivot(index='title', columns='user_id', values='rating').fillna(0)

compressed = csr_matrix(user_matrix.values)

knn = NearestNeighbors(algorithm='brute', metric='cosine')
knn.fit(compressed)

pickle.dump(knn, open('knn_model.pkl','wb'))
