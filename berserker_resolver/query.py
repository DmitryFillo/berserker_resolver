import random
import dns.resolver
import dns.exception


class Query(object):
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.get('timeout', 1)
        self.qname = kwargs.get('qname', 'A')
        self.nameservers = kwargs.get('nameservers', ['8.8.8.8', '8.8.4.4', '77.88.8.8', '77.88.8.1',])
        self._backend = dns.resolver.Resolver(configure=False)
        self._backend.lifetime = self.timeout

    def __call__(self, *args, **kwargs):
        return self.query(*args, **kwargs)

    def _set_ns(self, ns):
        self._backend.nameservers = [ns or random.choice(self.nameservers)]

    def query(self, domain, ns=None):
        self._set_ns(ns)
        try:
             answer = self._backend.query(domain, self.qname)
        except dns.exception.DNSException as e:
             answer = e
        return domain, ns, answer
