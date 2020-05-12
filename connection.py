from decouple import config
from psycopg2 import connect


class Connection:

    def __init__(self):
        self.DB_USER = config('DB_USERNAME')
        self.DB_PASS = config('DB_PASSWORD')
        self.DB_HOST = config('DB_HOST')
        self.DB_NAME = config('DB_NAME')
        self.DB_URL = f'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:5432\
            /{DB_NAME}'
        self.connection = connect(
            dbname=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST
        )
