"""
Universal Model Manager module
Downloads large 'keras' model file
and saves them locally 
"""

import requests
import shutil

try:
    from hashlib import sha3_256
except ImportError:
    from sha3 import sha3_256


MODEL_FOLDER = "models/"

def download_model(url):
    """
    Downloads large model file 
    returns the hash of the newly downloded model 
    and location of the model in temp folder
        :param url: string of url location of the model
    """
    # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
    local_filename = url.split('/')[-1]
    local_filename = MODEL_LOCATION + local_filename

    full_hash = sha3_256()

    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        full_hash.update(r.raw)

    return full_hash.hexdigest(), local_filename


def get_model(key, url):
    """
    Function gets a model from the paramters provided 
        :param key: A hash of the model uploaded
        :param url: A URL locator of the model file

    returns
        :param location: relative location of the model
    """   

    # try three times to download the model
    for i in range(3):
        # download model and calcuate the new hash key
        # this method downloads the model and saves in the 
        # temp model folder as well. 
        key_from_tx, location = download_model(url)

        if(key == key_from_tx):
            # this is done so that the model is not manipulated
            break
    
    if(key != key_from_tx):
        raise ValueError
    
    return location
    


