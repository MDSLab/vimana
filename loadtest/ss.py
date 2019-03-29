from random import Random
from locust import HttpLocust, TaskSet, task
import numpy as np
import requests
from PIL import Image
import struct
import json
import logging
import time
import csv
import scipy
import scipy.stats

from shutil import move, copyfile
import os

import base64
import hashlib
import json
from binascii import hexlify
import json
from uuid import uuid4

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import numpy as np
from keras.models import load_model
from PIL import Image
import sys
from keras import backend as K
from scipy.ndimage import filters
from scipy import misc

try:
    from hashlib import sha3_256
except ImportError:
    from sha3 import sha3_256

# Source of the code is based on an excelent piece code from stackoverflow
# http://stackoverflow.com/questions/22937589/how-to-add-noise-gaussian-salt-and-pepper-etc-to-image-in-python-with-opencv

def noise_generator (noise_type,image):
    """
    Generate noise to a given Image based on required noise type
    
    Input parameters:
        image: ndarray (input image data. It will be converted to float)
        
        noise_type: string
            'gauss'        Gaussian-distrituion based noise
            'poission'     Poission-distribution based noise
            's&p'          Salt and Pepper noise, 0 or 1
            'speckle'      Multiplicative noise using out = image + n*image
                           where n is uniform noise with specified mean & variance
    """
    row,col= image.shape
    if noise_type == "gauss":       
        mean = 0.0
        var = 0.01
        sigma = var**0.5
        gauss = np.array(image.shape)
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch)
        noisy = image + gauss
        return noisy.astype('uint8')
    elif noise_type == "s&p":
        s_vs_p = 0.5
        amount = 0.004
        out = image
        # Generate Salt '1' noise
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
              for i in image.shape]
        out[coords] = 255
        # Generate Pepper '0' noise
        num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
              for i in image.shape]
        out[coords] = 0
        return out
    elif noise_type == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy
    elif noise_type =="speckle":
        gauss = np.random.randn(row,col,ch)
        gauss = gauss.reshape(row,col,ch)        
        noisy = image + image * gauss
        return noisy
    else:
        return image
    

def write_to_csv(time_list, name):
    with open(str(name) + ".csv", 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(time_list)

def encode_transaction(value):
    """Encode a transaction (dict) to Base64."""

    return base64.b64encode(json.dumps(value).encode('utf8')).decode('utf8')

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

test_input_value = Image.open("test.jpg")

class UserBehavior(TaskSet):

    def on_start(self):
        pass


    @task(1)
    def profile(self):
        input_value = test_input_value
        input_value = np.array(input_value)
        input_value = noise_generator('s&p', input_value)

        
        input_value = input_value.reshape((1,)+input_value.shape+(1,))

        model = "current"

        transaction = {
            'method': 'query',
            'model': model,
            'input': input_value
        }

        # Since numpy is not json serializable
        # https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
        tx_dict = json.dumps(transaction, cls=NumpyEncoder)
        
        # tendermint_host = '35.246.69.140'
        # tendermint_port = 26657
        # endpoint = 'http://{}:{}/'.format(tendermint_host, tendermint_port)

        endpoint =''

        payload = {
            'method': 'broadcast_tx_commit',
            'jsonrpc': '2.0',
            'params': [encode_transaction(tx_dict)],
            'id': str(uuid4())
        }
        r = self.client.post(endpoint, data=json.dumps(payload))

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 000
    max_wait = 000




