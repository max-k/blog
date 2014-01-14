title: Packaging de modules PEAR sous archlinux
date: 2013-12-15 21:00:00
category: Archlinux
tags: [archlinux, packaging]
lang: fr
summary: Experimentations packaging PHP sous AUR

Aujourd'hui, j'ai tenté de packager un logiciel PHP qui nécessitait quelques
modules PEAR pour fonctionner.

Je reviendrai très bientôt écrire un billet à propos de ce logiciel mais pour
le moment, je vais me concentrer sur la manière de packager des modules PEAR
sous archlinux.

Ma première recherche sur AUR m'a permis de découvrir que seuls quelques
paquets PEAR étaient présents. La plupart d'entre eux étaient écris par numkem
qui s'est à priori lui-même inspiré de jsteel. J'ai donc décidé de me baser
sur le paquet pear-net-socket [1] de jsteel pour commencer.

```
cd ~/build
yaourt -G pear-net-socket
cd pear-net-socket
makepkg -sfr
yaourt -U pear-net-socket-1.0.10-1-any.pkg.tar.xz
```

Premier problème, php n'est pas une dépendance. Après le build, il est
désinstallé. Du coup, à cet instant, mon paquet est installé dans le répertoire
/usr/share/pear qui appartient au paquet php qui lui-même n'est pas installé.
Bon, rien de trop grace ceci-dit, ça semble même acceptable.

La partie intéressante de son paquet se trouve dans la fonction package :

```.bash
pear install -R"$pkgdir" -O -n "$srcdir"/$_pkgname-$pkgver.tgz
```

Une petite recherche dans la doc de pear nous explique ce qui se passe :

```
yaourt -S php-pear
pear help install
-R DIR, --installroot=DIR
    root directory used when installing files (aka PHP INSTALL_ROOT), use packagingroot for RPM
```

L'option indique a pear qur le répertoire d'installation cible se trouve
dans le paquet de sorte que rien n'est réellement installé pendant le build.

Ok, très bien, mais que se passe-t-il si j'essaie d'installer un paquet PEAR
hébergé sur un dépôt différent ? Testons ça :

```.bash
pear channel-add -R"$pkgdir" channel.xml
    Console_Getopt: unrecognized option -- R
```

En effet, rien n'est présent dans la doc pour rediriger le répertoire cible
lorsqu'on ajoute un nouveau canal. Testons une approche plus générique :

```.bash
  local _PEARDIR="${pkgdir}/usr/share/pear"
  local _PEAROPTS="-D php_dir=${_PEARDIR} -D doc_dir=${_PEARDIR}/doc"
  local _PEAROPTS="${_PEAROPTS} -D test_dir=${_PEARDIR}/test"
  local _PEAROPTS="${_PEAROPTS} -D data_dir=${_PEARDIR}/data"
  pear ${_PEAROPTS} channel-add channel.xml
  pear ${_PEAROPTS} install -O -n ${_pkgname}-${pkgver}.tgz
  rm -r ${_PEARDIR}/{.channels,.depdb*,.filemap,.lock}
```

Impeccable, l'ajout du canal externe est bien redirigé dans la paquet et
n'impacte donc pas notre installation pendant le build.

Je vais désormais utiliser cette méthode dans tous mes paquets PEAR.

Voici le résultat de cette session de packaging :

* [pear-http-request](https://aur.archlinux.org/packages/pear-http-request)

* [pear-http-webdavclient](https://aur.archlinux.org/packages/pear-http-webdavclient/)

* [pear-mail-mime](https://aur.archlinux.org/packages/pear-mail-mime/)

* [pear-mail-mimedecode](https://aur.archlinux.org/packages/pear-mail-mimedecode/)

* [pear-net-url](https://aur.archlinux.org/packages/pear-net-url/)

* [symfony-event_dispatcher](https://aur.archlinux.org/packages/symfony-event_dispatcher/)

* [guzzle](https://aur.archlinux.org/packages/guzzle/)

* [php-aws-sdk](https://aur.archlinux.org/packages/php-aws-sdk/)

[1]: https://aur.archlinux.org/packages/pe/pear-net-socket/PKGBUILD "PKGBUILD"

