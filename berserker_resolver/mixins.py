# -*- coding: utf-8 -*-

from berserker_resolver.base import set_kwargs
from functools import reduce
from collections import defaultdict
from re import compile as re_compile
from re import I as re_I

class WwwMixin(object):
    www_resolve = False
    www_resolve_combine = False

    def __init__(self, **kwargs):
        kwargs = set_kwargs(self, kwargs, ['www_resolve', 'www_resolve_combine'])
        super(WwwMixin, self).__init__(**kwargs)

    def www_add(self, domains):
        domains += ['www.'+i for i in domains]
        return domains

    def www_combine(self, resolved):
        r = re_compile(r'^(?:www\.)?(.*)', re_I)
        resolved = [(r.match(x).group(1), y) for x, y in resolved]
        union = lambda x, y: (x[0],x[0].__setitem__(y[0],x[0][y[0]].union(y[1])))
        return list(reduce(union, resolved, (defaultdict(set),))[0].items())

    def resolve(self, domains):
        resolved = None
        resolve_orig = super(WwwMixin, self).resolve
        if self.www_resolve:
            domains = self.www_add(domains)
            resolved = resolve_orig(domains)
            if self.www_resolve_combine:
                resolved = self.www_combine(resolved)
        else:
            resolved = resolve_orig(domains)
        return resolved
