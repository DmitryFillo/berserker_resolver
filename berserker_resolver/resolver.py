import re
import aiodns
import asyncio


class Resolver(object):
    _regexp_www = re.compile(r'^www\.{1}(.+)$', re.I)
    # _regexp_www_combine = re.compile(r'(?:www\.)?(.+\..+)', re.I)

    def __init__(self, **kwargs):
        self.tries = kwargs.get('tries', 1)

        # TODO: not working now
        self.timeout = kwargs.get('timeout', 3)

        self.qname = kwargs.get('qname', 'A')

        # TODO: check nameservers availability
        self.nameservers = kwargs.get('nameservers', [
            '8.8.8.8',
            '8.8.4.4',
            '77.88.8.8',
            '77.88.8.1',
            '84.200.69.80',
            '84.200.70.40',
        ])

        # TODO: is it needed? not working now
        self.verbose = kwargs.get('verbose', False)

        self.www = kwargs.get('www', False)

        # TODO: not working now
        self.www_combine = kwargs.get('www_combine', False)

        self._loop = kwargs.get('loop', asyncio.get_event_loop())

        # TODO: add timeout
        self._resolver = kwargs.get('resolver', aiodns.DNSResolver(loop=self._loop))

    @asyncio.coroutine
    def resolve(self, domains):
        domains = self._bind(domains)
        result = {}
        for domain, ns, domain_orig in domains:
            self._resolver.nameservers = [ns]
            f = yield from self._resolver.query(domain, self.qname)
            # TODO: add possibility to choose between orig and non-orig domains
            result.setdefault(domain_orig, set()).update(f)
        return result

    def resolve_until_complete(self, domains):
        return self._loop.run_until_complete(self.resolve(domains))

    def _bind(self, domains):
        for d in domains:
            for t in range(self.tries):
                for n in self.nameservers:
                    # TODO: move it outside the loop
                    if self.www:
                        with_www = self._regexp_www.match(d)
                        if with_www:
                            for i in (d, with_www.group(1)):
                                yield i, n, d
                        else:
                            for i in (d, 'www.'+d):
                                yield i, n, d
                    else:
                        # TODO: ???
                        yield d, n, d
