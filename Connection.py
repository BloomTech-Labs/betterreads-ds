from decouple import config
from sqlalchemy import create_engine


def connection():
    DB_USER = config('DB_USERNAME')
    DB_PASS = config('DB_PASSWORD')
    DB_HOST = config('DB_HOST')
    DB_NAME = config('DB_NAME')
    DB_URL = f'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}'
    engine = create_engine(DB_URL)
    return engine