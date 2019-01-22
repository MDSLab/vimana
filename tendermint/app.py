from __future__ import print_function
import struct
import abci.utils as util

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
import pickle
import os

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


INPUT_SHAPE=(28,28)

def encode(input_value, output):
    return struct.pack('l%si' %input_value.size,output, *input_value.flatten('F'))

def decode(raw,input_size=784):
    decoded=struct.unpack('l%si'%input_size,raw)
    output = decoded[0]
    input_value = decoded[1:]
    input_value = np.array(input_value)
    input_value = input_value.reshape(28,28,order='F').astype(np.uint8)
    return input_value,output

def get_result(input_value):
    K.clear_session()
    script_dir = os.path.dirname(__file__)
    rel_path = "model.h5"
    abs_file_path = os.path.join(script_dir, rel_path)
    model = load_model(abs_file_path)
    input_value = input_value.reshape((1,)+input_value.shape+(1,))
    val = model.predict(input_value)
    print(val[0].argmax(axis=0))
    return val[0].argmax(axis=0)

class Vimana(BaseApplication):

    def info(self, req) -> ResponseInfo:
        """
        Since this will always respond with height=0, Tendermint
        will resync this app from the begining
        """
        r = ResponseInfo()
        r.version = "1.0"
        r.last_block_height = 0
        r.last_block_app_hash = b''
        return r

    def init_chain(self, req) -> ResponseInitChain:
        """Set initial state on first run"""
        self.input_value = np.empty([28,28],dtype=np.uint8)
        self.output = 0
        # self.model_hash = 9b662cfdae5e209c43541fb329ec29ecff4b89404762aaf0b8c6ff1e50491b97
        self.last_block_height = 0
        return ResponseInitChain()

    def check_tx(self, tx) -> ResponseCheckTx:
        """
        Validate the Tx before entry into the mempool
        Checks the txs are submitted in order 1,2,3...
        If not an order, a non-zero code is returned and the tx
        will be dropped.
        """
        input_value, output = decode(tx)
        if not output == get_result(input_value):
            # respond with non-zero code
            return ResponseCheckTx(code=1)
        return ResponseCheckTx(code=CodeTypeOk, data=bytes(output))

    def deliver_tx(self, tx) -> ResponseDeliverTx:
        """Simply increment the state"""
        input_value, output = decode(tx)
        self.input_value = input_value
        self.output = output
        return ResponseDeliverTx(code=CodeTypeOk, data=bytes(output))

    def query(self, req) -> ResponseQuery:
        """Return the last tx count"""
        v = encode(self.input_value, self.output)
        return ResponseQuery(code=CodeTypeOk, value=v, height=self.last_block_height)

    def commit(self) -> ResponseCommit:
        """Return the current encode state value to tendermint"""
        hash = encode(self.input_value, self.output)
        return ResponseCommit(data=hash)


if __name__ == '__main__':
    # Create the app
    app = ABCIServer(app=WhiteElement())
    # Run it
    app.run()
