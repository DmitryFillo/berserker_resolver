==================
Berserker Resolver
==================

.. image:: https://travis-ci.org/DmitryFillo/berserker_resolver.svg?branch=dev
     :target: https://travis-ci.org/DmitryFillo/berserker_resolver
.. image:: https://coveralls.io/repos/DmitryFillo/berserker_resolver/badge.svg?branch=dev&service=github
     :target: https://coveralls.io/github/DmitryFillo/berserker_resolver?branch=dev

Fast mass dns resolver which can bypass loadbalancers.

.. contents::

Motivation
==========

DNS servers can provide load balancing of many types. It can be simple round-robin or another algorithm that
depends on the implementation of a particular DNS server. See `RFC 1794 <https://tools.ietf.org/html/rfc1794>`_ 
to understand the capabilities and flexibility of the DNS protocol. As a result, it is possible that when the ordinary
resolver is not able to get *all* IP addresses, e.g. DNS server can return small sets of IP addresses (or even only one IP)
with low TTL per request. Number and presence of addresses may vary depending on the load of servers. Important to note
that this information can be cached by other DNS servers and can be distorted. Getting all IP addresses problem arises when
you want to resolve many domains with sufficient accuracy which useful for blocking network purposes, e.g. websites filtering,
parental controls, etc.

Let's try to make a couple probes for www.twitter.com via Google Public DNS.

.. code:: bash

    ; <<>> DiG 9.10.2-P1 <<>> @8.8.8.8 www.twitter.com +nocomments +noquestion
    ; (1 server found)
    ;; global options: +cmd
    www.twitter.com.	582	IN	CNAME	twitter.com.
    twitter.com.		13	IN	A	199.16.156.230
    twitter.com.		13	IN	A	199.16.156.198
    twitter.com.		13	IN	A	199.16.156.70
    twitter.com.		13	IN	A	199.16.156.38
    ;; Query time: 5 msec
    ;; SERVER: 8.8.8.8#53(8.8.8.8)
    ;; WHEN: Sat Aug 01 22:59:41 MSK 2015
    ;; MSG SIZE  rcvd: 122

.. code:: bash

    ; <<>> DiG 9.10.2-P1 <<>> @8.8.8.8 www.twitter.com +nocomments +noquestion
    ; (1 server found)
    ;; global options: +cmd
    www.twitter.com.	592	IN	CNAME	twitter.com.
    twitter.com.		22	IN	A	199.16.156.198
    twitter.com.		22	IN	A	199.16.156.70
    twitter.com.		22	IN	A	199.16.156.6
    twitter.com.		22	IN	A	199.16.156.38
    ;; Query time: 5 msec
    ;; SERVER: 8.8.8.8#53(8.8.8.8)
    ;; WHEN: Sat Aug 01 22:59:45 MSK 2015
    ;; MSG SIZE  rcvd: 122

You see different RR sets with small TTL. What about another public DNS, e.g. 4.2.2.1 by Level 3 Communications?

.. code:: bash

    ; <<>> DiG 9.10.2-P1 <<>> @4.2.2.1 www.twitter.com +nocomments +noquestion
    ; (1 server found)
    ;; global options: +cmd
    www.twitter.com.	153	IN	CNAME	twitter.com.
    twitter.com.		218	IN	A	199.16.156.38
    twitter.com.		218	IN	A	199.59.148.10
    twitter.com.		218	IN	A	199.59.150.39
    twitter.com.		218	IN	A	199.16.156.102
    twitter.com.		218	IN	A	199.16.156.6
    twitter.com.		218	IN	A	199.59.150.7
    twitter.com.		218	IN	A	199.59.148.82
    twitter.com.		218	IN	A	199.59.149.198
    twitter.com.		218	IN	A	199.16.156.198
    twitter.com.		218	IN	A	199.16.156.230
    twitter.com.		218	IN	A	199.59.149.230
    twitter.com.		218	IN	A	199.16.156.70
    ;; Query time: 41 msec
    ;; SERVER: 4.2.2.1#53(4.2.2.1)
    ;; WHEN: Sat Aug 01 22:58:57 MSK 2015
    ;; MSG SIZE  rcvd: 250

