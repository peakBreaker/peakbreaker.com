---
title: "Tensorflow and language"
date: 2020-10-13
description: Micropost on working with text in Tensorflow
titleWrap: wrap
enableSidebar: false
enableToc: false
---

## Messy data

Part of the magic of deep learning is turning unstructured data into structured
data which has much more applicable value.  Text is another source of
unstructured data, which we can apply tensorflow to to do our magic.

### Preprocessing

- Use the `tensorflow.keras.preprocessing.text.Tokenizer` to turn words into
tokens. `tokenizer = Tokenizer(num_words=100)` & `tokenizer.fit_on_texts(sentences)`
- Use `tokenizer.texts_to_sequences()` to turn the texts to sequences
- We use padding to get a uniform size `tensorflow.keras.preprocessing.sequence.pad_sequences`
  where we use the `maxlen` param to set the sequence max length
- use `.word_index` to get the owrd indices
- Use `oov_token='str'` to set an out of vocab token
- Use `padding='post'` to get padding at the end of the sequences instead

### Word embeddings

Use the tokenized sentences from the preprocssing step and feed it into a keras
sequential model using and Embedding layer as the first step of the model

```python
model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dimensions, input_length=maxlen),
    # ... Add flatten and dense layers below
])
```

Using the tokenized text and labels, the embedding layer will sort of become a lookup
table for words which maps to a learened vector.  By then running the model
over the text, we can create embeddings for our text - one vector per word.
afterwards by flattening and adding Dense layers, we may get a model which can
get some predictive ability out of the text.

If you want to pull the embeddings out:

```python
e = model.layers[0]
weights = e.get_weights()[0]


with open('vecs.tsv', 'w', encoding='utf-8') as out_v, out_m = io.open('meta.tsv', 'w', encoding='utf-8'):
  for word_num in range(1, vocab_size):
    word = reverse_word_index[word_num]
    embeddings = weights[word_num]
    out_m.write(word + "\n")
    out_v.write('\t'.join([str(x) for x in embeddings]) + "\n")
```

May then upload the data to the [Tensorflow Embedding Projector](https://projector.tensorflow.org/) for fun and profit


TL;DR:

0. Remove stopwords
1. Encode the text data using a tokenizer
2. Use a DNN model with an initial embedding layer

### Recurrent Neural Nets

Simple DNNs on Embeddings doesnt carry any sentence context. To solve this, we
may use a RNN.

```python
tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
```

A Convoluation may work aswell:

```python
tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
tf.keras.layers.Conv1D(128, 5, activation='relu'),
tf.keras.layers.GlobalMaxPooling1D(),
```
