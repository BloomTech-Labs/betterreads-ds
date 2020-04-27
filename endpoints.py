from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from recommendations import Recommender

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
    r = Recommender(books)
    recommendations = r.recommend()
    return recommendations

if __name__ == "__main__":
    request_body = 'tests/mock_bookshelf.json'
    r = recommend(books=request_body)
    print(r)