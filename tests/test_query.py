import unittest
import dns.exception
from unittest.mock import Mock
from berserker_resolver.query import Query


class QueryTestCase(unittest.TestCase):

    def setUp(self):
        self.query = Query()
        self.query._backend.query = Mock(side_effect=lambda domain, qname: (domain, qname))

    def test_defaults(self):
        self.assertEqual(self.query.timeout, 1)
        self.assertEqual(self.query.timeout, self.query._backend.lifetime)
        self.assertEqual(self.query.qname, 'A')
        self.assertEqual(self.query.nameservers, ['8.8.8.8', '8.8.4.4', '77.88.8.8', '77.88.8.1',])

    def test_query(self):
        d = 'test.domain'
        ns = 'test.ns'
        result = self.query(d, ns)

        self.assertEqual(result, (d, ns, (d, self.query.qname)))
        self.assertTrue(ns in self.query._backend.nameservers)

    def test_query_with_default_ns(self):
        result = self.query('berserker:)')

        self.assertTrue(result[1] in self.query.nameservers)

    def test_query_exception(self):
        self.query._backend.query = Mock(side_effect=dns.exception.DNSException)
        result = self.query('berserker:)')

        self.assertTrue(isinstance(result[2], Exception))


if __name__ == '__main__':
    unittest.main()
