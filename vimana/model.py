import sys
import os
import logging

import numpy as np
import keras
from keras.models import load_model
from keras import backend as K
 
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

# Define the location where the model file is
MODEL_LOCATION = "model.h5"


class KerasModel(object):

    def __init__(self):

        # clear keras session to prevent memory error
        K.clear_session()

        # load the model 
        script_dir = os.path.dirname(__file__)
        rel_path = MODEL_LOCATION
        abs_file_path = os.path.join(script_dir, rel_path)
        try:
            model = load_model(abs_file_path)
            logger.info('Model loaded succesfully (%s)', model.summary())
        except Exception as e:
            logger.warning('Invalid model (%s): %s', type(e).__name__, e)

    def get_model_output(self, input_value):
        """Input value is a numpy array in the dimensions of the image

        returns output as an integer 
        Only for classification, hence assuming outputs to be only integers
        """
        try:
            ouput = model.predict(input_value)
        except Exception as e:
            logger.warning('Invalid Output (%s): %s', type(e).__name__, e)
        
        # output[0].argmax(axis=0) returns the value of output
        # as an integer
        return output[0].argmax(axis=0)