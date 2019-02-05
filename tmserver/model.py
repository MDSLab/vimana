import sys
import os
import logging

import numpy as np
import keras
from keras.models import load_model
from keras import backend as K
import tensorflow as tf

from PIL import Image
 
logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
logger = logging.getLogger(__name__)

# Define the location where the model file is
MODEL_LOCATION = "model.h5"


class KerasModel(object):

    def __init__(self):
        """ Keras Model should be a wrapper for all machine learning models
        using keras library for deep learning. 

        This connects with vimana, keras model is loaded from the 
        MODEL_LOCATION
        """

        # clear keras session to prevent memory error
        K.clear_session()

        # load the model 
        script_dir = os.path.dirname(__file__)
        rel_path = MODEL_LOCATION
        abs_file_path = os.path.join(script_dir, rel_path)
        try:
            self.model = load_model(abs_file_path)
            
            # https://github.com/keras-team/keras/issues/2397
            self.model._make_predict_function()
            self.graph = tf.get_default_graph()

            logger.info('Model loaded succesfully (%s)', self.model.summary())
        except Exception as e:
            logger.warning('Invalid model (%s): %s', type(e).__name__, e)

    def get_model_output(self, input_value):
        """Input value is a numpy array in the form of a list and it is 
        to be converted to numpy array in the dimensions of the image

        returns output as an integer 
        Only for classification, hence assuming outputs to be only integers
        """
        input_value = np.asarray(input_value)

        logger.debug("Input recived by model of shape")
        logger.debug(input_value.shape)

        try:
            with self.graph.as_default():
                output = self.model.predict(input_value)
        except Exception as e:
            logger.warning('Invalid Output (%s): %s', type(e).__name__, e)

        logger.debug("Predicted output : %i", output[0].argmax(axis=0))
        
        # output[0].argmax(axis=0) returns the value of output
        # as an integer
        return 1