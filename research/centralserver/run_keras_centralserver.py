from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import io
from model import KerasModel
import json

# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
model = None


@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = { "value" : None}
    if flask.request.method == "POST":
        tx = flask.request.json
        input_from_transaction = json.loads(tx)['input']
        output = model.get_model_output(input_from_transaction)
        data["value"] = int(output)

    return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
    	"please wait until server has fully started"))

    model = KerasModel()
    app.run()