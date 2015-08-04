import re
import random
import threading
import dns.resolver
import dns.exception
from berserker_resolver.utils import locked_iterator


class BaseResolver(object):
    _regexp_www = re.compile(r'(?:www\.){1}(.+\..+)', re.I)
    _regexp_www_combine = re.compile(r'(?:www\.)?(.+\..+)', re.I)

    def __init__(self, *args, **kwargs):
        self.tries = kwargs.get('tries', 1)
        self.timeout = kwargs.get('timeout', 1)
        self.qname = kwargs.get('qname', 'A')
        self.nameservers = kwargs.get('nameservers', ['8.8.8.8', '8.8.4.4', '77.88.8.8', '77.88.8.1',])
        self.verbose = kwargs.get('verbose', False)
        self.www = kwargs.get('www', False)
        self.www_combine = kwargs.get('www_combine', False)

        self._backend = dns.resolver.Resolver(configure=False)
        self._backend.lifetime = self.timeout

    def resolve(self, domains):
        domains = self._bind(domains)
        result, result_exception = self._run(domains)
        if self.verbose:
            return {
                'success' : result,
                'error' : result_exception,
            }
        else:
            return result

    def query(self, domain, ns=None):
        self._backend.nameservers = [ns or random.choice(self.nameservers)]
        return self._backend.query(domain, self.qname)

    def _bind(self, domains):
        for d in domains:
            for t in range(self.tries):
                for n in self.nameservers:
                    if self.www:
                        r = self._regexp_www.match(d)
                        if not r:
                            for i in (d, 'www.'+d):
                                yield i, n
                        else:
                            for i in (d, r.group(1)):
                                yield i, n
                    else:
                        yield d, n

    def _build(self, d, answer, result, result_exception):
        domain, ns = d
        if self.www_combine:
            domain = self._regexp_www_combine.match(domain).group(1)
        if not isinstance(answer, Exception):
            result.setdefault(domain, set()).update(iter(answer))
        elif self.verbose:
            result_exception.setdefault(domain, dict()).update({ns: answer})

    def _process(self, domains, result, result_exception):
        for d in domains:
            try:
                answer = self.query(*d)
            except dns.exception.DNSException as e:
                answer = e
            self._build(d, answer, result, result_exception)

    def _run(self, domains):
        result = {}
        result_exception = {}
        self._process(domains, result, result_exception)
        return result, result_exception


class Resolver(BaseResolver):
    def __init__(self, *args, **kwargs):
        super(Resolver, self).__init__(*args, **kwargs)
        self.threads = kwargs.get('threads', 16)
        self._lock = threading.Lock()

    @locked_iterator
    def _bind(self, *args, **kwargs):
        return super(Resolver, self)._bind(*args, **kwargs)

    def _build(self, *args, **kwargs):
        with self._lock:
            return super(Resolver, self)._build(*args, **kwargs)

    def _run(self, domains):
        result = {}
        result_exception = {}
        threads = []
        for i in range(self.threads):
            t = threading.Thread(target=self._process, args=(domains, result, result_exception))
            t.start()
            threads.append(t)
        for i in threads:
            i.join()
        return result, result_exception
