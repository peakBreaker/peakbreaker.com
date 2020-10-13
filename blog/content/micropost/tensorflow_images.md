---
title: "Tensorflow and images"
date: 2020-10-13
description: Micropost on working with images in Tensorflow
titleWrap: wrap
enableSidebar: false
enableToc: false
---

## Aahhh, Tensorflow

So this is a simple python script which is useful for me to add logging to my application quickly. Just add this to a file and import it to get the right format.  Add additional logic as needed.  The formatting here works well with stackdriver logging.


### Inspecting the raw data

```python
%matplotlib inline

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# Parameters for our graph; we'll output images in a 4x4 configuration
nrows = 4
ncols = 4

pic_index = 0 # Index for iterating over images

# Set up matplotlib fig, and size it to fit 4x4 pics
fig = plt.gcf()
fig.set_size_inches(ncols*4, nrows*4)

pic_index+=8

next_cat_pix = [os.path.join(train_cats_dir, fname) 
                for fname in train_cat_fnames[ pic_index-8:pic_index] 
               ]

next_dog_pix = [os.path.join(train_dogs_dir, fname) 
                for fname in train_dog_fnames[ pic_index-8:pic_index]
               ]

for i, img_path in enumerate(next_cat_pix+next_dog_pix):
  # Set up subplot; subplot indices start at 1
  sp = plt.subplot(nrows, ncols, i + 1)
  sp.axis('Off') # Don't show axes (or gridlines)

  img = mpimg.imread(img_path)
  plt.imshow(img)

plt.show()
```

### Generator for retreiving pictures

Tensorflow has the handy ImageDataGenerator for creating a generator which can
retreive images from a directory for testing and validation.

```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# All images will be rescaled by 1./255.
train_datagen = ImageDataGenerator( rescale = 1.0/255. )

# --------------------
# Flow training images in batches of 20 using train_datagen generator
# --------------------
train_generator = train_datagen.flow_from_directory(train_dir,
                                                    batch_size=20,
                                                    class_mode='binary',
                                                    target_size=(150, 150))
```

### A simple convolutional model

Create a sequential model with 2^4+n (16,32,64) convolutional layers. Use (3,3)
kernels. Add max pooling (2,2) after the convolutional layers. End the NN with
a Flatten layer and Dense layer, aswell as the output layer (using sigmoid or
softmax).

For loss, you may use `binary_crossentropy` or `categorical_crossentropy`
For optimizer, use `RMSprop` or `adam`
