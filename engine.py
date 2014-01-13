#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from flask import Flask, render_template, request, send_from_directory
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
from werkzeug.exceptions import NotFound
from werkzeug.contrib.atom import AtomFeed

import atom

app = Flask(__name__, static_folder='static')

app_mode = os.getenv('FLASK_MODE', 'development')
if app_mode == 'production':
    app.config.from_object('config.ProductionConfig')
elif app_mode == 'development':
    app.config.from_object('config.DevelopmentConfig')

pages = FlatPages(app)
freezer = Freezer(app)

@app.route('/')
def index():
    articles = (p for p in pages if 'date' in p.meta)
    latest = sorted(articles, reverse=True, key=lambda p: p.meta['date'])
    return(render_template('index.html', pages=latest))

@app.route('/category/<string:category>/')
def category(category):
    catzed = [p for p in pages if category in p.meta.get('category', ['misc'])]
    return(render_template('category.html', pages=catzed, category=category))

@app.route('/tag/<string:tag>/')
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return(render_template('tag.html', pages=tagged, tag=tag))

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return(render_template('page.html', page=page))

@app.route('/feed/<string:lang>/latest.atom')
def feed(lang):
    return(atom.gen_feed(app.config, pages, lang))

@app.route('/static/css/pygments.css')
def pygments():
    return(pygments_style_defs('default'), 200, {'Content-Type': 'text/css'})

@app.route('/robots.txt')
def robots():
    return(send_from_directory(app.static_folder, request.path[1:]))

@app.route('/sitemap.xml')
def sitemap():
    return(send_from_directory(app.static_folder, request.path[1:]))

@app.errorhandler(404)
def page_not_found(e):
    return(render_template('404.html'), 404)

@app.errorhandler(500)
def internal_server_error(e):
    return(render_template('50x.html'), 500)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)