.. code:: bash

    ; <<>> DiG 9.10.2-P1 <<>> @4.2.2.1 www.twitter.com +nocomments +noquestion
    ; (1 server found)
    ;; global options: +cmd
    www.twitter.com.	390	IN	CNAME	twitter.com.
    twitter.com.		28	IN	A	185.45.5.43
    twitter.com.		28	IN	A	185.45.5.32
    ;; Query time: 43 msec
    ;; SERVER: 4.2.2.1#53(4.2.2.1)
    ;; WHEN: Sat Aug 01 22:58:58 MSK 2015
    ;; MSG SIZE  rcvd: 79

Let's try www.youtube.com.

.. code:: bash

    ; <<>> DiG 9.10.2-P1 <<>> @8.8.8.8 www.youtube.com +nocomments +noquestion
    ; (1 server found)
    ;; global options: +cmd
    www.youtube.com.	21584	IN	CNAME	youtube-ui.l.google.com.
    youtube-ui.l.google.com. 284	IN	CNAME	wide-youtube.l.google.com.
    wide-youtube.l.google.com. 284	IN	A	64.233.165.198
    ;; Query time: 4 msec
    ;; SERVER: 8.8.8.8#53(8.8.8.8)
    ;; WHEN: Sat Aug 01 22:49:32 MSK 2015
    ;; MSG SIZE  rcvd: 121

.. code:: bash

    ; <<>> DiG 9.10.2-P1 <<>> @8.8.8.8 www.youtube.com +nocomments +noquestion
    ; (1 server found)
    ;; global options: +cmd
    www.youtube.com.	21479	IN	CNAME	youtube-ui.l.google.com.
    youtube-ui.l.google.com. 179	IN	CNAME	wide-youtube.l.google.com.
    wide-youtube.l.google.com. 179	IN	A	173.194.71.198
    ;; Query time: 5 msec
    ;; SERVER: 8.8.8.8#53(8.8.8.8)
    ;; WHEN: Sat Aug 01 22:49:35 MSK 2015
    ;; MSG SIZE  rcvd: 121

.. code:: bash

    ; <<>> DiG 9.10.2-P1 <<>> @4.2.2.1 www.youtube.com +nocomments +noquestion
    ; (1 server found)
    ;; global options: +cmd
    www.youtube.com.	81953	IN	CNAME	youtube-ui.l.google.com.
    youtube-ui.l.google.com. 299	IN	A	173.194.44.36
    youtube-ui.l.google.com. 299	IN	A	173.194.44.40
    youtube-ui.l.google.com. 299	IN	A	173.194.44.35
    youtube-ui.l.google.com. 299	IN	A	173.194.44.33
    youtube-ui.l.google.com. 299	IN	A	173.194.44.46
    youtube-ui.l.google.com. 299	IN	A	173.194.44.32
    youtube-ui.l.google.com. 299	IN	A	173.194.44.37
    youtube-ui.l.google.com. 299	IN	A	173.194.44.34
    youtube-ui.l.google.com. 299	IN	A	173.194.44.41
    youtube-ui.l.google.com. 299	IN	A	173.194.44.39
    youtube-ui.l.google.com. 299	IN	A	173.194.44.38
    ;; Query time: 41 msec
    ;; SERVER: 4.2.2.1#53(4.2.2.1)
    ;; WHEN: Sat Aug 01 22:53:00 MSK 2015
    ;; MSG SIZE  rcvd: 254

.. code:: bash

    ; <<>> DiG 9.10.2-P1 <<>> @4.2.2.1 www.youtube.com +nocomments +noquestion
    ; (1 server found)
    ;; global options: +cmd
    www.youtube.com.	71178	IN	CNAME	youtube-ui.l.google.com.
    youtube-ui.l.google.com. 237	IN	A	216.58.209.206
    ;; Query time: 43 msec
    ;; SERVER: 4.2.2.1#53(4.2.2.1)
    ;; WHEN: Sat Aug 01 22:53:00 MSK 2015
    ;; MSG SIZE  rcvd: 83

This outputs may be outdated soon, but it is only necessary to show the behavior of DNS. Any website can use
load balancing and you not able to do full resolving simply.

