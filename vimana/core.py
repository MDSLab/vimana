""" Bridge between Vimana and Tendermint 

This file exposes Vimana transaction 
logic to Tendermint Core
"""

# Thank you BigchianDB https://github.com/bigchaindb/bigchaindb
# Thank you py-abci https://github.com/davebryson/py-abci

import logging
import sys


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

# from vimana import Vimana
from tendermint_utils import (decode_transaction,
                                         calculate_hash)
from lib import Block


CodeTypeOk = 0
CodeTypeError = 1
logger = logging.getLogger(__name__)


class App(BaseApplication):

    def info(self, request):
        """
        Since this will always respond with height=0, Tendermint
        will resync this app from the begining
        """
        r = ResponseInfo()
        r.version = "1.0"
        r.last_block_height = 0
        r.last_block_app_hash = b''
        return r

    def __init__(self, vimana=None):
        self.vimana = vimana or Vimana()
        self.block_txn_ids = []
        self.block_txn_hash = ''
        self.block_transactions = []
        self.validators = None
        self.new_height = None

    def init_chain(self, genesis):
        """Set initial state on first run"""

        app_hash = ''
        height = 0
        abci_chain_height = 0

        block = Block(app_hash=app_hash, height=height, transactions=[])

        self.vimana.store_block(block._asdict())
        self.chain = {'height': abci_chain_height, 'is_synced': True,
                      'chain_id': genesis.chain_id}
        return ResponseInitChain()

    def check_tx(self, raw_transaction):
        """Validate the transaction before entry into
        the mempool.

        Args:
            raw_tx: a raw string (in bytes) transaction.
        """

        logger.debug('check_tx: %s', raw_transaction)
        transaction = decode_transaction(raw_transaction)
        if self.vimana.is_valid_transaction(transaction):
            logger.debug('check_tx: VALID')
            return ResponseCheckTx(code=CodeTypeOk)
        else:
            logger.debug('check_tx: INVALID')
            return ResponseCheckTx(code=CodeTypeError)

    def begin_block(self, req_begin_block):
        """Initialize list of transaction.
        Args:
            req_begin_block: block object which contains block header
            and block hash.
        """

        logger.debug('BEGIN BLOCK, height:%s, num_txs:%s',
                     req_begin_block.header.height + chain_shift,
                     req_begin_block.header.num_txs)

        self.block_txn_ids = []
        self.block_transactions = []
        return ResponseBeginBlock()

    def deliver_tx(self, raw_transaction):
        """Validate the transaction before mutating the state.

        Args:
            raw_tx: a raw string (in bytes) transaction.
        """

        self.abort_if_abci_chain_is_not_synced()

        logger.debug('deliver_tx: %s', raw_transaction)
        transaction = self.vimana.is_valid_transaction(
            decode_transaction(raw_transaction), self.block_transactions)

        if not transaction:
            logger.debug('deliver_tx: INVALID')
            return ResponseDeliverTx(code=CodeTypeError)
        else:
            logger.debug('storing tx')
            self.block_txn_ids.append(transaction.id)
            self.block_transactions.append(transaction)
            return ResponseDeliverTx(code=CodeTypeOk)

    def end_block(self, request_end_block):
        """Calculate block hash using transaction ids and previous block
        hash to be stored in the next block.

        Args:
            height (int): new height of the chain.
        """

        height = request_end_block.height 
        self.new_height = height

        block_txn_hash = calculate_hash(self.block_txn_ids)
        block = self.vimana.get_latest_block()

        if self.block_txn_ids:
            self.block_txn_hash = calculate_hash([block['app_hash'], block_txn_hash])
        else:
            self.block_txn_hash = block['app_hash']

        return ResponseEndBlock()

    def commit(self):
        """Store the new height and along with block hash."""

        data = self.block_txn_hash.encode('utf-8')
        return ResponseCommit(data=data)

