""" Contains state changes for the abci node

The connection between AI models and state happens here. 
"""
import logging
import sys
import os
import json

import rlp
from trie import Trie
from trie.db.memory import MemoryDB
from rlp.sedes import big_endian_int, binary
import numpy as np

from model import KerasModel
from utils import calculate_hash

logging.basicConfig(level=os.environ.get("LOGLEVEL", "NOTSET"))
logger = logging.getLogger(__name__)

STATE_KEY = b'stateKey'
BLANK_ROOT_HASH = b''

method_query = 'query'
method_upload = 'model_upload'
method_activate = 'model_activate'
method_list = ( method_upload , method_activate, method_query)

class StateMetaData(rlp.Serializable):
    fields = [
        ('size', big_endian_int),
        ('height', big_endian_int),
        ('apphash', binary)
    ]

    def __init__(self, size, height, apphash):
        super().__init__(size, height, apphash)


class State(object):
    """
    Talks directly to cold storage and the merkle
    only
    """

    def __init__(self, db, size, height, apphash):
        self.db = db
        self.size = size
        self.height = height
        self.apphash = apphash

        # TODO pass the keras model also as init parameter
        self.keras_model = KerasModel()

    @classmethod
    def load_state(cls, dbfile=None):
        """ Create or load State.
        returns: State
        """
        if not dbfile:
            return (cls(MemoryDB(), 0, 0, BLANK_ROOT_HASH))

    def save(self):
        # Save to storage
        meta = StateMetaData(self.size, self.height, self.apphash)
        serial = rlp.encode(meta, sedes=StateMetaData)
        self.db.set(STATE_KEY, serial)
        return self.apphash
    
    def get_model_output(self, tx):
        """function takes transaction as the input
        returns the output of the model
        """
        input_from_transaction =  json.loads(tx)['input']

        try:
            return self.keras_model.get_model_output(input_from_transaction)
        except Exception as e:
            logger.warning('Error while using Keras model (%s): %s', type(e).__name__, e)
            return None 

    def get_transaction_hash(self, tx, mode):
        """function takes raw hex tx as input
        returns the hash of the transactiaon of the input field
        """
        if(mode = method_query):
            input_from_transaction =  json.loads(tx)['input']
            input_from_transaction_as_np = np.asarray(input_from_transaction)

            hash_of_transaction = calculate_hash(input_from_transaction_as_np)
            return hash_of_transaction
        
        elif(mode = method_activate):
            model_hash_from_transaction = json.loads(tx)['model']
            model_url_from_transaction = json.loads(tx)['url']

            return model_hash_from_transaction, model_url_from_transaction
