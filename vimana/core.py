""" Bridge between Vimana and Tendermint 

This file exposes Vimana transaction 
logic to Tendermint Core
"""

import logging
import sys
import os

from math import ceil
from abci import (
    ABCIServer,
    BaseApplication,
    ResponseInfo,
    ResponseInitChain,
    ResponseCheckTx, ResponseDeliverTx,
    ResponseQuery,
    ResponseCommit,
    CodeTypeOk,
)

from state import State
from umm import get_model
from utils import (
    prefix_key,
    decode_transaction,
    encode_output,
    encode_output_str,
    prefix_model,
    get_transaction_method
)

method_query = 'query'
method_upload = 'model_upload'
method_activate = 'model_activate'
method_list = (method_upload, method_activate, method_query)

logging.basicConfig(level=os.environ.get("LOGLEVEL", "NOTSET"))
logger = logging.getLogger(__name__)


class App(BaseApplication):

    def __init__(self):
        self.state = State.load_state()

    def info(self, req):
        """
        Since this will always respond with height=0, Tendermint
        will resync this app from the begining
        """
        r = ResponseInfo()
        r.version = "1.0"
        r.last_block_height = self.state.height
        r.last_block_app_hash = b''
        return r

    def deliver_tx(self, tx):
        """Validate the transaction before mutating the state.

        Args:
            raw_tx: a raw string (in bytes) transaction.
        Returns: output to be send to the node in string after encoding.
        """
        transaction = decode_transaction(tx)
        logger.debug(transaction)

        method = get_transaction_method(transaction)

        if not method or method not in method_list:
            raise ValueError('Mode must be one of the following {}.'
                             .format(', '.join(method_list)))

        # UPDATE DOCS: -1 is an indication of no response.
        response_encoded = -1

        if(method == method_query):
            # calculate hash of the input.
            key = self.state.get_transaction_hash(transaction, method_query)

            # get model output
            value = self.state.get_model_output(transaction)

            logger.info("✅ Transaction recived %s = %s", key, value)

            self.state.db.set(prefix_key(key), value)
            self.state.size += 1

            response_encoded = encode_output(value)

        elif(method == method_upload):
            """name, hash and url from where to be downloaded
            """

            logger.info(method + "📦!!")
            # get the hash key of the model from the tx
            model_name, key, url_of_model = self.state.get_transaction_hash(
                transaction, method_upload)

            # no need to check if model exists already, tendermint does by default

            # get the relative location of the model inside the Model folder, this part downloads the model.
            location = get_model(model_name, key, url_of_model)

            logger.debug("Transaction recived model of %s hash 🛳", key)

            self.state.db.set(prefix_model(key), location)
            self.state.size += 1

            response_encoded = encode_output_str(location)
            logger.info(response_encoded)

        logger.info("😍 Wow! Transaction delivered succesfully ")

        return ResponseDeliverTx(code=CodeTypeOk, data=response_encoded)

    def check_tx(self, tx):
        return ResponseCheckTx(code=CodeTypeOk)

    def commit(self):
        byte_length = max(ceil(self.state.size.bit_length() / 8), 1)
        app_hash = self.state.size.to_bytes(byte_length, byteorder='big')
        self.state.app_hash = app_hash
        self.state.height += 1
        self.state.save()
        logger.info("🦄 Yaasss! Transaction commit succesfully ")
        return ResponseCommit(data=app_hash)

    def query(self, req):
        # TODO is not fully implemented!
        key = self.state.get_transaction_hash(req.data)
        value = self.state.db.get(prefix_key(key))
        logger.info("key %s returned %s", key, value)
        return ResponseQuery(code=CodeTypeOk, value=value)
