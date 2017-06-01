import re
import asyncio
import itertools
import collections
import aiodns
from berserker_resolver.result import BerserkerResult


class BerserkerResolver(object):
    _regexp_www = re.compile(r'^www\.{1}(.+)$', re.I)

    def __init__(self, **kwargs):
        self.tries = kwargs.get('tries', 1)
        self.timeout = kwargs.get('timeout', 1)
        self.qname = kwargs.get('qname', 'A')

        self.nameservers = kwargs.get('nameservers', [
            '8.8.8.8',
            '8.8.4.4',
            '77.88.8.8',
            '77.88.8.1',
            '4.2.2.1',
            '4.2.2.2',
        ])

        self.www = kwargs.get('www', False)
        self.chunk_size = kwargs.get('chunk_size', 256)
        self._loop = kwargs.get('loop', asyncio.get_event_loop())

    def resolve_until_complete(self, domains):
        return self._loop.run_until_complete(self.resolve(domains))

    @asyncio.coroutine
    def resolve(self, domains):
        domains = self._bind(domains)
        results = {}
        futures = collections.deque()
        resolvers = self._get_resolvers()
        for c in self._get_chunks(domains):
            for domain, ns, i in c:
                futures.append(self._query(domain, i, resolvers[ns]))
            for (d, r) in (yield from asyncio.gather(*futures, loop=self._loop)):
                if results.setdefault(d, None):
                    results[d] += r
                else:
                    results[d] = r
            futures.clear()
        return results

    @asyncio.coroutine
    def _query(self, d, i, resolver):
        try:
            results = yield from resolver.query(i, self.qname)
            result = BerserkerResult(domain=d, result=results)
        except aiodns.error.DNSError:
            # Mass resolver doesn't care about DNS errors, so just initialize empty BerserkerResult
            result = BerserkerResult(domain=d)
        return d, result

    def _get_resolvers(self):
        return dict((i, self._create_resolver(i)) for i in self.nameservers)

    def _create_resolver(self, ns=None):
        resolver = aiodns.DNSResolver(loop=self._loop, tries=self.tries, timeout=self.timeout)
        if ns:
            resolver.nameservers = [ns]
        return resolver

    def _get_chunks(self, domains):
        domains_iter = iter(domains)
        while True:
            chunk = tuple(itertools.islice(domains_iter, self.chunk_size))
            if not chunk:
                return
            yield chunk

    def _bind(self, domains):
        for d in domains:
            for i in self._bind_with_www(d):
                for ns in self._bind_with_nameservers_and_tries():
                    yield d, ns, i

    def _bind_with_nameservers_and_tries(self):
        return (ns for ns in self.nameservers for _ in range(self.tries))

    def _bind_with_www(self, d):
        if self.www:
            www = self._regexp_www.match(d)
            if www:
                for i in (d, www.group(1),):
                    yield i
            else:
                for i in (d, 'www.' + d,):
                    yield i
        else:
            yield d
