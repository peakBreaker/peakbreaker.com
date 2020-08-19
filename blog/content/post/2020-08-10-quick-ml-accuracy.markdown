---
categories: ['Data Science']
description: Short post on accuracy
featured_image: covers/notes.jpg
author: Anders
title: Measuring accuracy in classification problems
date: "2020-08-18"
layout: post
draft: false
series: ["Accuracy in ML"]
tags: ['ml', 'software', 'data']
---

## How far am I off?

This is just a quick post off my personal notes. It has been a while since Ive
written here, so welcome me back!

![From my notes](/images/posts/ml/anders_notes.jpg)

So a big part of creating a machine learning model for some application is to
figure out how well it is performing. We need to validate and check that the
model is generalizing to our problem, and we need to be able to compare models
against each other to choose the correct solution for our problem.  This is the
topic of accuracy in machine learning.

In this post, Ill be looking at **accuracy for classification problems**, and in
a later post Ill write about regression.

## Loss vs Accuracy

Something that confused me on this subject is that loss functions
and accuracy metrics are closely associated. They sometimes overlap, but the
general difference is this as far as I can tell:

- Loss functions is used by the model during training (on a per sample basis)
- Accuracy is used for our application to evaluate the model

**Loss functions** are what calculates the error of our model, or how far off a 
model prediction is from the truth. The Loss function is the function between a
models output and the target variable, which we use to train the model. For 
classification, common loss functions include LogLoss, CrossEntropy or 
HingeLoss - for classification problems.

![Loss vs accuracy](/images/posts/ml/loss_vs_acc.png)

I trained a simple MNIST CNN model and logged the loss and accuracy for each
epoch here.  As we can see, and expect, the loss falls, and the
accuracy improves over the epochs of training. The accuracy is however here
used to validate the model for our application purposes, and not for doing
gradient descent such as the loss is being used for.

On the other hand, to see how well the model is performing on new data - our
validation dataset perhaps - we might want to use the F1 score for accuracy. 
This depends on our application, and is much in the hands of the model 
developer.  It is also important in evaluating different models against
eachother. We will touch more on accuracy below, and some different accuracy 
metrics.

## Accuracy

To first get an understanding of the concepts, its important to look at
individual samples and how we define successful classification for them. To do
this, we place individual predictions in a confusion matrix.

// Confusion matrix

- True/False : Model successful classification
- Positive/Negative : Model prediction

So a True Positive (TP), would be the model flagging a positive prediction, and
being correct in its guess. This becomes a 2x2 matrix, where the predictions
are the column features, and the actual classes are the rows

|       | pT | pF |
| :---        |    :----:   |          ---: |
| P      | TP       | FN   |
| F   | FP        |  TN      |

Lets take a few examples.  Lets imagine we have a model predicting two classes
- one and zero `[0,1]` - and we feed it some data. The actual labels of the
  data are as follows:

`[0,0,1,1]`

And the model predicts:

`[0,1,0,1]`

This means we have the following CM:

|       | pT | pF |
| :---        |    :----:   |          ---: |
| P      | 1       | 1   |
| F   | 1        |  1      |

Or the data:

`[TN,FP,FN,TP]`

This holds true for binary classification problems. Doing multiclass problems
just means we need to segment the problem. e.g. ABC => TP_A, TP_B, TP_C, TN_A, etc.
Thus allowing us to calculate precision & recall etc for each label. We can
however plot out the CM for the multiclass problem the same way, here is an
example from the iris dataset from [scikit
learn](https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py):

![iris confusion matrix](/images/posts/ml/confusion_matrix.png)

So with this out of the way, imagine we want to run the model on a test dataset
and check how well it is doing!

### Flat Accuracy

This is the easiest accuracy to understand.  It is just how often the model is
correct.

`Number of correct predictions / Number of total predictions`

or `TP+TN / TP+TN+FP+FN`

Easy

### Precision & Recall

Precision is `TP / TP+FP` - Why do we care about this? It tells us how good the
model is when it flags the data as positive. For the application, this may be
very important, such as if youre detecting poisonous mushrooms.  You dont want
a model to tell you that the mushroom is fine, if it is actually is poisonous,
even if this means the model might flag some safe mushrooms to be poisonous.

The other side of the coin is recall. Recall is `TP / TP+FN` - which defines
how well the model is at calling out the instances of the class we care about.
A high recall is useful if we want to detect our class, but we dont care so
much about when we call out false positives.  So a model which is screening
lots of people for cancer should try to recall most or all of the cancer cases,
for further investigation.

It is up to the model developer here to define the threshold between precision
and recall based on the application, as they are often in tension. Often a good
derived metric from precision and recall is the harmonic mean of these metrics
- known as the **F1 Score**, which may be good to use in for example hyperparam
tuning.

### ROC / AUC

By tweaking the classification threshold, we can get an ROC curve by plotting
TP rate vs FP rate.

![ROC Curve](/images/posts/ml/simple_roc.png)

The area under this curve is the AUC, and may be used to evaluate how good
a model is in general. Great!

## Final thoughts

Building machine learning models is one thing, but just as important is to
understand the model, evaluate it continuously to know when it is time to
retrain our model, or to just see how well it is fitting to our application. It
is clearly important in explaining the model, and it is a core skill to even
building out a model.

My passion in ml lies not in building models themselves, but rather all the
systems and knowledge that lies around the model, often known as the MLOps, and
being able to evaluate model accuracy is one part of this.  I also believe that
this is the hard part of machine learning.


