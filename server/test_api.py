from __future__ import print_function
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
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input

def api_call(file_name):
    K.clear_session()
    model = load_model('tendermint/model.h5')

    img_path = "data/"+file_name

    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    val = model.predict(x)
    print(val[0].argmax(axis=0))
    return val[0].argmax(axis=0)

def get_result(file_name):
    K.clear_session()
    model = load_model('tendermint/model.h5')
    pic = Image.open(file_name)
    Pic = np.array(pic)
    x = Pic.reshape((1,)+Pic.shape+(1,))
    val = model.predict(x)
    print(val[0].argmax(axis=0))
    return val[0].argmax(axis=0)