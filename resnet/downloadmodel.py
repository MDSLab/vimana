from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
import keras
import numpy as np

model = keras.applications.resnet50.ResNet50(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000)

model.save("model.h5")