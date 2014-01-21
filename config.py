# -*- coding: utf-8 -*-

class Config(object):
    DEBUG = False
    TESTING = False
    SITE_TITLE = u"Je me vide la tête"
    DEFAULT_AUTHOR = 'max-k'
    FLATPAGES_EXTENSION = '.md'
    FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite', 'extra', 'toc']
    FLATPAGES_AUTO_RELOAD = True
    FREEZER_REMOVE_EXTRA_FILES = True
    PYGMENTS_THEME = 'friendly'
    DEFAULT_LANGUAGE = "en"
    AVAILABLE_LANGUAGES = ["en", "fr"]
    FEED_SIZE_LIMIT = 15
    LOCALIZED_FEED_TITLES = {"en": "Most recent articles [en]",
                             "fr": u"Articles les plus récents [fr]"}
    DISPLAYED_CATEGORIES = ['Archlinux', 'News', 'Misc']
    DEFAULT_LOCATION = 'blog'

class ProductionConfig(Config):
    FREEZER_BASE_URL = 'https://blog.max-k.org/'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    FREEZER_RELATIVE_URLS = True

