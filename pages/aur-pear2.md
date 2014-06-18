title: Archlinux PEAR packaging layout 2
date: 2014-01-05 17:00:00
category: Archlinux
tags: [archlinux, packaging]
lang: en
summary: AUR PHP packaging experiments 2

Hi, on my last article [1], i talked about about archlinux PEAR packaging.

All the packages were correctly installed but there was a little problem :

Modules installed from external channels were'nt listed by PEAR as installed
because external channels themselves wheren't correctly registered.

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

I began by creating packages for channels as for the modules.

To install a pear channel, three things are needed :

* Channel folder stored in /usr/share/pear/.registry
* Channel registry file stored in /usr/share/pear/.channels
* Channel alias file stored in /usr/share/pear/.channels/.alias

Example for http://pear.symfony.com/ : 
[pear-channel-symfony2](https://aur.archlinux.org/packages/pe/pear-channel-symfony2/PKGBUILD)

Now, the channel needs to be added as a dependency to module's package :

```.bash
depends=('php>=5.3.2' 'pear-channel-symfony2')
```

Also .registry folder must no longer been deleted :

```.diff
-  rm -r ${_PEARDIR}/{.channels,.depdb*,.filemap,.lock,.registry}
+  rm -r ${_PEARDIR}/{.channels,.depdb*,.filemap,.lock}
+  rm -r ${_PEARDIR}/.registry/{.channel.__uri,.channel.*.php.net}
```

Take a look at the result after this update :

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

Here is the result of this packaging session :

* [pear-channel-symfony2](https://aur.archlinux.org/packages/pe/pear-channel-symfony2/)

* [symfony-event_dispatcher](https://aur.archlinux.org/packages/symfony-event_dispatcher/)

* [pear-channel-guzzlephp](https://aur.archlinux.org/packages/pear-channel-guzzlephp/)

* [guzzle](https://aur.archlinux.org/packages/guzzle/)

* [pear-channel-aws](https://aur.archlinux.org/packages/pear-channel-aws/)

* [php-aws-sdk](https://aur.archlinux.org/packages/php-aws-sdk/)

[1]: ../aur-pear "aur-pear"
