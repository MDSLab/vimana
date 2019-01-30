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
from utils import prefix_key, decode_transaction, encode_output

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
        """

        transaction = decode_transaction(tx)
        # calculate hash of the input.
        key = self.state.get_transaction_hash(transaction)

        # get model output
        value = self.state.get_model_output(transaction)

        logger.info("Transaction recived %s = %s", key, value)

        self.state.db.set(prefix_key(key), value)
        self.state.size += 1

        logger.info("Wow! Transaction delivered succesfully 😍")
        return ResponseDeliverTx(code=CodeTypeOk, data=encode_output(value))

    def check_tx(self, tx):
        return ResponseCheckTx(code=CodeTypeOk)

    def commit(self):
        byte_length = max(ceil(self.state.size.bit_length() / 8), 1)
        app_hash = self.state.size.to_bytes(byte_length, byteorder='big')
        self.state.app_hash = app_hash
        self.state.height += 1
        self.state.save()
        logger.info("Yaasss! Transaction commit succesfully 🦄")
        return ResponseCommit(data=app_hash)

    def query(self, req):
        key = self.state.get_transaction_hash(req.data)
        value = self.state.db.get(prefix_key(key))
        return ResponseQuery(code=CodeTypeOk, value=value)

