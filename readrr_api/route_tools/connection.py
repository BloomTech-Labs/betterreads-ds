from decouple import config
from sqlalchemy import create_engine


<<<<<<< HEAD:connection.py
def connection():
    DB_USER = config('DB_USERNAME')
    DB_PASS = config('DB_PASSWORD')
    DB_HOST = config('DB_HOST')
    DB_NAME = config('DB_NAME')
    DB_URL = f'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}'
    return create_engine(DB_URL)
=======
class Connection:

    def __init__(self):
        self.DB_USER = config('DB_USERNAME')
        self.DB_PASS = config('DB_PASSWORD')
        self.DB_HOST = config('DB_HOST')
        self.DB_NAME = config('DB_NAME')

        self.url = f'postgres://{self.DB_USER}:{self.DB_PASS}'\
            f'@{self.DB_HOST}:5432/{self.DB_NAME}'
        self.connection = connect(
            dbname=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST
        )
>>>>>>> e6b857e4531bcb98cdec97ad9b6f49176b6eb497:readrr_api/route_tools/connection.py
