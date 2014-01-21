# -*- coding: utf-8 -*-

from urlparse import urljoin
from flask import request
from werkzeug.contrib.atom import AtomFeed

def make_external(base_url, url):
    return urljoin(base_url, url)

def gen_feed(config, pages, lang):
    feed_title = config['LOCALIZED_FEED_TITLES'][lang]
    feed = AtomFeed(feed_title, feed_url=request.url, url=request.url_root)
    l_pages = (p for p in pages if 'date' in p.meta and p.meta['lang'] == lang)
    latest = sorted(l_pages, reverse=True, key=lambda p: p.meta['date'])
    for article in latest[:config['FEED_SIZE_LIMIT']]:
        author = config['DEFAULT_AUTHOR']
        if 'author' in article.meta:
            author = article.meta['author']
        path = "/%s/%s" % (lang, article.path[:-4])
        if lang == config['DEFAULT_LANGUAGE']:
            path = article.path
        feed.add(article.meta['title'], unicode(article.html),
                 content_type='html', author=author,
                 url=make_external(config['FREEZER_BASE_URL'], article.path),
                 updated=article.meta['date'])
    return(feed.get_response())

