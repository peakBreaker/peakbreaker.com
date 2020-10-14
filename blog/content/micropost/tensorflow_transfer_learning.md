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
