import os

import pandas as pd

from connection import connection


if __name__ == "__main__":

    engine = connection()
    path = 'goodbooks-10k/'

    for file in os.listdir(path):
        if file.endswith(".csv"):
            df = pd.read_csv(path + file)
            print(f'{file} -> SQL')
            df.to_sql(
                f'goodbooks_{file.split(".")[0]}',
                con=engine,
                if_exists='replace',
                index=False
                )
