from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    userBooksId: int = None
    bookId: int = None
    googleId: str = None
    title: str = None
    authors: str = None
    readingStatus: int = None
    favorite: bool = None
    categories: str = None
    thumbnail: str = None
    pageCount: int = None
    dateStarted: datetime = None
    dateEnded: datetime = None
    dateAdded: datetime = None

@app.post('/recommendations')
def recommend(*, books: List[Book]):
    for book in books:
        print(book.title)
    '''
    from goodreads_api.recommendations import Recommender
    r = Recommender(books)
    return r
    '''
    return books