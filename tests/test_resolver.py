import unittest
import dns.exception
from mock import Mock
from collections import defaultdict
from berserker_resolver.resolver import BaseResolver, Resolver


class BaseResolverTestCase(unittest.TestCase):
    def setUp(self):
        self.resolver = BaseResolver()

    def test_defaults(self):
        self.assertEqual(self.resolver.tries, 48)
        self.assertEqual(self.resolver.timeout, 3)
        self.assertEqual(self.resolver._backend.lifetime, self.resolver.timeout)
        self.assertEqual(self.resolver.qname, 'A')
        self.assertEqual(self.resolver.nameservers, ['8.8.8.8', '8.8.4.4', '77.88.8.8', '77.88.8.1', '84.200.69.80', '84.200.70.40',])
        self.assertFalse(self.resolver.verbose)
        self.assertFalse(self.resolver.www)
        self.assertFalse(self.resolver.www_combine)

    def test_query(self):
        def query(d, qname):
            return d, qname, self.resolver._backend.nameservers[0]
        self.resolver._backend.query = Mock(side_effect=query)

        result = self.resolver.query('test')
        self.assertEqual(result[0], 'test')
        self.assertEqual(result[1], 'A')
        self.assertTrue(result[2] in self.resolver.nameservers)

        result = self.resolver.query('test', 'custom.ip')
        self.assertEqual(result[2], 'custom.ip')

    def test_resolve(self):
        domains = ['ya.ru', 'fillo.me']
        answer = ['ip', 'ip', 'another.ip']
        self.resolver._backend.query = Mock(side_effect=lambda d, qname: answer)
        self.assertEqual(self.resolver.resolve(domains), dict([(i, set(answer)) for i in domains]))

    def test_resolve_tries_and_nameservers(self):
        result = defaultdict(lambda: defaultdict(int))
        def query(d, qname):
            ns = self.resolver._backend.nameservers[0]
            result[d][ns] += 1
            return []
        self.resolver._backend.query = Mock(side_effect=query)
        self.resolver.tries = 42

        for i in self.resolver.resolve(['ya.ru', 'fillo.me']).keys():
            self.assertEqual(dict(result[i]), dict([(i, self.resolver.tries) for i in self.resolver.nameservers]))

    def test_resolve_www(self):
        self.resolver._backend.query = Mock(side_effect=lambda d, qname: [])
        self.resolver.www = True
        domains = ['ya.ru', 'fillo.me', 'www.ru', 'www.example.com', 'www.www.com',]
        result = {
            'ya.ru' : set([]),
            'fillo.me' : set([]),
            'example.com' : set([]),
            'www.ru' : set([]),
            'www.com' : set([]),
            'www.ya.ru' : set([]),
            'www.fillo.me' : set([]),
            'www.www.ru' : set([]),
            'www.www.com' : set([]),
            'www.example.com' : set([]),
        }

        self.assertEqual(self.resolver.resolve(domains), result)

    def test_resolve_www_combine(self):
        test_domain = 'fillo.me'
        test_domain_answer = ['fillo.me.ip']

        domains = ['ya.ru', 'www.ru', 'www.example.com', 'www.www.com', test_domain, 'www.'+test_domain]
        answer = ['ip', 'ip', 'another.ip']
        result = {
            'ya.ru' : set(answer),
            'example.com' : set(answer),
            'www.ru' : set(answer),
            'www.com' : set(answer),
            test_domain : set(answer+test_domain_answer),
        }

        def query(d, qname):
            if d == 'www.'+test_domain:
                return test_domain_answer
            else:
                return answer
        self.resolver._backend.query = Mock(side_effect=query)
        self.resolver.www_combine = True

        self.assertEqual(self.resolver.resolve(domains), result)

    def test_resolve_verbose(self):
        domain = 'bad.domains'
        ns = 'bad.ns'
        self.resolver.nameservers.append(ns)

        def query(d, qname):
            if d == domain and \
               self.resolver._backend.nameservers[0] == ns:
                raise dns.exception.DNSException('test')
            else:
                return []
        self.resolver._backend.query = Mock(side_effect=query)
        self.resolver.verbose = True

        result = self.resolver.resolve(['ya.ru', 'fillo.me', domain])
        self.assertTrue(domain in result['success'])
        self.assertEqual(str(result['error'][domain][ns]), 'test')


class ResolverTestCase(unittest.TestCase):
    def setUp(self):
        self.resolver = Resolver()

    def test_defaults(self):
        self.assertEqual(self.resolver.threads, 512)

    def test_resolve(self):
        domains = ['ya.ru', 'fillo.me']
        answer = ['ip', 'ip', 'another.ip']
        self.resolver._backend.query = Mock(side_effect=lambda d, qname: answer)
        self.assertEqual(self.resolver.resolve(domains), dict([(i, set(answer)) for i in domains]))


if __name__ == '__main__':
    unittest.main()
