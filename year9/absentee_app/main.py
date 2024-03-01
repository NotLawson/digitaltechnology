import tensorflow as tf
import keras
import numpy as np
import base64 as b64
from io import BytesIO
import json
from PIL import Image, ImageOps
from flask import Flask, render_template, request
tf.keras = keras

MODEL = tf.keras.models.load_model("model/model.h5", compile=False)


def predict_image(image):
    # Load the labels
    class_names = open("model/labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = MODEL.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return class_name[2:], confidence_score

Image.open

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/subimage", methods = ["POST"])
def image():
    data = request.data.removeprefix(b'data:image/jpeg;base64,')
    with open("image.png", "wb") as fh:
        fh.write(b64.decodebytes(data))
    img = Image.open("image.png")
    class_str, _ = predict_image(img)
    per = round(_, 2)
    per = int(per * 100)
    return class_str

@app.route("/mark" ,methods = ["POST"])
def mark():
    name = request.form.get("name")
    reason = request.form.get("reason")
    return render_template("redirect.html", name = name, reason = reason)


if __name__ == "__main__":
    app.run("0.0.0.0", 8080, debug=True)

