import base64
import hashlib
import json
from binascii import hexlify

try:
    from hashlib import sha3_256
except ImportError:
    from sha3 import sha3_256


def encode_transaction(value):
    """Encode a transaction (dict) to Base64."""

    return base64.b64encode(json.dumps(value).encode('utf8')).decode('utf8')


def decode_transaction(raw):
    """Decode a transaction from bytes to a dict."""

    return json.loads(raw.decode('utf8'))


def decode_transaction_base64(value):
    """Decode a transaction from Base64."""

    return json.loads(base64.b64decode(value.encode('utf8')).decode('utf8'))


def calculate_hash(key_list):
    if not key_list:
        return ''

    full_hash = sha3_256()
    for key in key_list:
        full_hash.update(key.encode('utf8'))

    return full_hash.hexdigest()
