"""
This module is a set of helper functions to process data from the google
books API. The functions are as follows:

retreive_details()  - Retreive specific keys from a dictionary object

clean()             - Alter data to match data model

process_list()      - Process a list of dictionaries to endpoint output format

"""
import pickle
import requests
import json

# This is a general function. Should work on any JSON data
def retreive_details(input_dict,keys_to_extract):
    """
    Retreive specific keys from a dictionary object
    
    This function searches through a dictionary, and
    retreives keys that match keys from a list. This function 
    will find matching keys in every level of the dictionary heirarchy.
    
    Inputs:
    input_dict      -  A dictionary (expected to be from json.loads() 
                       in the context of BetterReads, but the function
                       will work on any dictionary).
    keys_to_extract -  A list of keys that you want to extract from the 
                       json_dict object.
                       
    Output:
    new_dict        -  A new "flattened"dictionary with all the matching keys. 
                       All the keys are in the top level.
    """
    
    new_dict={}
    for item in input_dict.keys():
        if type(input_dict[item]) is dict:
            temp_dict = retreive_details(input_dict[item],keys_to_extract)
            new_dict.update(temp_dict)
        if item in keys_to_extract:
            new_dict[item] = input_dict[item] 
    return new_dict

# The following functions are specific to the BetterReads Project
def clean(input_dict):
    """
    Alter data to match data model 
    
    This function reformats isbns, and modifies the id name
    from a dictionary returned from retreive_details. It also 
    changes the id key to googleId to match the format that the
    API endpoint specifies.
    
    Input:
    input_dict  - a dictionary output from retreive_details using
                  the list of keys required for the BetterReadsDS 
                  API response.
    
    Output:
    output_dict - a dictionary ready to send as a response to a
                  request received by the server.
    """
    
    my_dict = {}
    
    # Change the format of the isbn data
    try:
        for i in input_dict['industryIdentifiers']:
            my_dict[("".join(i['type'].split('_')).lower())] = i['identifier']

        # Add isbns to dictionary and remove the industryIdentifiers key
        input_dict.update(my_dict)
        del input_dict['industryIdentifiers']
    except KeyError:
        pass
    
    # Change id to googleId
    # Try/except should not be necessary here.
    # Google Books always returns an id
    input_dict['googleId']=input_dict['id']
    del input_dict['id']
    
    output_dict = input_dict
    return output_dict

def process_list(list_of_entries,keys_to_extract):
    """
    Process a list of dictionaries to endpoint output format
    
    This function takes a list of dictionaries, extracts the keys
    specified, and then cleans the resulting list of dictionaries.
    See the clean function for details on what "cleaning" entails.
    
    Inputs: 
    list_of_entries - A list of dictonaries from the Google Books API.
                    
    keys_to_extract - A list of keys that you want to extract from the
                      json_dict object.
    
    Outputs:
    out_list        - a list of dictionaries containing book entries.
    
    """
    out_list = []
    for i in list_of_entries:
        parsed_dict = retreive_details(i,keys_to_extract)
        clean_dict = clean(parsed_dict)
        out_list.append(clean_dict)
    return out_list