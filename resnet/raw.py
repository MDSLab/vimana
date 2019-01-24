from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np
import struct


def load_image(file_name):
    img_path = "../data/"+file_name

    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

def encode(input_value, output):
    return struct.pack('l%sf' %input_value.size,output, *input_value.flatten('F'))

def decode(raw,input_size=784):
    decoded=struct.unpack('l%sf'%input_size,raw)
    output = decoded[0]
    input_value = decoded[1:]
    input_value = np.array(input_value)
    input_value = input_value.reshape(224,224,3,order='F').astype(np.float32)
    input_value = input_value.reshape((1,)+input_value.shape)
    return input_value,output


inp = load_image("k.jpg")
print(inp.shape)
enc = encode(inp,543)

inpx,outx = decode(enc,inp.size)
print(outx, inpx.shape)

print(np.array_equal(inp,inpx))



print()
print(enc.hex())


