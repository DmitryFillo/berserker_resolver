# -*- coding: utf-8 -*-

print('make coffee ... :)')

'''
Python 2/3 compat
'''
from sys import version_info

_version = version_info.major

if _version == 3:
    from urllib.request import urlopen
elif _version == 2:
    from urllib2 import urlopen

'''
Speed measurement
'''
import time

def timer(f):
    def wrap(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print('Time: %f' % (time.time()-t))
        return res
    return wrap

'''
Get ~10000 random domains from opendns github
'''
url = 'https://raw.githubusercontent.com/opendns/public-domain-lists/master/opendns-random-domains.txt'
domains = list(set([d.decode('utf-8').replace('\n', '') for d in urlopen(url)]))

'''
Thread Resolver and ~10000 domains
'''
from berserker_resolver import ThreadResolver

# default params
resolver = ThreadResolver()

@timer
def resolve():
    print('\ndefault params (1024 threads, 2 tries, 1 second lifetime, 8.8.8.8 and 8.8.4.4 dns), ~10000 domains')
    resolved = resolver.resolve(domains)
    return resolved

resolve()

# increase threads
resolver = ThreadResolver(threads=2048)

@timer
def resolve():
    print('\ndefault params, but 2048 threads, ~10000 domains')
    resolved = resolver.resolve(domains)
    return resolved

resolve()

# add additional nameservers, increase tries, increase threads
nameservers = [
    '8.8.8.8',
    '8.8.4.4',
    '208.67.222.222',
    '208.67.220.220',
    '77.88.8.8',
    '77.88.8.1',
    '4.2.2.1'
]
resolver = ThreadResolver(threads=2048, tries=3, nameservers=nameservers)

@timer
def resolve():
    print('\nmany nameservers, 3 tries, 2048 threads, default lifetime, ~10000 domains')
    resolved = resolver.resolve(domains)
    return resolved

resolve()

# add www_resolve
resolver.www_resolve = True
resolver.www_resolve_combine = True

@timer
def resolve():
    print('\nprevious config + www-prefix resolve')
    resolved = resolver.resolve(domains)
    return resolved

resolve()

'''
Simple Resolver
Very slow, only for example (one-thread version of ThreadResolver, no threads param)
'''
from berserker_resolver import SimpleResolver

resolver = SimpleResolver(tries=1, lifetime=1)

@timer
def resolve():
    print('\none-thread slow resolver, 1 try, lifetime 1 second, 200 domains')
    resolved = resolver.resolve(domains[:200])
    return resolved

resolve()

'''
YouTube Resolving (loadbalancers test)
'''
import socket

@timer
def resolve():
    print('\nloadbalancered www.youtube.com resolving, gethostbyname')
    resolved = socket.gethostbyname('www.youtube.com')
    return resolved

print(resolve())

resolver = ThreadResolver(nameservers=nameservers)

@timer
def resolve():
    print('\nloadbalancered www.youtube.com resolving, ThreadResolver with many nameservers')
    resolved = resolver.resolve(['www.youtube.com'])
    return resolved

print(resolve())
