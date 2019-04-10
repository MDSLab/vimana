import random
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

import numpy as np
import sys


try:
    from hashlib import sha3_256
except ImportError:
    from sha3 import sha3_256

def encode_transaction(value):
    """Encode a transaction (dict) to Base64."""

    return base64.b64encode(json.dumps(value).encode('utf8')).decode('utf8')


class UserBehavior(TaskSet):


    def on_start(self):
        self.val = random.randint(1,1000000000)
        pass


    @task(1)
    def profile(self):


        tx_dict = json.dumps(str(self.val) + '=' + str(self.val) )
        self.val+=1

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




