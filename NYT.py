from decouple import config


class NYT():

    def __init__(self):
        self.NYT_KEY = config('NYT_KEY')
        # self.engine = connection()
        return

    def query(self):
        '''
        queries NYT API
        returns: JSON list of bestsellers
        '''
        print(self.NYT_KEY)
        return

    def update(self, table_name, books):
        '''
        updates DB with bestsellers
        returns: DB updated confirmation message
        '''
        return

    def get_bestsellers(self, genre):
        '''
        queries DB for most recent bestsellers (based on genre)
        returns: JSON
        '''
        return


if __name__ == "__main__":
    conn = NYT()
    conn.query()
