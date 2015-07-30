==================
Berserker Resolver
==================

.. image:: https://travis-ci.org/DmitryFillo/berserker_resolver.svg?branch=dev
     :target: https://travis-ci.org/DmitryFillo/berserker_resolver
.. image:: https://coveralls.io/repos/DmitryFillo/berserker_resolver/badge.svg?branch=dev&service=github
     :target: https://coveralls.io/github/DmitryFillo/berserker_resolver?branch=dev

Berserker Resolver is fast mass dns resolver which can bypass loadbalancers.

Tested with Python 2.7.8 and Python 3.4.2. But hope it works with many other versions.

Goal
----

Firstly, fast resolving. Resolving in one thread is very boring. Berkserer Resolver using threads and it's really fast approach (maybe some asyncio in the future, see TODO below).

Secondly, loadbalancers. For example, www.youtube.com is using loadbalancers and nameservers returns set of ip addresses with small TTL (try dig @8.8.8.8 www.youtube.com or dig @ns1.google.com www.youtube.com).
When TTL expired nameservers returns another set of ip addresses. How we can get ALL ip addresses? Of course, we know Google networks, but what about others sites?
In addition, some servers caches answers and do it differently. This is really bad for fine resolving. Solution is simple: query set of nameservers many times in the hope of getting all addresses.

And so Berserker Resolver emerged.

Backend of Berserker Resolver is dnspython.

How it use
----------

Install

    pip install berserker_resolver

You can use ThreadResolver which is thread-version of Berserker Resolver.

    from berserker_resolver import ThreadResolver

    resolver = ThreadResolver()

    to_resolve = ['ya.ru',]

    resolved = resolver.resolve(to_resolve)

    print(list(resolved)) # [('ya.ru', {'213.180.204.3', '93.158.134.3', '213.180.193.3'})]

Settings
--------

Keyword arguments to the constructor can be:

* **threads** is in how many threads resolve domains. Default is 1024.
* **tries** is how many times each nameserver will be quered. Default is 2.
* **lifetime** is timeout for each query. Default is 1 second.
* **nameservers** is nameservers list. Default is ['8.8.8.8', '8.8.4.4'].

Methods
-------

Main method is **resolve**. Note that the resolve method always returns **dict_items** (Python3) and **dictionary-itemiterator** (Python2). Argument must be list of domains.

Other methods you can find in the sources. Berserker Resolver is modular and simple.

About threads
-------------

Note that more threads lead to increase speed of resolving. You should test it and choose desired value. But carefully, you can create a DDoS attack!
And also check this: http://stackoverflow.com/questions/344203/maximum-number-of-threads-per-process-in-linux

WWW-prefix feature
------------------

Sometimes we need resolve domains with **www** prefix. Berserker Resolver can add this prefix to the list of domains automatically.

If **www_resolve** is True resolver will duplicate domains with **www** prefix.

    from berserker_resolver import ThreadResolver

    resolver = ThreadResolver(www_resolve=True)

    to_resolve = ['ya.ru',]

    resolved = resolver.resolve(to_resolve)

    print(list(resolved))) # [('ya.ru', {'213.180.204.3', '93.158.134.3', '213.180.193.3'}), ('www.ya.ru', {'213.180.204.3', '93.158.134.3', '213.180.193.3'})]

If **www_resolve_combine** is True resolver will combine domain with **www** prefix to his no-www version.

    from berserker_resolver import ThreadResolver

    resolver = ThreadResolver()

    to_resolve = ['test.example',]

    resolved = resolver.resolve(to_resolve)

    print(list(resolved)) # [('test.example', {'1.1.1.1'})]

    to_resolve = ['www.test.example',]

    resolved = resolver.resolve(to_resolve)

    print(list(resolved)) # [('www.test.example', {'2.2.2.2'})]

    resolver = ThreadResolver(www_resolve=True, www_resolve_combine=True)

    to_resolve = ['test.example',]

    resolved = resolver.resolve(to_resolve)

    print(list(resolved)) # [('test.example', {'1.1.1.1', '2.2.2.2'})]

More examples
-------------

See https://github.com/DmitryFillo/berserker_resolver/blob/master/examples.py

TODO
-------------

See https://github.com/DmitryFillo/berserker_resolver/blob/master/TODO
