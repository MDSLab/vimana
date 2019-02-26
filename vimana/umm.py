"""
Universal Model Manager module
Downloads large 'keras' model file
and saves them locally 
"""

import requests
import os

try:
    from hashlib import sha3_256
except ImportError:
    from sha3 import sha3_256

from progress.bar import ShadyBar
from progress.spinner import Spinner


TEMP_LOCATION = "temp/"
MODEL_LOCATION = "models/"


def download_model(name, url):
    """
    Downloads large model file 
    returns the hash of the newly downloded model 
    and location of the model in temp folder
        :param url: string of url location of the model
        :param name: string name of model 
    """
    # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
    local_filename = url.split('/')[-1]

    local_filename = TEMP_LOCATION + local_filename

    full_hash = sha3_256()
    with requests.get(url, stream=True) as r:
        size = r.headers['content-length']
        if size:
            p = ShadyBar(local_filename, max=int(size))
        else:
            p = Spinner(local_filename)
            
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    p.next(len(chunk))
                    f.write(chunk)
                    full_hash.update(chunk)
                    # f.flush()

    unique_filename = MODEL_LOCATION + name + ".h5"
    os.rename(local_filename, unique_filename)

    return full_hash.hexdigest(), unique_filename


def get_model(name, key, url):
    """
    Function gets a model from the paramters provided 
        :param anme: name of the model uploaded
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
        key_from_tx, location = download_model(name, url)

        # TODO check if model already exists

        if(key == key_from_tx):
            # this is done so that the model is not manipulated
            break

    if(key != key_from_tx):
        raise ValueError("The model recived is insecure please try again")

    return location