The solution is query many nameservers many times for each domain. Yes, it's a bit clumsy, but works well enough
in many cases. The resolving should be performed in multiple threads, because resolving in one thread is slow,
especially in this case.

And so Berserker Resolver is emerged.

*It's worth noting that full resolving may be impossible because GEO load balancing or resolving can be occurred 
"at the wrong time in the wrong place" when some servers are down and their IP addresses are excluded from DNS pool by fault
tolerance algorithm. If you need actual information you should schedule resolving attempts, maintain your DNS database,
maybe perform resolving from different networks/servers. There is no universal solution for that cases, but you can use Berserker
Resolver as the backend in your application.*

Query backend
=============

Berserker Resolver is using `dnspython <http://www.dnspython.org/>`_ as query backend and so operates with its built-in types.

Supported versions
==================

* Python 2.6
* Python 2.7
* Python 3.2
* Python 3.3
* Python 3.4

Installation
============

Install using pip::

    pip install berserker_resolver

Resolver class
==============

Core of the Berserker Resolver.

Methods:

+ resolve

Properties:

+ nameservers
+ tries
+ timeout
+ qname
+ threads
+ www
+ www_combine
+ verbose

Properties can be assign via constructor or directly to the object.

Resolver.resolve
----------------

Resolve method. It takes list of domains and returns dictionary with results.

.. code:: python

    from berserker_resolver import Resolver

    domains = ['kernel.org', 'toster.ru']

    resolver = Resolver()
    result = resolver.resolve(domains)

    print(result)
    '''
        {
            'toster.ru': {
                <DNS IN A rdata: 178.248.236.52>
            },
            'kernel.org': {
                <DNS IN A rdata: 198.145.20.140>,
                <DNS IN A rdata: 199.204.44.194>,
                <DNS IN A rdata: 149.20.4.69>
            }
        }
    '''

Resolver.nameservers
--------------------

List of nameservers for resolving, each of them will be queried for particular domain.

The larger the list, the more chances to get all IP addresses, but it increases
time  needed for resolving.

Default is ``['8.8.8.8', '8.8.4.4', '77.88.8.8', '77.88.8.1']``.

Resolver.tries
--------------

Number of queries for each nameserver.

If the number of times increases, the resolving accuracy increases too, but it also
increases time to resolving.

Default is ``1``.

Resolver.timeout
----------------

The total number of seconds to spend trying to get an answer to the query.

Note that low timeout combined with high values of ``Resolver.tries`` and ``Resolver.threads`` can lead to
numerous timeout errors when nameserver does not have time to return a response.

Default is ``1``.

Resolver.threads
----------------

Number of threads.

More threads lead to increase speed of resolving, but too many threads lead to threads switching overhead.
You should test different numbers and choose one suitable for your systems. Also be careful with large number of threads, you can
flood the DNS server. If you want to use crazy large amount of threads, check
`stackoverflow thread <https://stackoverflow.com/questions/344203/maximum-number-of-threads-per-process-in-linux>`_ and
increase ``Resolver.timeout``.

Default is ``16``.

Resolver.qname
--------------

DNS query type name.

Default is ``A``.

Resolver.www
------------

This property enables automatic addition/removal of *www* prefix depending on the domain.

.. code:: python

    from berserker_resolver import Resolver

    domains = ['wikipedia.org', 'www.toster.ru']

    resolver = Resolver(www=True)
    result = resolver.resolve(domains)

    print(result)
    '''
        {
            'toster.ru': {
                <DNS IN A rdata: 178.248.236.52>
            },
            'www.wikipedia.org': {
                <DNS IN A rdata: 91.198.174.192>
            },
            'www.toster.ru': {
                <DNS IN A rdata: 178.248.236.52>
            },
            'wikipedia.org': {
                <DNS IN A rdata: 91.198.174.192>
            }
        }
    '''

Default is ``False``.

Resolver.www_combine
--------------------

This property enables automatic combining *www* prefix domains with theirs non-*www* versions.

