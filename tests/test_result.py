import unittest
from berserker_resolver.result import BerserkerResult


class BerserkerResultTestCase(unittest.TestCase):
    _domain = 'test.domain'

    def test_initial(self):
        # Arrange
        sut = BerserkerResult(self._domain)

        # Assert
        self.assertEqual(len(sut.result), 0)
        self.assertEqual(sut.domain, self._domain)

    def test_add(self):
        # Arrange
        sut = BerserkerResult(self._domain)

        test_entity = type('', (), dict(ttl=15))()
        new_result = BerserkerResult(self._domain, [test_entity])

        # Act
        sut += new_result

        # Assert
        self.assertEqual(len(sut.result), 1)
        self.assertEqual(sut.result.pop().ttl, test_entity.ttl)

    def test_get_item_field(self):
        # Arrange
        test_entity1 = type('', (), dict(ttl=15))()
        test_entity2 = type('', (), dict(ttl=16, a='ggg.com'))()
        sut = BerserkerResult(self._domain, [test_entity1, test_entity2])

        # Act
        result1 = [sut['ttl'], sut['ttl']]
        result2 = [sut['a'], sut['a']]

        # Assert
        for r1 in result1:
            self.assertEqual(len(r1), 2)
            self.assertEqual(r1, {15, 16})

        for r2 in result2:
            self.assertEqual(len(r2), 1)
            self.assertEqual(r2, {'ggg.com'})


if __name__ == '__main__':
    unittest.main()
