# -*- coding: utf-8 -*-

from berserker_resolver.base import set_kwargs, xrange_compat
from dns.resolver import Resolver

class BaseQuery(object):
    lifetime = 2
    resolver = Resolver()

    def __init__(self, **kwargs):
        set_kwargs(self, kwargs, ['lifetime'])
        self.resolver.lifetime = self.lifetime
        super(BaseQuery, self).__init__(**kwargs)

    def base_query(self, domain):
        q = []
        try:
            q = self.resolver.query(domain, 'A')
            q = [i.to_text() for i in q]
        except:
            pass
        return q

class Query(BaseQuery):
    tries = 2
    nameservers = ['8.8.8.8', '127.0.0.1',]

    def __init__(self, **kwargs):
        set_kwargs(kwargs, ['tries', 'nameservers'])
        super(Query, self).__init__(**kwargs)

    def query(self, domain):
        resolved = set()
        for t in xrange_compat(self.tries):
            for nameserver in self.nameservers:
                self.resolver.nameservers = [nameserver]
                q = self.base_query(domain)
                resolved.update(set(q))
        return resolved
