from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect,Http404

from .test_api import api_call
import numpy as np
import requests
from PIL import Image
import struct
import json

from shutil import move, copyfile
import os

from .models import MLModel
from .forms import MLModelForm

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
    result = api_call(input_file)
    print(input_file)
    print("--------RESULT-------------")
    print(result)
    return HttpResponse(result)

def commit(request):
    input_file = request.POST.get('file')
    input_value = Image.open(input_file)
    input_value = np.array(input_value)
    # output = api_call(input_file)
    output = 1
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
