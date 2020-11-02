---
title: "Tensorflow Transfer Learning"
date: 2020-10-14
description: Micropost on transfer learning with tensorflow
titleWrap: wrap
enableSidebar: false
enableToc: false
---

## Transfer learning

We can train our own neural nets, but we might not get great performance, or
overfit, due to our limited datasets. A better approach for many applications
may be to use transfer learning in order to adapt an existing model which is
trained on humongous datasets by some of the smartest people out there spending
loads of time on this task.  This is known as Transfer Learning, and in 
Tensorflow it is real simple.

### Overview

1. Get the pre trained model, somehow. Keras has some in the `applications`
   module
2. for loop over pre_model.layers and set layers to `layer.trainable = False`
3. Get the layer you want to feed into your new top layers
   `last_layer = pre_model.get_layer('mixed7')`
4. Start appending new layers `x = tf.keras.layers.Flatten()(last_layer.output)`
5. Instantiate the new model `model = tf.keras.Model(pre_model.input, x)`
6. Run the regular compile, fit etc to the new datasets

There is a decent chance the model will gradually overfit over the epochs.
A good way to mitigate this is to add a dropout layer in the new top.

### Example

```python

# Create the base model from the pre-trained model MobileNet V2
IMG_SHAPE = IMG_SIZE + (3,)

# 1. Get the pre trained model
base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet')

# 2. Set pre trained model to not train
base_model.trainable = False
# or for layer in base_model.layers:
##  layer.trainable = False

# 3. Get the last layer (use base_model.summary() to inspect)
last_layer = base_model.get_layer('out_relu (ReLU)')

# 4. Append new layers
x = tf.keras.layers.Flatten()(last_layer.output)
x = tf.keras.layers.Dropout(0.2)(x)
x = tf.keras.layers.Dense(1024, activation='relu')(x)
prediction_layer = tf.keras.layers.Dense(1, activation='sigmoid')(x)

# 5. Instantiate model
model = tf.keras.Model(inputs=base_model.inputs, outputs=prediction_layer)

# 6. Compile, fit, data etc
base_learning_rate = 0.0001
model.compile(optimizer=tf.keras.optimizers.Adam(lr=base_learning_rate),
              loss=tf.keras.losses.BinaryCrossentropy(),
              metrics=['accuracy'])


_URL = 'https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip'
path_to_zip = tf.keras.utils.get_file('cats_and_dogs.zip', origin=_URL, extract=True)
PATH = os.path.join(os.path.dirname(path_to_zip), 'cats_and_dogs_filtered')

train_dir = os.path.join(PATH, 'train')
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# All images will be rescaled by 1./255.
train_datagen = ImageDataGenerator(
      rescale=1./255,
      rotation_range=40,
      width_shift_range=0.2,
      height_shift_range=0.2,
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True,
      fill_mode='nearest',
      validation_split=0.2)


# --------------------
# Flow training images in batches of 20 using train_datagen generator
# --------------------
train_generator = train_datagen.flow_from_directory(train_dir,
                                                    batch_size=BATCH_SIZE,
                                                    class_mode='binary',
                                                    target_size=IMG_SIZE,
                                                    subset='training')

validation_generator = train_datagen.flow_from_directory(train_dir,
                                                    batch_size=BATCH_SIZE,
                                                    class_mode='binary',
                                                    target_size=IMG_SIZE,
                                                    subset='validation')


history = model.fit(train_generator,
                    validation_data=validation_generator,
                    epochs=3,
                    steps_per_epoch=train_generator.samples // BATCH_SIZE, 
                    verbose=2)
```
