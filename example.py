# -*- coding: utf-8 -*-

'''
Python 2/3 compat
'''
from berserker_resolver.base import get_version

_version = get_version()
if _version == 3:
    from urllib.request import urlopen
elif _version == 2:
    from urllib2 import urlopen

'''
Get ~10000 random domains from opendns github
'''
url = 'https://raw.githubusercontent.com/opendns/public-domain-lists/master/opendns-random-domains.txt'
domains = list(set([str(d, encoding='utf-8').replace('\n', '') for d in urlopen(url)]))

# ...
