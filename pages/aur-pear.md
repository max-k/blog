title: Archlinux PEAR packaging layout
date: 2013-12-15 21:00:00
category: Archlinux
tags: [archlinux, packaging]
lang: en
summary: AUR PHP packaging experiments

Today, I tried to package a PHP software wich need some PEAR modules to work.

I'll come back soon to write something about this software but for now, I'll
focus on archlinux way to package PEAR modules.

My first research on AUR tells me that there is not so much PEAR packages
on it. Most of them was written by numkem whose seems to have been inspired by
jsteel so i decided to use jsteel's pear-net-socket package [1] as a beginning.

```
cd ~/build
yaourt -G pear-net-socket
cd pear-net-socket
makepkg -sfr
yaourt -U pear-net-socket-1.0.10-1-any.pkg.tar.xz
```

First problem, php is not a dependency. After the build, it's removed.
So, at this time, my package is installed on /usr/share/pear, directory owned
by php package but php itself is not installed.
It's not a big deal and probably acceptable.

The interesting part of his package is in the package function :

```.bash
pear install -R"$pkgdir" -O -n "$srcdir"/$_pkgname-$pkgver.tgz
```

A quick check on pear help explain me what's happend :

```
yaourt -S php-pear
pear help install
-R DIR, --installroot=DIR
    root directory used when installing files (aka PHP INSTALL_ROOT), use packagingroot for RPM
```

It tells to pear that the target directory for the installation is located
into the package so it doesn't install anything at build time.

Ok, fine, but what's happend when i try to install a PEAR package hosted on a
different repository ? Let's take a try :

```.bash
pear channel-add -R"$pkgdir" channel.xml
    Console_Getopt: unrecognized option -- R
```

Indeed, nothing is present in the documentation to relocate target directory
when adding a new channel. So I'll try another approach more generic :

```.bash
  local _PEARDIR="${pkgdir}/usr/share/pear"
  local _PEAROPTS="-D php_dir=${_PEARDIR} -D doc_dir=${_PEARDIR}/doc"
  local _PEAROPTS="${_PEAROPTS} -D test_dir=${_PEARDIR}/test"
  local _PEAROPTS="${_PEAROPTS} -D data_dir=${_PEARDIR}/data"
  pear ${_PEAROPTS} channel-add channel.xml
  pear ${_PEAROPTS} install -O -n ${_pkgname}-${pkgver}.tgz
  rm -r ${_PEARDIR}/{.channels,.depdb*,.filemap,.lock}
```

All right, the external channel adding is correctly relocated to package
directory doesn't involve system configuration at build time.

I'll use this new pattern in all of my PEAR packages now.

Here is the result of this packaging session :

* [pear-http-request](https://aur.archlinux.org/packages/pear-http-request)

* [pear-http-webdavclient](https://aur.archlinux.org/packages/pear-http-webdavclient/)

* [pear-mail-mime](https://aur.archlinux.org/packages/pear-mail-mime/)

* [pear-mail-mimedecode](https://aur.archlinux.org/packages/pear-mail-mimedecode/)

* [pear-net-url](https://aur.archlinux.org/packages/pear-net-url/)

* [symfony-event_dispatcher](https://aur.archlinux.org/packages/symfony-event_dispatcher/)

* [guzzle](https://aur.archlinux.org/packages/guzzle/)

* [php-aws-sdk](https://aur.archlinux.org/packages/php-aws-sdk/)

[1]: https://aur.archlinux.org/packages/pe/pear-net-socket/PKGBUILD "PKGBUILD"

