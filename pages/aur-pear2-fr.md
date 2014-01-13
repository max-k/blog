title: Packaging de modules PEAR sous archlinux 2
date: 2014-01-05
category: Archlinux
tags: [archlinux, packaging]
lang: fr
summary: Experimentations PHP sous AUR 2

Salut, dans mon dernier article [1], j'ai abordé la packaging PEAR pour
archlinux.

Les paquets étaient correctement installés mais il y avait un petit problème :

Les modules installés depuis des canaux externes n'étaient pas listés par PEAR
comme installés car les canaux eux-mêmes n'était pas correctement enregistrés.

```.bash
$ yaourt -S symfony-event_dispatcher
$ pear list -a
Installed packages, channel __uri:
==================================
(no packages installed)

Installed packages, channel doc.php.net:
========================================
(no packages installed)

Installed packages, channel pear.php.net:
=========================================
(no packages installed)

Installed packages, channel pecl.php.net:
=========================================
(no packages installed)
```

J'ai commencé par créer des paquets pour les canaux comme pour les modules.

Pour installer un canal, trois éléments sont nécessaires :

* Le répertoire du canal stocké dans /usr/share/pear/.registry
* Le fichier d'enregistrement du canal stocké dans /usr/share/pear/.channels
* Le fichier d'alias du canal stocké dans /usr/share/pear/.channels/.alias

Exemple pour http://pear.symfony.com/ : 
[pear-channel-symfony2](https://aur.archlinux.org/packages/pe/pear-channel-symfony2/PKGBUILD)


Maintenant, le canal doit être ajouté en dépendance dans la paquet du module :

```.bash
depends=('php>=5.3.2' 'pear-channel-symfony2')
```

Le répertoire .registry ne doit également plus être supprimé :

```.diff
-  rm -r ${_PEARDIR}/{.channels,.depdb*,.filemap,.lock,.registry}
+  rm -r ${_PEARDIR}/{.channels,.depdb*,.filemap,.lock}
+  rm -r ${_PEARDIR}/.registry/{.channel.__uri,.channel.*.php.net}
```

Jetons un oeil au résultat après cette mise à jour :

```.bash
$ yaourt -S symfony-event_dispatcher
$ pear list -a
Installed packages, channel __uri:
==================================
(no packages installed)

Installed packages, channel doc.php.net:
========================================
(no packages installed)

Installed packages, channel pear.php.net:
=========================================
(no packages installed)

Installed packages, channel pear.symfony.com:
=============================================
Package         Version State
EventDispatcher 2.4.0   stable

Installed packages, channel pecl.php.net:
=========================================
(no packages installed)
```

Tada !!

Voici le résultat de cette session de packaging :

* [pear-channel-symfony2](https://aur.archlinux.org/packages/pe/pear-channel-symfony2/)

* [symfony-event_dispatcher](https://aur.archlinux.org/packages/symfony-event_dispatcher/)

* [pear-channel-guzzlephp](https://aur.archlinux.org/packages/pear-channel-guzzlephp/)

* [guzzle](https://aur.archlinux.org/packages/guzzle/)

* [pear-channel-aws](https://aur.archlinux.org/packages/pear-channel-aws/)

* [php-aws-sdk](https://aur.archlinux.org/packages/php-aws-sdk/)

[1]: ./aur-pear-fr.html "aur-pear"
