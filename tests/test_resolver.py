import unittest
from berserker_resolver.resolver import Resolver


class ResolverTestCase(unittest.TestCase):
    def setUp(self):
        self.resolver = Resolver()

    def test_defaults(self):
        self.assertEqual(self.resolver.tries, 1)

    # TODO: write tests for resolve
    def test_resolve(self):
        pass


if __name__ == '__main__':
    unittest.main()
