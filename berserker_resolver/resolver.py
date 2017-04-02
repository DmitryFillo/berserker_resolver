import re
import asyncio
import itertools
import collections
import aiodns


class BerserkerResult(object):
    def __init__(self, domain, results=None, errors=None):
        self._domain = domain
        self._results = set()
        self._errors = set()

        if results:
            self._results.update(results)
        if errors:
            self._errors.update(errors)

    def domain(self):
        return self._domain

    def results(self):
        return self._results

    def errors(self):
        return self._errors

    def __str__(self):
        return self._domain

    def __add__(self, other):
        if other.domain() != self._domain:
            raise TypeError('You can add BerserkerResult with another only if domain is equal.')

        if self._results:
            results = set(self._results)
        else:
            results = set()

        if self._errors:
            errors = set(self._errors)
        else:
            errors = set()

        other_results = other.results()
        other_errors = other.errors()

        if other_results:
            results.update(other_results)
        if other_errors:
            errors.update(other_errors)

        return BerserkerResult(domain=self._domain, results=results, errors=errors)


class BerserkerResolver(object):
    _regexp_www = re.compile(r'^www\.{1}(.+)$', re.I)
    # _regexp_www_combine = re.compile(r'(?:www\.)?(.+\..+)', re.I)

    def __init__(self, **kwargs):
        self.tries = kwargs.get('tries', 1)

        self.qname = kwargs.get('qname', 'A')

        # TODO: check nameservers availability
        self.nameservers = kwargs.get('nameservers', [
            '8.8.8.8',
            #'8.8.4.4',
            #'77.88.8.8',
            #'77.88.8.1',
            #'84.200.69.80',
            #'84.200.70.40',
        ])

        self.www = kwargs.get('www', False)

        self.chunk_size = kwargs.get('chunk_size', 1024)

        self._loop = kwargs.get('loop', asyncio.get_event_loop())

    async def resolve(self, domains):
        domains = self._bind(domains)
        results = {}
        futures = collections.deque()
        for c in self._get_chunks(domains):
            for domain, ns, i in c:
                futures.append(self._query(domain, ns, i))
            for (d, r) in await asyncio.gather(*futures):
                result = results.setdefault(d, None)
                if result:
                    results[d] += r
                else:
                    results[d] = r
            futures.clear()
        return results

    def resolve_until_complete(self, domains):
        return self._loop.run_until_complete(self.resolve(domains))

    async def _query(self, d, ns, i):
        resolver = self._get_resolver()
        resolver.nameservers = [ns]
        try:
            results = await resolver.query(i, self.qname)
            result = BerserkerResult(domain=d, results=results)
        except aiodns.error.DNSError as e:
            result = BerserkerResult(domain=d, errors=[e])
        return d, result

    def _get_resolver(self):
        return aiodns.DNSResolver(loop=self._loop, tries=1)

    def _get_chunks(self, domains):
        while True:
            chunk = tuple(itertools.islice(domains, self.chunk_size))
            if not chunk:
                return
            yield chunk

    def _bind(self, domains):
        if self.www:
            for d in domains:
                for i in self._bind_with_www(d):
                    for ns in self._bind_with_nameservers_and_tries():
                        yield d, ns, i
        else:
            for d in domains:
                for ns in self._bind_with_nameservers_and_tries():
                    yield d, ns, d

    def _bind_with_nameservers_and_tries(self):
        return (ns for ns in self.nameservers for _ in range(self.tries))

    def _bind_with_www(self, d):
        www = self._regexp_www.match(d)
        if www:
            for i in (d, www.group(1),):
                yield i
        else:
            for i in (d, 'www.' + d,):
                yield i
