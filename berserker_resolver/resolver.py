import re
import random
import threading
import dns.resolver
import dns.exception
from berserker_resolver.utils import locked_iterator


class BaseResolver(object):
    def __init__(self, *args, **kwargs):
        self.tries = kwargs.get('tries', 1)
        self.nameservers = kwargs.get('nameservers', ['8.8.8.8', '8.8.4.4', '77.88.8.8', '77.88.8.1',])
        self.timeout = kwargs.get('timeout', 1)
        self.qname = kwargs.get('qname', 'A')
        self.verbose = kwargs.get('verbose', False)
        self.www = kwargs.get('www', False)
        self.www_combine = kwargs.get('www_combine', False)
        self._backend = dns.resolver.Resolver(configure=False)
        self._backend.lifetime = self.timeout

    def query(self, domain, ns=None):
        self._backend.nameservers = [ns or random.choice(self.nameservers),]
        try:
             answer = self._backend.query(domain, self.qname)
        except dns.exception.DNSException as e:
             answer = e
        return domain, ns, answer

    def resolve(self, domains):
        if self.www:
            domains = self._www(domains)

        domains = self._bind(domains)
        resolved = self.run_queries(domains)

        if self.www_combine:
            resolved = self._www_combine(resolved)

        result = self._fold(resolved)
        return result

    def _www(self, domains):
        r = re.compile(r'(?:www\.){1}.+', re.I)
        for i in domains:
            if not r.match(i):
                domains.append('www.'+i)
        return domains

    def _www_combine(self, resolved):
        r = re.compile(r'(?:www\.)?(.+)', re.I)
        resolved = ((r.match(domain).group(1), ns, answer) for domain, ns, answer in resolved)
        return resolved

    def _bind(self, domains):
        for d in domains:
            for t in range(self.tries):
                for n in self.nameservers:
                    yield d, n

    def _fold(self, resolved):
        result = {}
        result_exception = {}
        for domain, ns, answer in resolved:
            if not isinstance(answer, dns.exception.DNSException):
                result.setdefault(domain, set()).update(answer.rrset)
            elif self.verbose:
                result_exception.setdefault(domain, dict()).update({ns: answer})
        if self.verbose:
            return {
                'success' : result,
                'error' : result_exception,
            }
        else:
            return result

    def run_queries(self, domains):
        return NotImplemented


class ThreadResolver(BaseResolver):
    def __init__(self, *args, **kwargs):
        super(ThreadResolver, self).__init__(*args, **kwargs)
        self.threads = kwargs.get('threads', 16)
        self._lock = threading.Lock()

    @locked_iterator
    def _bind(self, *args, **kwargs):
        return super(ThreadResolver, self)._bind(*args, **kwargs)

    def _worker(self, domains, resolved):
        for i in domains:
            answer = self.query(*i)
            with self._lock:
                resolved.append(answer)

    def run_queries(self, domains):
        resolved = []
        threads = []
        for i in range(self.threads):
            t = threading.Thread(target=self._worker, args=(domains, resolved))
            t.start()
            threads.append(t)
        for i in threads:
            i.join()
        return resolved

