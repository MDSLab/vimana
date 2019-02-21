from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect,Http404

from .test_api import api_call
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

try:
    from hashlib import sha3_256
except ImportError:
    from sha3 import sha3_256


from .models import MLModel
from .forms import MLModelForm
 

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

mode_commit = 'broadcast_tx_commit'
mode_list = ('broadcast_tx_async','broadcast_tx_sync', mode_commit)

def encode(input_value, output):
    return struct.pack('l%si' %input_value.size,output, *input_value.flatten('F'))

def main(request,id=None):
    mlmodel = MLModel.objects.all()
    active = MLModel.objects.filter(active=True)
    print(active)
    context={
        "model": mlmodel,
        "active": active,
    }
    return render(request,"main.html",context)

def model_create(request):
	form = MLModelForm(request.POST or None , request.FILES)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		return HttpResponseRedirect("/")
	context={
    "form":form,
    }
	return render(request,"form.html",context)

def update_active(request, id=None):
    
    active = MLModel.objects.filter(active=True)
    for node in active:
        node.active = False
        node.save(update_fields=["active"])

    instance = get_object_or_404(MLModel,id=id)
    instance.active = True
    instance.save(update_fields=["active"])

    
    path = os.path.relpath(instance.file.path)
    copyfile(path, 'tendermint/model.h5')
    return HttpResponseRedirect("/")

def test(request):
    input_file  = request.POST.get('file')
    K.clear_session()
    model = load_model('tmserver/model.h5')
     
    time_taken = []
    for i in range(1,101):
        start_time = time.time()
        input_value = Image.open("data/"+"img_"+str(i)+".jpg")
        input_value = np.array(input_value)

        input_value = input_value.reshape((1,)+input_value.shape+(1,))

        result = model.predict(input_value)

        end_time = time.time()
        print(end_time-start_time)
        time_taken.append(end_time-start_time)
    
    print("Average time taken")
    print(sum(time_taken)/float(len(time_taken)))
    
    print("Writing to CSV")
    write_to_csv(time_taken, "mnist_without_tendermint")

    return HttpResponse(result)

def encode_transaction(value):
    """Encode a transaction (dict) to Base64."""

    return base64.b64encode(json.dumps(value).encode('utf8')).decode('utf8')

def post_transaction( transaction, mode):
    """Submit a valid transaction to the mempool."""
    if not mode or mode not in mode_list:
        raise ValidationError('Mode must be one of the following {}.'
                                .format(', '.join(mode_list)))

    tx_dict = transaction
    
    tendermint_host = 'localhost'
    tendermint_port = 26657
    endpoint = 'http://{}:{}/'.format(tendermint_host, tendermint_port)

    payload = {
        'method': mode,
        'jsonrpc': '2.0',
        'params': [encode_transaction(tx_dict)],
        'id': str(uuid4())
    }
    # TODO: handle connection errors!
    # print(payload)
    return requests.post(endpoint, json=payload)

def write_transaction(transaction, mode):
    # This method offers backward compatibility with the Web API.
    """Submit a valid transaction to the mempool."""
    response = post_transaction(transaction, mode)
    return _process_post_response(response.json(), mode)

def _query_transaction( transaction):
    """Submit a valid transaction to the mempool."""
    # if not mode or mode not in mode_list:
    #     raise ValidationError('Mode must be one of the following {}.'
    #                             .format(', '.join(mode_list)))

    tx_dict = transaction
    
    tendermint_host = 'localhost'
    tendermint_port = 26657
    endpoint = 'http://{}:{}/'.format(tendermint_host, tendermint_port)

    payload = {
        "method": "abci_query",
        "jsonrpc": "2.0",
        "params":[None, encode_transaction(tx_dict), None, None],
        "id": str(uuid4())
    }
    # TODO: handle connection errors!
    print(payload)
    return requests.post(endpoint, json=payload)

def query_transaction(transaction):
    response = _query_transaction(transaction)
    return _process_post_response(response.json(), 'abci_query')

def _process_post_response(response, mode):
    # print(response)

    error = response.get('error')
    if error:
        status_code = 500
        message = error.get('message', 'Internal Error')
        data = error.get('data', '')

        if 'Tx already exists in cache' in data:
            status_code = 400

        return (status_code, message + ' - ' + data)

    result = response['result']
    if mode == mode_commit:
        check_tx_code = result.get('check_tx', {}).get('code', 0)
        deliver_tx_code = result.get('deliver_tx', {}).get('code', 0)
        error_code = check_tx_code or deliver_tx_code
    else:
        error_code = result.get('code', 0)

    if error_code:
        return (500, 'Transaction validation failed')
    # todo convert output to json
    return decode_output(result['deliver_tx']['data'])

def decode_output(value):
    value_in_base64 = base64.b64decode(value)
    return int.from_bytes(value_in_base64, byteorder='big')

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def write_to_csv(time_list, name):
    with open(str(name) + ".csv", 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(time_list)

def commit(request):
    input_file = request.POST.get('file')
    input_value = Image.open("data/" + input_file)
    input_value = np.array(input_value)

    input_value = input_value.reshape((1,)+input_value.shape+(1,))

    transaction = {
        'input': input_value
    }

    # Since numpy is not json serializable
    # https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
    transaction = json.dumps(transaction, cls=NumpyEncoder)
    
    result = write_transaction(transaction, 'broadcast_tx_sync')

    return HttpResponse(result)

def query(request):
    pass
    # input_file = request.POST.get('file')
    # input_value = Image.open("data/" + input_file)
    # input_value = np.array(input_value)

    # input_value = input_value.reshape((1,)+input_value.shape+(1,))

    # transaction ={
    #     'input': input_value
    # }

    # # Since numpy is not json serializable
    # # https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
    # transaction = json.dumps(transaction, cls=NumpyEncoder)

    # result = query_transaction(transaction)

    # return HttpResponse(result)

