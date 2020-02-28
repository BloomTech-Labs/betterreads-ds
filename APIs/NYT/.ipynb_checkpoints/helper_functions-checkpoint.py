import requests
import json

def aggregate(alist,attribute):
    """ This function aggregates specific attributes from a list of dictionaries

    INPUT:
    alist     - a list of dictionaries. All the dictionaries have the same
                "Schema" meaning that all of the dictionaries have the same
                key values

    attribute - a dictionary key that you would like to aggregate in a list

    OUTPUT:
    agg       - a list of values contained within the attribute pair
    """
    agg = []
    for i in alist:
        agg.append(i[attribute])
    return agg

def dictlist_to_df(alist):
    """ Functionto turn a list of dictionaries into to a pandas dataframe"""
    column_names = alist[0].keys()
    df = pd.Dataframe(columns=column_names)
    for item in column_names:
        column_vals = aggregate(alist,item)
        df[item] = column_vals
    return df

def test():
    print('test')
    pass

def get_list(book_list_name,api_key):
    """ Function to compose and obtain information from a NYT
    books endpoint.
    
    There are many book lists, and the api returns the book lists
    in JSON format with a lot of information beyond just the titles 
    of the books. 
    
    This function returns a book list with just the pertinent 
    information. a dictionary in the format {ISBN:Book title}. 
    
    Dependencies: 
    requests
    json
    """
    
    request_url=("https://api.nytimes.com/svc/books/v3/lists/current/"
                 + book_list_name
                 + ".json?api-key="
                 + api_key)
    results = requests.get(request_url)
    results = json.loads(results.text)
    
    book_list = aggregate(results['results']['books'],'title')
    
    return book_list