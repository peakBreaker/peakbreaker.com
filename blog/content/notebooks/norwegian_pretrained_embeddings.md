---
title: "Pretrained Norwegian nlp embedding models"
date: 2020-11-14
description: getting dirty with fasttext and w2v
titleWrap: wrap
enableSidebar: false
enableToc: false
---

## FastText

**Download resources and deps**

First download the pretrained fasttext model from [fasttext](https://fasttext.cc/docs/en/crawl-vectors.html) in the appropriate language for our experiment. In this case Norwegian


```python
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
```


```python
! pip install fasttext &> /dev/null
```


```python
norwegian_model_f = 'cc.no.300.bin'
```


```python
import gzip
import shutil
with gzip.open(norwegian_model_f+'.gz', 'rb') as f_in:
    with open(norwegian_model_f, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
```


```python
import fasttext
ft = fasttext.load_model(norwegian_model_f)
```

    Warning : `load_model` does not return WordVectorModel or SupervisedModel any more, but a `FastText` object which is very similar.



```python
[n for n in ft.get_nearest_neighbors('konsulent', k=100) if 'konsulent' not in n[1].lower()]
```




    [(0.7269838452339172, 'rådgiver'),
     (0.6610698699951172, 'IT-rådgiver'),
     (0.629156231880188, 'prosjektleder'),
     (0.6253646016120911, 'VVS-rådgiver'),
     (0.6252682209014893, '-rådgiver'),
     (0.6225616931915283, 'HMSrådgiver')]




```python
help(ft.get_nearest_neighbors)
```

    Help on method get_nearest_neighbors in module fasttext.FastText:
    
    get_nearest_neighbors(word, k=10, on_unicode_error='strict') method of fasttext.FastText._FastText instance
    



```python
del(ft)
```

## Word2Vec

First download a pretrained norwegian model from [github](https://github.com/Kyubyong/wordvectors) and move it to the repo


```python
! mkdir -p w2v
```


```python
! mv /home/peakbreaker/Downloads/no.zip ./w2v/
```

    mv: cannot stat '/home/peakbreaker/Downloads/no.zip': No such file or directory



```python
! pip install gensim &> /dev/null
```


```python
from zipfile import ZipFile
norwegian_w2v_model_f = 'w2v/no.zip'
ZipFile(norwegian_w2v_model_f).extractall('w2v')
```


```python
import gensim
```


```python
model = gensim.models.Word2Vec.load('w2v/no.bin')
```


```python
model.most_similar('hallo')
```




    [('radioprogrammet', 0.5731750726699829),
     ('sommeråpent', 0.5661594271659851),
     ('nitimen', 0.5642672777175903),
     ('talkshowet', 0.5346325635910034),
     ('tv-programmet', 0.5236023664474487),
     ('ylvis', 0.5019408464431763),
     ('radioteatret', 0.49859005212783813),
     ('dagsrevyen', 0.4889247417449951),
     ('barne-tv', 0.48854684829711914),
     ('radioteateret', 0.48758113384246826)]




```python
model.most_similar('verden')
```




    [('europa', 0.6526151895523071),
     ('verdenen', 0.5795935392379761),
     ('kloden', 0.554469883441925),
     ('landet', 0.5417060852050781),
     ('norden', 0.4880366921424866),
     ('vest-europa', 0.4815964996814728),
     ('latin-amerika', 0.46273982524871826),
     ('universet', 0.45110243558883667),
     ('samfunnet', 0.4509172737598419),
     ('afrika', 0.45039165019989014)]




```python
model.most_similar_cosmul(positive=['konge', 'kvinne'], negative=['mann'])
```




    [('monark', 0.9270060658454895),
     ('dronning', 0.8959850668907166),
     ('fyrste', 0.8814278244972229),
     ('overkonge', 0.8673690557479858),
     ('tronarving', 0.8655897378921509),
     ('regent', 0.8644863367080688),
     ('hersker', 0.8569005131721497),
     ('farao', 0.8543179035186768),
     ('prinsesse', 0.8368269801139832),
     ('herskeren', 0.8366155624389648)]


