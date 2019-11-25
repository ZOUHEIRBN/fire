import cv2
import numpy as np
import os

from keras.backend import set_session, get_session
from keras.models import model_from_json
import tensorflow as tf


def auc(y_true, y_pred):
    ac = tf.metrics.auc(y_true, y_pred)[1]
    return ac

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print(ROOT_DIR)
json_file = open(os.path.join(ROOT_DIR, 'model.json'), 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(os.path.join(ROOT_DIR, 'model.h5'))
print("Loaded model from disk")


graph = tf.get_default_graph()
session = tf.Session()
init = tf.global_variables_initializer()
session.run(init)

LABELS = ["none", "Fire"]


def prepare(img, width=96, height=96):
    img = cv2.resize(img, (width, height))
    img = np.expand_dims(img, 0)
    return img


def split(img, factor_size=1., width=96, height=96):
    w, h, p = img.shape
    wd = int(width * factor_size)
    hi = int(height * factor_size)
    splist = [prepare(img, width=width, height=height)]
    for x in range(wd, w, wd):
        for y in range(hi, h, hi):
            sp = img[x - wd:x, y - hi:y]
            sp = prepare(sp, width=width, height=height)
            splist.append(sp)

    return splist


def predict(image_set):
    global graph
    global session
    with graph.as_default():
        set_session(session)
        preds = []
        for frame in image_set:
            imagesplits = split(frame, factor_size=2)
            frames = [{"name": "Capture", "frame": sp} for sp in imagesplits]

            for frame_data in frames:
                pred = loaded_model.predict(frame_data["frame"])
                pred = [np.round(p * 100, 2) for p in pred[0]]

                preds.append(pred)

        pred_avg = {}
        preds = np.array(preds).transpose()

        for i in range(len(preds)):
            mean = np.median(preds[i])
            pred_avg[LABELS[i]] = str(np.round(mean, 2))

        return pred_avg







