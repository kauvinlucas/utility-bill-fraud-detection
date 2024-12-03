from code.utils.image_transform import find_best_contours, four_point_transform

from io import BytesIO

import numpy as np
import tensorflow as tf
from PIL import Image
import cv2
import imutils

model = None


def load_model():
    model = tf.keras.models.load_model('model/model.keras')
    print("Model loaded")
    return model


def predict(image: Image.Image):
    global model
    if model is None:
        model = load_model()

    new_size = (1024, 500)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    ratio = image.shape[0] / 1000.0
    orig = image.copy()
    image = imutils.resize(image, height = 1000)
    screenCnt, output_image, gray = find_best_contours(image)
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    tranformed_img = Image.fromarray(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
    if warped.shape[0] > warped.shape[1]:
            tranformed_img = tranformed_img.rotate(-90, Image.NEAREST, expand = 1)
    tranformed_img = tranformed_img.resize(new_size)
    image_array  = tf.keras.utils.img_to_array(tranformed_img)
    image_array = tf.expand_dims(image_array, 0) # Create a batch
    predictions = model.predict(image_array)
    score = tf.nn.softmax(predictions[0])
    class_names = ['fraud', 'not-fraud']
    prediction_class = class_names[np.argmax(score)]
    confidence_score = 100 * np.max(score)
    return prediction_class, confidence_score


def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image