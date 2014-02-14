title: Migration to Flask based blog engine
date: 2014-02-14 21:55:00
category: News
tags: [python, publishing]
lang: fr
summary: Fabrication de mon moteur de blog avec Flask-Flatpages et Frozen-Flask

[TOC]

Salut, pour commencer, je suis fier de vous annoncer la migration de ce blog
vers son nouveau moteur static !

[Pelican] est un très bon moteur mais il était un petit peu difficile de le
personnaliser pour qu'il corresponde à mes besoins alors, pour des raisons
didactiques, j'ai préféré créer le miens.

Aussi, je souhaitais tester Flask depuis longtemps et
[Le post de Nicolas Perriault] a fini de me convaincre.

Du coup, voici comment le tout est organisé :

Flask : Le framework
--------------------

[Flask] est un micro-framework qui permet de construire rapidement des
applications web REST puissantes et faciles à maintenir.

Il me permet de gérer mon schéma d'URLs ainsi que son jeu de fonctions.

Jinja2 : Les vues
-----------------

[Jinja2] est un moteur de template. Avec lui, je peux construire ma structure
HTML avec la flexibilité d'un langage dynamique.

Structures conditionnelles, boucles, variables, inclusions, tout est là.

Flask-FlatPages : Gestionnaire de contenu MarkDown
--------------------------------------------------

[Flask-FlatPages] est une extension construite pour fournir une
collection de pages à partir de fichiers "plats" (ex. MarkDown ou RST) à votre
application.

Avec elle, je peux écrire mes posts avec un langage de balisage facile à
utiliser et les servir via Flask.

La collection de pages est accessible depuis mon application et mes
templates Jinja2.

Frozen-Flask : The statifieur
-----------------------------

[Frozen-Flask] est une autre extension construite pour geler une application
Flask sous la forme d'un ensemble de fichiers HTML.

Avec elle, je peux rendre mon application totalement statique et, par
conséquent, l'héberger en utilisant n'importe quel service d'hébergement
supportant les fichiers HTML (tous en fait).

Frozen-Flask va parcourir votre application en  suivant le schéma d'URLs
ainsi que les liens des templates.

Python : La Glue
-----------------

Enfin, j'ai écrit un petit module un peu moche afin de gérer mes flux Atom
basé sur la collection de pages de Flask-FlatPages afin d'achever la
couverture fonctionnelle.

Voilà tout.


Le nouveau moteur est trés flexible et puissant et est multilingue.

[Pelican]: http://blog.getpelican.com/ "Pelican"
[Flask]: http://flask.pocoo.org/ "Flask"
[Jinja2]: http://jinja.pocoo.org/docs/ "Jinja2"
[Frozen-Flask]: http://pythonhosted.org/Frozen-Flask/ "Frozen-Flask"
[Flask-FlatPages]: http://pythonhosted.org/Flask-FlatPages/ "Flask-FlatPages"
[Le post de Nicolas Perriault]: https://nicolas.perriault.net/code/2012/dead-easy-yet-powerful-static-website-generator-with-flask/ "Le blog de Nicolas Perriault"

