import tensorflow as tf
from keras.models import load_model
import tensorflow_hub as hub
from keras.src.utils import load_img, img_to_array
import numpy as np

SIZE = 224


def resize_image(img, label):
    img = tf.cast(img, tf.float32)
    img = tf.image.resize(img, (SIZE, SIZE))
    img = img / 255.0
    return img, label


def predict(image_path):
    img = load_img(image_path)
    img_array = img_to_array(img)
    img_resized, _ = resize_image(img_array, '_')
    img_expended = np.expand_dims(img_resized, axis=0)
    model = load_model('../neuron_network/my_model.h5',
                       custom_objects={'KerasLayer': hub.KerasLayer})
    prediction = model.predict(img_expended)[0][0]

    print(prediction)
    if prediction > 0.7:
        return 'собака!'
    elif prediction < 0.3:
        return 'кошка!'
    else:
        return 'сложно сказать что'
