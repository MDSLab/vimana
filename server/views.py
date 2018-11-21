from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect,Http404

from .test_api import api_call
import numpy as np
import requests
from PIL import Image
import struct
import json
def encode(input_value, output):
    return struct.pack('l%si' %input_value.size,output, *input_value.flatten('F'))

def main(request,id=None):

    context={
    }
    return render(request,"main.html",context)


def test(request):
    input_file  = request.POST.get('file')
    result = api_call(input_file)
    print(input_file)
    print("--------RESULT-------------")
    print(result)
    return HttpResponse(result)

def commit(request):
    input_file = request.POST.get('file')
    input_value = Image.open(input_file)
    input_value = np.array(input_value)
    output = api_call(input_file)
    raw = encode(input_value,output)
    raw_hex = raw.hex()
    print("Input image loaded ")
    # print(input_value)
    print("--Output generated is---")
    print(output)
    # print("------Raw Hex ------")
    # print(raw_hex)
    json_response = requests.get('http://localhost:26657/broadcast_tx_commit?tx=0x'+raw_hex)
    return HttpResponse(json_response)
