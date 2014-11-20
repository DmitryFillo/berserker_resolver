Berserker Resolver
==================

Berserker Resolver is fast mass dns resolver which can bypass loadbalancers.

Tested with Python 2.7.8 and Python 3.4.2. But hope it works with many other versions.

Goal
----

For example, YouTube is using loadbalancers and nameservers returns set of ip addresses with small TTL. When TTL expired nameservers returns another set of ip addresses. How we can get ALL ip addresses? 
Of course, we know Google networks, but what about others sites? 

We can query set of nameservers many times in the hope of getting all addresses. And so Berserker Resolver emerged.

Backend of Berserker Resolver is dnspython.

Concuerrence
------------

Resolving in one thread is very boring. Berkserer Resolver using threads and it's really fast approach.

But maybe add some asynchronous code (asyncio/coroutine) in the future. See TODO on GitHub.

Features
--------

Sometimes we need resolve domains with **www** prefix. Berserker Resolver can add this prefix to the list of domains automatically. See more info below.

Explanatory example
-------------------

Install package.

    pip install berserker_resolver

Initialize resolver.

    from berserker_resolver import ThreadResolver

    resolver = ThreadResolver()

    to_resolve = ['ya.ru',]

    resolved = resolver(to_resolve)

    print(resolved) # [('ya.ru', {'213.180.204.3', '93.158.134.3', '213.180.193.3'})]

Params
------

Params are keyword arguments to the constructor.

* **threads** is in how many threads resolve domains. Default is 8.
* **tries** is how many times each nameserver will be quered. Default is 2.
* **lifetime** is timeout for each query. Default is 2.
* **nameservers** is nameservers list. Default is ['8.8.8.8', '4.2.2.1'].

If **www_resolve** is True resolver will duplicate domains with **www** prefix. _Make sure that your domains list must NOT contain domains with **www** prefix for this case!_ Sometime this will be fixed. :)

    from berserker_resolver import ThreadResolver

    resolver = ThreadResolver(www_resolve=True)

    to_resolve = ['ya.ru',]

    resolved = resolver(to_resolve)

    print(resolved) # [('ya.ru', {'213.180.204.3', '93.158.134.3', '213.180.193.3'}), ('www.ya.ru', {'213.180.204.3', '93.158.134.3', '213.180.193.3'})]

If **www_resolve_combine** is True resolver will combine domain with **www** prefix to his no-www version.

    from berserker_resolver import ThreadResolver

    resolver = ThreadResolver()

    to_resolve = ['test.example',]

    resolved = resolver(to_resolve)

    print(resolved) # [('test.example', {'1.1.1.1'})]

    to_resolve = ['www.test.example',]

    resolved = resolver(to_resolve)

    print(resolved) # [('www.test.example', {'2.2.2.2'})]

    resolver = ThreadResolver(www_resolve=True, www_resolve_combine=True)

    to_resolve = ['test.example',]

    resolved = resolver(to_resolve)

    print(resolved) # [('test.example', {'1.1.1.1', '2.2.2.2'})]
