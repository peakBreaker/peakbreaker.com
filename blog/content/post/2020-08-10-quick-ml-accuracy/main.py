#!/usr/bin/env python


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def train():
    # Model / data parameters
    num_classes = 10
    input_shape = (28, 28, 1)

    # the data, split between train and test sets
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    # Scale images to the [0, 1] range
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255
    # Make sure images have shape (28, 28, 1)
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    print("x_train shape:", x_train.shape)
    print(x_train.shape[0], "train samples")
    print(x_test.shape[0], "test samples")


    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)



    model = keras.Sequential(
        [
            keras.Input(shape=input_shape),
            layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation="softmax"),
        ]
    )

    model.summary()


    def e_cb(epoch, logs):
        import json
        with open('train_logs.json', 'a') as l:
            data =json.dumps({'epoch': epoch, **logs})  
            l.write(data + '\n')

    my_callbacks = [
        tf.keras.callbacks.LambdaCallback(
            on_epoch_end=e_cb
            )
        ]

    batch_size = 512
    epochs = 10

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1, callbacks=my_callbacks)

    return model

def extract_logs():
    with open('train_logs.json') as l:
        df = pd.read_json(l, lines=True)
    print(df.head())
    return df

def plot_loss_acc(df):
    plt.plot(df['loss'], label='loss')
    plt.plot(df['accuracy'], label='accuracy')
    plt.legend()
    plt.xlabel('epoch')
    plt.title('Plotting accuracy vs loss for simple CNN on MNIST')
    plt.show()


if __name__ == '__main__':
    df = extract_logs()
    plot_loss_acc(df)
