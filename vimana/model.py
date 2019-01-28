import sys
import os
import logging

import numpy as np
import keras
from keras.models import load_model
from keras import backend as K

from PIL import Image
 
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
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
            logger.info('Model loaded succesfully (%s)', self.model.summary())
        except Exception as e:
            logger.warning('Invalid model (%s): %s', type(e).__name__, e)

    # def test_model(self):
        # logger.info("Testing model")
        # script_dir = os.path.dirname(__file__)
        # rel_path = "8.png"
        # abs_file_path = os.path.join(script_dir, rel_path)
        # logger.info("wait why doesnt this work")
        # pic = Image.open(abs_file_path)
        # Pic = np.array(pic)
        # logger.info("wtf")
        # x = Pic.reshape((1,)+Pic.shape+(1,))
        # logger.info("loaded images")
    #     output = self.model.predict(input_value)
    #     logger.info("output recived")
    #     logger.info(output)
    #     return True

    def get_model_output(self, input_value):
        """Input value is a numpy array in the form of a list and it is 
        to be converted to numpy array in the dimensions of the image

        returns output as an integer 
        Only for classification, hence assuming outputs to be only integers
        """
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

        input_value = np.asarray(input_value)

        logger.info(input_value.shape)
        logger.info(type(input_value))

        logger.info("Testing model")
        script_dir = os.path.dirname(__file__)
        rel_path = "8.png"
        abs_file_path = os.path.join(script_dir, rel_path)
        logger.info("wait why doesnt this work")
        pic = Image.open(abs_file_path)
        Pic = np.array(pic)
        logger.info("wtf")
        x = Pic.reshape((1,)+Pic.shape+(1,))
        logger.info("loaded images")

        ouput = model.predict(x)
        logger.info(output)

        # try:
        #     ouput = self.model.predict(input_value)
        # except Exception as e:
        #     logger.warning('Invalid Output (%s): %s', type(e).__name__, e)
        
        # output[0].argmax(axis=0) returns the value of output
        # as an integer
        return output[0].argmax(axis=0)