import pickle
import requests
import json


with open('./example_google_books_return.obj','rb') as f:
    a = pickle.load(f)

def retreive_details(json_dict,relevant_values):
    new_dict={}
    i = 1
    for item in json_dict.keys():
        print("on item" + str(i) + ":"+item)
        if type(json_dict[item]) is dict:
            print("recursing")
            temp_dict = retreive_details(item,relevant_values)
            print(temp_dict)
            new_dict.update(temp_dict)
        if item in relevant_details:
            new_dict[item] = json_dict[item] 
        i+=1
    return new_dict

relevant_details=['id','googleId','title','authors','publisher',
                  'publishDate','description','isbn10','isbn13',
                  'pageCount','categories','Thumbnail','smallThumbnail',
                  'language','webRenderLink','textSnipped','isEbook']

my_dict_list = []

for item in a['items']:
    temp_dict = retreive_details(item,relevant_details)
    my_dict_list.append(temp_dict)
print(my_dict_list)