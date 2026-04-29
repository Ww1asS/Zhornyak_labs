import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical

(img_train, res_train), (img_test, res_test) = mnist.load_data()
img_train = img_train / 255.0
img_test = img_test / 255.0

res_train = to_categorical(res_train)
res_test = to_categorical(res_test)

img_test = tf.image.resize(img_test[..., np.newaxis], (14,14)) [..., 0]
img_train = tf.image.resize(img_train[..., np.newaxis], (14,14)) [..., 0]

model = Sequential([
    Flatten(input_shape=(14,14)),
    Dense(280, activation='relu'),
    Dense(10, activation='softmax')
])

model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
              )

model.fit(
          img_train,
          res_train,
          epochs=10,
          validation_data =(img_test, res_test)
          )

model.save("model.keras")