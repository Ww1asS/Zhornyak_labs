import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Dense, SimpleRNN
from tensorflow.keras.datasets import imdb
from tensorflow.keras import utils
from tensorflow.keras.preprocessing.sequence import pad_sequences
from plot_keras_history import show_history, plot_history

max_words = 10000
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=10000)
maxlen = 200
x_train = pad_sequences(x_train, maxlen=maxlen)
x_test = pad_sequences(x_test, maxlen=maxlen)

model = Sequential([
    Embedding(max_words,2,input_length=maxlen),
    SimpleRNN(16),
    Dense(1,activation='sigmoid')
])

model.compile(optimizer="rmsprop",
              loss='binary_crossentropy',
              metrics=['accuracy'])

print(model.summary())

his = model.fit(x_train,
                    y_train,
                    epochs=10,
                    batch_size=128,
                    validation_split=0.1)

show_history(his)
plot_history(his, path="standard.png")
plt.close()



