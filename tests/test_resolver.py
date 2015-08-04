import unittest
import dns.exception
from mock import Mock
from collections import defaultdict
from berserker_resolver.resolver import BaseResolver, Resolver


class BaseResolverTestCase(unittest.TestCase):

    def setUp(self):
        self.resolver = BaseResolver()

    def test_defaults(self):
        self.assertEqual(self.resolver.tries, 1)
        self.assertEqual(self.resolver.timeout, 1)
        self.assertEqual(self.resolver._backend.lifetime, self.resolver.timeout)
        self.assertEqual(self.resolver.qname, 'A')
        self.assertEqual(self.resolver.nameservers, ['8.8.8.8', '8.8.4.4', '77.88.8.8', '77.88.8.1',])
        self.assertFalse(self.resolver.verbose)
        self.assertFalse(self.resolver.www)
        self.assertFalse(self.resolver.www_combine)

    def test_query(self):
        self.resolver.nameservers = ['ip', 'second.ip', 'another.ip']

        def query(domain, qname):
            return domain, qname, self.resolver._backend.nameservers[0]

        self.resolver._backend.query = Mock(side_effect=query)

        result = self.resolver.query('test')
        self.assertEqual(result[0], 'test')
        self.assertEqual(result[1], 'A')
        self.assertTrue(result[2] in self.resolver.nameservers)

        result = self.resolver.query('test', 'custom.ip')
        self.assertEqual(result[0], 'test')
        self.assertEqual(result[1], 'A')
        self.assertEqual(result[2], 'custom.ip')

    def test_resolve(self):
        d = ['ya.ru', 'fillo.me']
        answer = ['ip', 'ip', 'another.ip']

        self.resolver._backend.query = Mock(side_effect=lambda d, q: answer)
        self.assertEqual(self.resolver.resolve(d), dict([(i, set(answer)) for i in d]))

    def test_resolve_tries_and_nameservers(self):
        d = ['ya.ru', 'fillo.me']

        self.resolver.tries = 42
        self.resolver.nameservers = ['one.ns', 'two.ns', 'three.ns']

        result = defaultdict(lambda: defaultdict(int))
        def query(domain, qname):
            ns = self.resolver._backend.nameservers[0]
            result[domain][ns] += 1
            return []

        self.resolver._backend.query = Mock(side_effect=query)

        for i in self.resolver.resolve(d).keys():
            self.assertEqual(dict(result[i]), dict([(i, self.resolver.tries) for i in self.resolver.nameservers]))

    def test_resolve_www(self):
        answer = ['ip', 'ip', 'another.ip']
        self.resolver._backend.query = Mock(side_effect=lambda d, q: answer)

        self.resolver.www = True

        d = ['ya.ru', 'fillo.me', 'www.ru', 'www.example.com', 'www.www.com',]
        r = {
            'ya.ru' : set(answer),
            'fillo.me' : set(answer),
            'example.com' : set(answer),
            'www.ru' : set(answer),
            'www.com' : set(answer),
            'www.ya.ru' : set(answer),
            'www.fillo.me' : set(answer),
            'www.www.ru' : set(answer),
            'www.www.com' : set(answer),
            'www.example.com' : set(answer),
        }

        self.assertEqual(self.resolver.resolve(d), r)

    def test_resolve_www_combine(self):
        answer = ['ip', 'ip', 'another.ip']
        answer_custom = ['test.ip']

        def query(domain, qname):
            if domain == 'www.fillo.me':
                return answer_custom
            else:
                return answer

        self.resolver._backend.query = Mock(side_effect=query)

        self.resolver.www_combine = True

        d = ['ya.ru', 'fillo.me', 'www.ru', 'www.example.com', 'www.www.com', 'www.fillo.me',]
        r = {
            'ya.ru' : set(answer),
            'fillo.me' : set(answer+answer_custom),
            'example.com' : set(answer),
            'www.ru' : set(answer),
            'www.com' : set(answer),
        }

        self.assertEqual(self.resolver.resolve(d), r)

    def test_resolve_verbose(self):
        d = ['ya.ru', 'fillo.me', 'except.com']
        answer = ['ip', 'ip', 'another.ip', 'bad.ns']

        def query(domain, qname):
            if domain == 'except.com' and \
               self.resolver._backend.nameservers[0] == 'bad.ns':
                raise dns.exception.DNSException('test')
            else:
                return []

        self.resolver._backend.query = Mock(side_effect=query)
        self.resolver.verbose = True
        self.resolver.nameservers = answer

        result = self.resolver.resolve(d)

        self.assertTrue('except.com' in result['success'])
        self.assertEqual(str(result['error']['except.com']['bad.ns']), 'test')


class ResolverTestCase(unittest.TestCase):

    def setUp(self):
        self.resolver = Resolver()

    def test_defaults(self):
        self.assertEqual(self.resolver.threads, 16)

    def test_resolve(self):
        d = ['ya.ru', 'fillo.me']
        answer = ['ip', 'ip', 'another.ip']

        self.resolver._backend.query = Mock(side_effect=lambda d, q: answer)
        self.assertEqual(self.resolver.resolve(d), dict([(i, set(answer)) for i in d]))

if __name__ == '__main__':
    unittest.main()
