import unittest
from mock import Mock
from collections import defaultdict
from berserker_resolver.resolver import BaseResolver, Resolver


class BaseResolverTestCase(unittest.TestCase):

    def setUp(self):
        self.resolver = BaseResolver()

    def test_defaults(self):
        self.assertEqual(self.resolver.tries, 1)
        self.assertEqual(self.resolver.nameservers, ['8.8.8.8', '8.8.4.4', '77.88.8.8', '77.88.8.1',])
        self.assertFalse(self.resolver.verbose)
        self.assertFalse(self.resolver.www)
        self.assertFalse(self.resolver.www_combine)

    def test_resolve(self):
        self.resolver._run_queries = lambda d: [(i[0], i[1], ['1.1.1.1', '2.2.2.2', '1.1.1.1']) for i in d]

        d = ['ya.ru', 'fillo.me']
        r = {
            'ya.ru' : set(['1.1.1.1', '2.2.2.2']),
            'fillo.me' : set(['1.1.1.1', '2.2.2.2']),
        }

        self.assertEqual(self.resolver.resolve(d), r)

    def test_resolve_www(self):
        self.resolver._run_queries = lambda d: [(i[0], i[1], ['1.1.1.1', '2.2.2.2', '1.1.1.1']) for i in d]
        self.resolver.www = True

        d = ['ya.ru', 'fillo.me']
        r = {
            'ya.ru' : set(['1.1.1.1', '2.2.2.2']),
            'fillo.me' : set(['1.1.1.1', '2.2.2.2']),
            'www.ya.ru' : set(['1.1.1.1', '2.2.2.2']),
            'www.fillo.me' : set(['1.1.1.1', '2.2.2.2']),
        }

        self.assertEqual(self.resolver.resolve(d), r)

    def test_resolve_www_combine(self):
        def run_queries(domains):
            result = []
            for d, ns in domains:
                if d == 'www.fillo.me':
                    result.append((d, ns, ['5.5.5.5']))
                else:
                    result.append((d, ns, ['1.1.1.1', '2.2.2.2']))
            return result

        self.resolver._run_queries = run_queries
        self.resolver.www = self.resolver.www_combine = True

        d = ['ya.ru', 'fillo.me']
        r = {
            'ya.ru' : set(['1.1.1.1', '2.2.2.2']),
            'fillo.me' : set(['1.1.1.1', '2.2.2.2', '5.5.5.5']),
        }

        self.assertEqual(self.resolver.resolve(d), r)

    def test_resolve_tries_and_nameservers(self):
        result = defaultdict(lambda: defaultdict(int))

        def run_queries(domains):
            for d, ns in domains:
                result[d][ns] += 1
            return []

        self.resolver._run_queries = run_queries
        self.resolver.tries = 10
        self.resolver.nameservers = ['one.ns', 'two.ns']

        d = ['ya.ru', 'fillo.me']
        r_ns = {'one.ns': 10, 'two.ns': 10}
        r = {
            'ya.ru' : r_ns,
            'fillo.me' : r_ns,
        }

        self.assertEqual(self.resolver.resolve(d), {})
        self.assertEqual(result, r)

    def test_resolve_verbose(self):
        def run_queries(domains):
            result = []
            for d, ns in domains:
                if d == 'test.exception':
                    if ns == 'test.ns':
                        result.append((d, ns, Exception('berserker:)')))
                    else:
                        result.append((d, ns, Exception('test')))
                else:
                    result.append((d, ns, [1,2,3,3,3,3,2,2]))
            return result

        self.resolver._run_queries = run_queries
        self.resolver.verbose = True
        self.resolver.nameservers.append('test.ns')

        d = ['fillo.me', 'test.exception']
        r_success = {
            'fillo.me' : set([1,2,3])
        }
        r_error = {
            'test.exception': {
                '77.88.8.1': Exception('test'),
                '77.88.8.8': Exception('test'),
                '8.8.4.4': Exception('test'),
                '8.8.8.8': Exception('test'),
                'test.ns': Exception('berserker:)'),
            }
        }

        resolved = self.resolver.resolve(d)
        self.assertEqual(resolved['success'], r_success)

        for ns, e in resolved['error']['test.exception'].items():
            self.assertEqual(str(r_error['test.exception'][ns]), str(e))


class ResolverTestCase(unittest.TestCase):

    def setUp(self):
        self.resolver = Resolver()

    def test_defaults(self):
        self.assertEqual(self.resolver.threads, 16)

    def test_resolver(self):
        self.resolver.query = Mock(side_effect=lambda d, ns: (d, ns, [d+'.answer', 1, 1]))
        r = {
            'ya.ru': set(['ya.ru.answer', 1]),
            'fillo.me': set(['fillo.me.answer', 1])
        }
        self.assertEqual(self.resolver.resolve(['ya.ru', 'fillo.me']), r)


if __name__ == '__main__':
    unittest.main()
