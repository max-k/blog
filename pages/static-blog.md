title: Migration to Flask based blog engine
date: 2014-02-14 21:55:00
category: News
tags: [python, publishing]
lang: en
summary: Building my own blog engine using Flask-Flatpages and Frozen-Flask

[TOC]

Hi, to begin, i'm proud to announce the migration of this blog to its brand new
static engine !

[Pelican] is a very good engine but it was a little bit painfull to customize
it to fit my needs so, for didactic purposes, i preferred to make my own.

Also, i wanted to try flask since a long time and [Nicolas Perriault's post]
about flask's static blogging capabilities finished to convince me.

So here is how it's organised :

Flask : The framework
---------------------

[Flask] is a micro-framework wich allows to quickly build powerfull, REST
compliants and easy to maintain web applications.

It allows me to handle my URL scheme and its set of functions.

Jinja2 : The views
------------------

[Jinja2] is a template engine. With it, I can build my HTML strucutre with the
flexibility of a dynamic language.

Conditionnal statements, loops, variables, includes, all is there.

Flask-FlatPages : Markdown content management system
---------------------------------------------------

[Flask-FlatPages] is an extension built to provide a collection of pages
from flat files (eg. MarkDown or RST) to your application.

With it, I can write my posts with an easy to use markup language and serve
them using Flask.

The pages collection is accessible from my application and my Jinja2
templates.

Frozen-Flask : The staticizer
-----------------------------

[Frozen-Flask] is another Flask extension build to freeze an application to
a set of HTML files.

With it you can make your Flask application totally static and host it on any
hosting service wich supports HTML files (all of them in fact).

Frozen-Flask will browse your application, following the URLs scheme and
templates's links.

Python : The Glue
-----------------

Finally, I wrote a small and ugly module to manage Atom feeds based on
Flask-FlatPages pages collection to finish functionnal coverage.

That's all folks.

The new engine is very flexible and powerfull and is multilingual.

You can checkout the sources : [here]

[Pelican]: http://blog.getpelican.com/ "Pelican"
[Flask]: http://flask.pocoo.org/ "Flask"
[Jinja2]: http://jinja.pocoo.org/docs/ "Jinja2"
[Frozen-Flask]: http://pythonhosted.org/Frozen-Flask/ "Frozen-Flask"
[Flask-FlatPages]: http://pythonhosted.org/Flask-FlatPages/ "Flask-FlatPages"
[Nicolas Perriault's post]: https://nicolas.perriault.net/code/2012/dead-easy-yet-powerful-static-website-generator-with-flask/ "Nicolas Perriault's Blog"
[here]: https://github.com/max-k/blog "blog on github"

