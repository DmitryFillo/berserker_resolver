import unittest
from berserker_resolver.result import BerserkerResult


class BerserkerResultTestCase(unittest.TestCase):
    def setUp(self):
        self._domain = 'test.domain'
        self._resolver = BerserkerResult(self._domain)

    def test_initial(self):
        self.assertEqual(len(self._resolver.result), 0)
        self.assertEqual(self._resolver.domain, self._domain)
        self.assertEqual(str(self._resolver.domain), self._domain)

    def test_add(self):
        pass


if __name__ == '__main__':
    unittest.main()
