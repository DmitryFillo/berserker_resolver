import unittest
from berserker_resolver.utils import LockedIterator, locked_iterator


class UtilsTestCase(unittest.TestCase):
    def test_locked_iterator(self):
        @locked_iterator
        def test_gen(s):
            for i in [1, s]:
                self.assertTrue(g.lock.locked())
                yield i

        g = test_gen('test')

        self.assertTrue(isinstance(g, LockedIterator))

        self.assertEqual(next(g), 1)
        self.assertEqual(next(g), 'test')
        self.assertFalse(g.lock.locked())


if __name__ == '__main__':
    unittest.main()
