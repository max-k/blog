#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from collections import OrderedDict

from flask import Flask, render_template, request, send_from_directory, g
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
from werkzeug.exceptions import NotFound
from werkzeug.contrib.atom import AtomFeed
from jinja2 import Environment

import atom

jinja_env = Environment(extensions=['jinja2.ext.i18n', 'jinja2.ext.do'])

app = Flask(__name__, static_folder='static')

app_mode = os.getenv('FLASK_MODE', 'development')
if app_mode == 'production':
    app.config.from_object('config.ProductionConfig')
elif app_mode == 'development':
    app.config.from_object('config.DevelopmentConfig')

app.jinja_options['extensions'].append('jinja2.ext.do')

pages = FlatPages(app)
freezer = Freezer(app)

default_lang = app.config['DEFAULT_LANGUAGE']

@app.route('/')
def index():
    articles = (p for p in pages if 'date' in p.meta)
    latest = sorted(articles, reverse=True, key=lambda p: p.meta['date'])
    return(render_template('index.html', pages=latest))

@app.route('/category/<string:category>/', defaults={'lang': default_lang})
@app.route('/<string:lang>/category/<string:category>/')
def category(lang, category):
    g.category = category
    catzed = [p for p in pages if category in p.meta.get('category', 'Misc')]
    return(render_template('category.html', pages=catzed, category=category))

@app.route('/tag/<string:tag>/', defaults={'lang': default_lang})
@app.route('/<string:lang>/tag/<string:tag>/')
def tag(lang, tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return(render_template('tag.html', pages=tagged, tag=tag))

@app.route('/<path:path>/', defaults={'lang': default_lang})
@app.route('/<string:lang>/<path:path>/')
def page(lang, path):
    suffix = ''
    g.location = app.config['DEFAULT_LOCATION']
    if path in app.config['AVAILABLE_LANGUAGES']:
        lang = path
        return(index())
    if lang != default_lang:
        suffix = "-%s" % (lang)
    page = pages.get_or_404("%s%s" % (path, suffix))
    if page.meta.get('date', '') == '':
        g.location = path
    if page.meta.get('category', '') != '':
        g.category = page.meta.get('category')
    return(render_template('page.html', page=page))

@app.route('/feed/latest.atom', defaults={'lang': default_lang})
@app.route('/<string:lang>/feed/latest.atom')
def feed(lang):
    return(atom.gen_feed(app.config, pages, lang))

@app.route('/static/css/pygments.css')
def pygments():
    style = pygments_style_defs(app.config['PYGMENTS_THEME'])
    return(style, 200, {'Content-Type': 'text/css'})

#@app.route('/robots.txt')
#def robots():
#    return(send_from_directory(app.static_folder, request.path[1:]))

#@app.route('/sitemap.xml')
#def sitemap():
#    return(send_from_directory(app.static_folder, request.path[1:]))

#@app.route('/favicon.ico')
#def favicon():
#    return(send_from_directory(app.static_folder,
#                                'favicon.ico',
#                                mimetype='image/vnd.microsoft.icon'))

@app.errorhandler(404)
def page_not_found(e):
    return(render_template('404.html'), 404)

@app.errorhandler(500)
def internal_server_error(e):
    return(render_template('50x.html'), 500)

@freezer.register_generator
def generic_url_generator():
    categories = list(OrderedDict.fromkeys(
                         [p.meta.get('category', 'Misc') for p in pages]
                        ))
    tags = []
    for tag_list in [p.meta.get('tags', []) for p in pages]:
        tags.extend(tag_list)
    ordered_tags = list(OrderedDict.fromkeys(tags))
    paths = [p.path for p in pages]
    for lang in app.config['AVAILABLE_LANGUAGES']:
        yield 'feed', {'lang': lang}
        for path in paths:
            if lang == app.config['DEFAULT_LANGUAGE'] and path[-3] != '-':
                yield 'page', {'lang': lang, 'path': path}
            if lang != app.config['DEFAULT_LANGUAGE'] and path[-3] == '-':
                yield 'page', {'lang': lang, 'path': path[:-3]}
        for category in categories:
            yield 'category', {'lang': lang, 'category': category}
        for tag in ordered_tags:
            yield 'tag', {'lang': lang, 'tag': tag}

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)

