# Thank you BigchianDB https://github.com/bigchaindb/bigchaindb

"""Module containing main contact points with Tendermint and
Models.

"""
import logging
from collections import namedtuple
from uuid import uuid4
import rapidjson
import os

try:
    from hashlib import sha3_256
except ImportError:
    # NOTE: neeeded for Python < 3.6
    from sha3 import sha3_256

import requests

from tendermint_utils import encode_transaction, merkleroot
from model import KerasModel

logging.basicConfig(level=os.environ.get("LOGLEVEL", "NOTSET"))
logger = logging.getLogger(__name__)

config = {
    'tendermint': {
        'host': 'localhost',
        'port': 26657,
    },
}

class Vimana(object):
    """ Vimana API

    send transations between models
    """
    def __init__(self, connection=None):
        """Initialize the Vimana instance

        """
        self.mode_commit = 'broadcast_tx_commit'
        self.mode_list = ('broadcast_tx_async',
                          'broadcast_tx_sync',
                          self.mode_commit)
        self.tendermint_host = config['tendermint']['host']
        self.tendermint_port = config['tendermint']['port']
        self.endpoint = 'http://{}:{}/'.format(self.tendermint_host, self.tendermint_port)
        self.block = None
        self.keras_model = KerasModel()

    def post_transaction(self, transaction, mode):
        """Submit a valid transaction to the mempool."""
        if not mode or mode not in self.mode_list:
            raise ValidationError('Mode must be one of the following {}.'
                                  .format(', '.join(self.mode_list)))

        tx_dict = transaction.tx_dict if transaction.tx_dict else transaction.to_dict()
        payload = {
            'method': mode,
            'jsonrpc': '2.0',
            'params': [encode_transaction(tx_dict)],
            'id': str(uuid4())
        }
        # TODO: handle connection errors!
        return requests.post(self.endpoint, json=payload)

    def write_transaction(self, transaction, mode):
        # This method offers backward compatibility with the Web API.
        """Submit a valid transaction to the mempool."""
        response = self.post_transaction(transaction, mode)
        return self._process_post_response(response.json(), mode)

    def _process_post_response(self, response, mode):
        logger.debug(response)

        error = response.get('error')
        if error:
            status_code = 500
            message = error.get('message', 'Internal Error')
            data = error.get('data', '')

            if 'Tx already exists in cache' in data:
                status_code = 400

            return (status_code, message + ' - ' + data)

        result = response['result']
        if mode == self.mode_commit:
            check_tx_code = result.get('check_tx', {}).get('code', 0)
            deliver_tx_code = result.get('deliver_tx', {}).get('code', 0)
            error_code = check_tx_code or deliver_tx_code
        else:
            error_code = result.get('code', 0)

        if error_code:
            return (500, 'Transaction validation failed')

        return (202, '')

    def store_block(self, block):
        """Create a new block."""

        self.block = block
        return

    def get_latest_block(self):
        """Get the block with largest height."""

        return self.block

    def validate_transaction(self, tx, current_transactions=[]):
        """Validate a transaction against the current status of the database."""

        transaction = tx

        # CLEANUP: The conditional below checks for transaction in dict format.
        # It would be better to only have a single format for the transaction
        # throught the code base.
        if isinstance(transaction, dict):
            try:
                transaction = Transaction.from_dict(tx)
            except SchemaValidationError as e:
                logger.warning('Invalid transaction schema: %s', e.__cause__.message)
                return False
            except ValidationError as e:
                logger.warning('Invalid transaction (%s): %s', type(e).__name__, e)
                return False
        return transaction

    def is_valid_transaction(self, tx, current_transactions=[]):
        # NOTE: the function returns the Transaction object in case
        # the transaction is valid
        try:
            return self.validate_transaction(tx, current_transactions)
        except ValidationError as e:
            logger.warning('Invalid transaction (%s): %s', type(e).__name__, e)
            return False
    
    def get_model_output(self, tx):
        # the function returns the output of the Transation object in 
        # case the input is valid and model works properly
        try:
            input_from_transaction =  tx['input']
            return self.keras_model.get_model_output(input_from_transaction)
        except:
            logger.warning('Invalid input supplied to model')
            return -1 # Negative number denotes invalid output


Block = namedtuple('Block', ('app_hash', 'height', 'transactions'))