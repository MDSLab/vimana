import base64
import hashlib
import json
from binascii import hexlify

try:
    from hashlib import sha3_256
except ImportError:
    from sha3 import sha3_256

KV_PAIR_PREFIX_KEY = b'kvPairKey'
MODEL_PREFIX_KEY = b'modelPairKey'

def prefix_key(key):
    """Takes key as a string and returns a byte string
    """
    key = str.encode(key)
    return KV_PAIR_PREFIX_KEY + key

def prefix_model(key):
    """Takes key as a string and returns a byte string
    """
    key = str.encode(key)
    return MODEL_PREFIX_KEY + key

def encode_transaction(value):
    """Encode a transaction (dict) to Base64."""

    return base64.b64encode(json.dumps(value).encode('utf8')).decode('utf8')

def encode_output(value):
    """Takes value and converts to an integer byte string"""
    return bytes([int(value)])

def encode_output_str(value):
    """Takes value and converts to an string byte string"""
    return bytes(value, 'utf-8')

def decode_transaction(raw):
    """Decode a transaction from bytes to a dict."""

    return json.loads(raw.decode('utf8'))


def decode_transaction_base64(value):
    """Decode a transaction from Base64."""

    return json.loads(base64.b64decode(value.encode('utf8')).decode('utf8'))


def calculate_hash(key_list):
    if key_list.size == 0:
        return ''
    full_hash = sha3_256()
    for key in key_list:
        full_hash.update(key)
    return full_hash.hexdigest()

def get_transaction_method(tx):
    """ takes transacation as a json
    returns the type of transaction as a string
    """
    method_from_transaction = json.loads(tx)['method']
    return str(method_from_transaction)
