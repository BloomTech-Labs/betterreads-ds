from decouple import config


class NYT():

    def __init__(self):
        NYT_KEY = config('NYT_KEY')
        # self.engine = connection()
        return

    def query(self):
        '''
        queries NYT API
        returns: JSON list of bestsellers
        '''
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