.. code:: python

    from berserker_resolver import Resolver

    domains = ['facebook.com', 'www.facebook.com']

    resolver = Resolver()
    result = resolver.resolve(domains)

    print(result)
    '''
        {
            'facebook.com': {
                <DNS IN A rdata: 173.252.120.6>
            },
            'www.facebook.com': {
                <DNS IN A rdata: 31.13.93.3>,
                <DNS IN A rdata: 31.13.91.2>,
                <DNS IN A rdata: 173.252.88.66>,
                <DNS IN A rdata: 31.13.64.1>
            }
        }
    '''

    resolver.www_combine = True
    result = resolver.resolve(domains)

    print(result)
    '''
        {
            'www.facebook.com': {
                <DNS IN A rdata: 173.252.120.6>
                <DNS IN A rdata: 31.13.93.3>,
                <DNS IN A rdata: 31.13.91.2>,
                <DNS IN A rdata: 173.252.88.66>,
                <DNS IN A rdata: 31.13.64.1>
            }
        }
    '''

Powerful use case is combine this property together with ``Resolver.www``.

.. code:: python

    from berserker_resolver import Resolver

    domains = ['facebook.com']

    resolver = Resolver(www=True, www_combine=True)
    result = resolver.resolve(domains)

    print(result)
    '''
        {
            'www.facebook.com': {
                <DNS IN A rdata: 173.252.120.6>
                <DNS IN A rdata: 31.13.93.3>,
                <DNS IN A rdata: 31.13.91.2>,
                <DNS IN A rdata: 173.252.88.66>,
                <DNS IN A rdata: 31.13.64.1>
            }
        }
    '''

Default is ``False``.

Resolver.verbose
----------------

This property enables error reporting, e.g. nxdomain, noanswer, etc. ``Resolver.resolve`` normally returns
dictionary with resolved domains, but with this option it returns dictionary with two keys:

+ success
+ error

``result['success']`` is dictionary with successfully resolved domains, as if without ``Resolver.verbose``.
``result['error']`` is dictionary with unsuccessfully resolved domains where each key contains another dictionary
with per nameserver exception. Exceptions comes from dnspython backend as ``dns.exception.DNSException`` subclasses.
Check out `dnspython docs <http://www.dnspython.org/docs/1.12.0/dns.exception.DNSException-class.html>`_ for more
information about built-in exceptions.

.. code:: python

    from berserker_resolver import Resolver

    domains = ['nonexistent.domain', 'facebook.com']

    resolver = Resolver(verbose=True)
    result = resolver.resolve(domains)

    print(result)
    '''
        {
            'success': {
                'facebook.com': {
                    <DNS IN A rdata: 173.252.120.6>
                }
            },
            'error': {
                'nonexistent.domain': {
                    '77.88.8.1': NXDOMAIN(),
                    '8.8.4.4': NXDOMAIN(),
                    '8.8.8.8': NXDOMAIN(),
                    '77.88.8.8': NXDOMAIN()
                }
            }
        }
    '''

*Note that particular domain can be placed in both dictionaries, because some nameservers can return answer and some not.*

.. code:: python

    from berserker_resolver import Resolver

    domains = ['facebook.com']

    # 216.239.32.10 is ns1.google.com
    resolver = Resolver(nameservers=['216.239.32.10', '8.8.8.8'], verbose=True)
    result = resolver.resolve(domains)

    print(result)
    '''
        {
            'success': {
                'facebook.com': {
                    <DNS IN A rdata: 173.252.120.6>
                }
            },
            'error': {
                'facebook.com': {
                    '216.239.32.10': NoNameservers()
                }
            }
        }
    '''

Default is ``False``.

Finding the necessary number of tries
=====================================

*CAUTION! Heuristic feature!*

Berserker Resolver provides ``detect_tries`` function, which can detect necessary tries
for referece domain with a given accuracy.

Positional arguments are:

+ domain
+ cycles

Keyword arguments are passed to the ``Resolver`` as is, e.g. ``Resolver.threads``, ``Resolver.nameservers``,
etc.

.. code:: python

    from berserker_resolver import detect_tries

    tries = detect_tries(cycles=32, threads=1024, nameservers=['8.8.8.8', '127.0.0.1'])
    print(tries)

domain
------

Reference domain for detection, which means a domain which is totally load balanced.

Default is ``youtube.com``.

cycles
------

Desired accuracy. The higher the number, the better the result, but greatly increases function run time.

Default is ``100``.
