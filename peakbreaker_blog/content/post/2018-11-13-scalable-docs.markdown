---
categories: Docs
layout: post
featured_image: covers/docs.png
author: Anders
tags: ['Sphinx', 'Python', 'Documentation', 'gh-pages', 'oauth', 'readthedocs', 'rtfd', 'heroku', 'cloud']
finished: true
date: "2018-11-13"
title: Scalable Documentation
---

# Documentation

In this entry, I am happy to be writing about something I have feelings
for and about.  Documentation is one of those core needs in the maslow pyramid
of technology, yet far too often overlooked.

![yo dawd documentation](http://www.quickmeme.com/img/fc/fc987e2549a985112129f76108984dcaa0b73bd240c0b6e15b12e53ac19e4991.jpg)

It sounds easy, right? Just write some documents on what youre doing. Wrong, 
that attitude does not scale. Unmaintained documentation is worse than no
documentation, and documentation accumulates the same technical dept as code,
thus it should be treated with atleast as much love.

In addition documentation means so many different things, so in order to have
any communication on this subject, we need to specify what documentation even
means.

## What is documentation

Documentation comes from the english word "Document" which means
a "representation of thought". Man, thats deep.

When you write, you write to different audiences. In my case here, Im writing to
someone called "no one" *(cry)*. You are also writing for different purposes,
In my case here, Im writing because I have a strange affiliation with
documentation.

**TL;DR on this chapter:** Documentation can roughly be divided in two, *Process
documentation* for the devs, engineers and whatnot which needs some level of
technical competence to read, and *User documentation* which is for those pesky users
who doesnt necessarily have years of experience with the technology you spend
your life building.

Lets go through some different types of docuementation for some examples:

**Code as Documentation:** When you craft code, your code should be clear enough 
to self document *what* it is doing. Comments in code should tell you *Why* the
code is doing whatever it is doing. Docstrings, those comments at the top of
files, classes, functions and whatever else, provide an idea of *usage*. We'll
get back to docstrings.

**README:** Provides instructions on running your project and setting up
a devenv. Pretty essential to any project.

**API Docs:** Guide and reference for how to use your API. Should absolutely be
provided if you want people to use your technology.

**Style guides:** Document which detemines the style guide and conventions for
whatever. For example, should variable names follow PascalCase, camelCase or
under_scores? Well theres a lot more to this, but it sets the conventions for
the technology development, so we can all follow the same standards, which is
very nice.

**Requirements & design documents:** Bridge between devs and stakeholders,
outlines the architecture and overviews the software.

**Wiki/Guides:** Explains concepts for the technology. For example, I used
a ringbuffer like datastructure once and created a wiki entry to explain the
conceptual level of how it works. May also provide mathematics on how something
works, which is great as its a very efficient way of expressing concepts.

**User manuals:** How a user should use your product, but often also loved by
the SysAdmin.

![Manuals xkcd](https://imgs.xkcd.com/comics/manuals.png)

So documenation come in very many flavors, and have many different use-cases.
There are some additional ones, such as QA documents, but those should almost
have a own blogpost for themselves.

## Challanges with documentation

With such complexity and so many different forms of documentation, there are
plenty of challenges with writing documentation:

- It is timeconsuming
- It can be(come) misleading
- It can become unsynced with the source (if you change the code it documents,
  but not the documentation)
- It becomes an ad-hoc operation

So many engineers and developers hate it, or dont do it all. It is often joked
that omitting documentation gives work security, because when youre the only
one who knows the technology, then you cant be fired.  hehe.

*HEHEHEHE.*

## Why document

So with all these challenges, why bother spending time and resources to write
good documentation? Why even write documentation at all? Well:

- 6 months from now, you're gonna thanks yourself because you dont remember the
  details of the technology you made
- You want to create value (thats why youre working with tech, right?) and be
  useful for the people around you
- You want people to use your technology (it makes your technology more
  valuable, which is good for you)
- It structures your thoughts and improved your technology
- You cant scale without Software Engineering and documentation is a part of SE

![if you could just document](https://media.makeameme.org/created/yeah-if-you-4xnjle.jpg)

Okay great, but again writing bad and misleading documenation is worse than no
documentation. So we must apply systems and tools to automate and scale the way
we do documentation, so that we can be more efficient and effective at our
technical writing skills. Thus Im going to introduce a toolchain for docs
below, and we'll get started with some proper docs. Sound good? Great!

## Scalable documentation toolchain

Lets implement a documentation stack for automating our documentation workflow!

### Round 1: Sphinx with Readthedocs

Sphinx is a rather mature documentation tool, being heavily used in the python
community, and written almost entirely in python. It is the tool used for
documenting a large number of open source projects, for example the:

- [Linux Kernel](https://www.kernel.org/doc/html/latest/index.html),
- [Python itself](https://docs.python.org/3/),
- [Blender](https://docs.blender.org/manual/en/latest/)
- And many more

First off on creating a scalable documentation stack with sphinx is to get
sphinx up and running. In addition I will host the test project on readthedocs,
for demo purposes and because its very quick and easy.

#### Prereq
- python with virtualenv and pip
- git
- virtualenv venv && source venv/bin/activate
- `pip install sphinx`

#### Setting up sphinx

**Key points:**
- Sphinx is based on the rst text format, but can be extended to use markdown
- Sphinx provides a nice wizard and some utitiles for building docs with make
  right off the bat

A good guide is already provided in the [readthedocs docs](https://docs.readthedocs.io/en/latest/intro/getting-started-with-sphinx.html).  TL;DR we do the following

```
$ mkdir docs && cd docs
$ sphinx-quickstart # and stick to defaults
$ make html
$ $BROWSER _builds/html/index.html
```

If the above commands succeeded, you should have very basic docs in your browser
now. Sphinx uses rst and many nifty things to bring home good documentation,
and you will use the web and [sphinx doc](http://www.sphinx-doc.org/) when
doing your actual documentation.

However there is a few key skills which is important in order to write scalable
documentation, which I need to talk about, and that is modularization and
generating docs from docstrings.

#### Modular Documentation

Okay so lets extend the index.rst file with another file. Lets say we have the
following folder structure

```
docs/
 | -- index.rst
 | -- api.rst
```

To include the extended documentation, we write the following in `index.rst`:

```
Documentation is Awesome!
=========================

.. toctree::
   :maxdepth: 1
   :caption: Table of Contents:

   api
```

This should include the api.rst file

#### Generating documentation from docstrings

First we make sure we can include our python code by adding the following in
our conf.py (fill out the path to the code):

```python
sys.path.insert(0, os.path.abspath('<path to code>'))
```

and make sure the *'sphinx.ext.autodoc'* extention is added to extentions in
conf.py. To write docstrings in a different format than traditional
reStructuredText (such as numpy below), include the *'sphinx.ext.napoleon'* extention aswell.
You want to include your python module in your api.rst file, such as this:

```
API documentaiton
=================

.. automodule:: <my python module with docstrings>
   :members:
```

Remember that it is included from the path set above.

Write docstrings in the code with, for example, the [NumPy](http://www.sphinx-doc.org/en/1.5/ext/example_numpy.html#example-numpy)
style docstrings, and finally compile the documentation with make.

`$ make html`

Now check out the docs, and you should see the docstrings in the documentation!

#### ReadTheDocs

Deploying on [ReadTheDocs](https://readthedocs.org) is quite straight forward.
Just set up a new account (with github), go to [Dashboard](https://readthedocs.org/dashboard/)
and press "Import a Project".  Then select the repository with the sphinx
documentation and you should be flying

If youve come this far, you can look at my test deployment [here](https://docme.readthedocs.io)

### Round 2: Sphinx with gh-pages
Since can be useful to deploy on gh-pages (such as in round 3), this next point will take on how we do that.

- Create a repository on github (which will be the gh-pages docs repo)
- Clone the repo as html:

```
$ git clone git@github.com/<username>/<repo>.git html
```

- cd into the repo and run quickstart:

```
$ cd html && sphinx-quickstart
```

Make sure you select `y` youre being prompted about githubpages

```
> githubpages: create .nojekyll file to publish the document on GitHub pages (y/n) [n]: 
```

- Now edit and build the docs. To run make clean (on html only), add the following to the makefile:

```
clean:
    @rm -rf $(BUILDDIR)/html/*.{html,js} $(BUILDDIR)/html/{objects.inv,_static,_sources,.buildinfo}
```

- Add a few extra items to the .gitignore:

```
# User ignores
objects.inv
.buildinfo
_sources
```

- Commit and push the project with all the html compiled: 

```
$ git commit -m "Added documentation as html for gh-pages" && git push -u <repo>
```

- Enable gh-pages on github for the repo by going to repository settings

![github pages setting](/assets/img/blog/gh-pages-docme.png)

Finally you should have it deployed on gh-pages like [this](https://peakbreaker.com/docme_pages), 
with [this repo](https://github.com/peakBreaker/docme_pages)

### Round 3: Sphinx with git submodules

Adding submodules is pretty straight forward
1. *$ git submodule add \<submodule\>*
2. Add the docs in the submodule to the rst files
3. Build and push the new documentation

Why do we do this? Well this is hugely useful if we have build our architecture
using microservices, and are not using a monorepo - which is common these
days. I wont go into details here - if you figured out Round 1 and 2 and know how git
submodules work, then this should be a breeze.

### Round 4: Deploying docs with OAuth on Heroku

*And checking organization membership*

This blogpost originally came from the desire to update and
improve the way my company does documentation. Understandably, they and many
others do not want all their trade secrets and proprietary technology openly
exposed on the web, so I wanted to add a layer of protection on the
documentation. Say hello to OAuth.

Now Im not going to go into the depths of how OAuth works, as there are many
guides already on that subject, and it can become a blogpost of its own.
I want to just set up and deploy a layer of OAuth protection on the
documentation. So for this I will planned the following:

- Use the [Flask-Dance](https://github.com/singingwolfboy/flask-dance) library
  to get OAuth capabilities
- Use GitHub OAuth
- Deploy on Heroku
- Check user organizations using OAuth and check if they are part of whatever
  org to authenticate

**Cool, so lets get started!**

#### Building the application

The author of the Flask Dance library had written an [example implementation](https://github.com/singingwolfboy/flask-dance-github)
 of Github OAuth, so I used it to get started. He also provided a very good
readme which I followed.

To check the organizations, I found an useful [issue](https://github.com/singingwolfboy/flask-dance/issues/131),
and github [api docs](https://developer.github.com/v3/orgs/) so I deployed the app with the following code:

```python
import os
import json

from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint(scope='read:org')
app.register_blueprint(github_bp, url_prefix="/login")

AMEDIA_ORG_ID = 582844


@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))

    # Get user details
    resp = github.get("/user")
    ret = '<h2>USER DETAILS:</h2><br>'
    if resp.ok:
        ret += "You are %s on GitHub<br>" % resp.json()["login"]
    else:
        ret += 'FAILED AT GETTING USER DATA<br>'

    # Get user organizations
    ret += '<h2>ORGANIZATIONS:</h2><br>'
    resp = github.get("/user/orgs")
    if not resp.ok:
        ret += 'FAILED AT GETTING USERORG DATA<br>'
    else:
        u_orgs = resp.json()
        ret += "<pre>%s</pre><br>" % json.dumps(u_orgs, indent=4)

        # Check if user is part of Amedia
        for org in u_orgs:
            if org.get('id', None) == AMEDIA_ORG_ID:
                ret += '<h3>--- YOU ARE PART OF AMEDIA ORGANIZATION --- </h3>'
                break
        else:
            ret += '<h3>--- YOU ARE NOT MEMBER OF AMEDIA --- </h3>'

    # Finally return the retval
    return ret


if __name__ == "__main__":
    app.run()
```

Some comments on the code above:
- Make sure the OAuth scope is correct too see user orgs. Notice the line 

```python
github_bp = make_github_blueprint(scope='read:org')
```

- Use env vars for the client_id and client_secret 

```python
os.environ.get('<env var>')
```

- Commit and push to a gh repo

#### Deploying to Heroku

Deploying to Heroku was a breeze once I got into the jazz. The guide on the gh
repo was very nice to follow, but the basic steps are as follows:

1. Create an account
2. Press *New->Create new app*
3. Name the app something fun
4. Press Connect to github (assuming the app is pushed to your gh)
5. Select the app
6. Make sure you have a [Procfile](https://devcenter.heroku.com/articles/procfile), [runtime.txt](https://devcenter.heroku.com/articles/python-runtimes), [app.json](https://devcenter.heroku.com/articles/app-json-schema) and
   requirements.txt in the repo
    - Procfile is one line and looks like this
    `web: gunicorn app:app --log-file=-`
    - runtime.txt tells heroku the python dist to use, for example is says: "python-3.7.0"
    - app.json provides heroku with some application meta information
7. Create a [github OAuth application](https://github.com/settings/applications/new), provide the ClientID and Client Secret to
   the heroku app using env vars in the heroku console (under application settings)
8. If done correctly, you should now see the app on your website.  See my [demo](https://peakbreaker-app.herokuapp.com/)
9. If the auth works, you should be able to just config the flask app to serve
   the docs as a static directory. I havent done this in the demo, but its no big thing

### Final words

Hopefully you now see that documentation is a large endeavour and that it is
worth doing right. If you have followed my instructions above, you should be
atleast a bit familiar with pretty decent documentation stack.

This post became quite long, but I hope you got something out of it. I know
I did, exploring this topic has been a fun journey.

![AmediaAnders](/assets/img/blog/amedia_job.jpg)

Best regards from Anders

