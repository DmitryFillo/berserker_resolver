import unittest

suite = unittest.TestLoader().discover('tests')

unittest.TextTestRunner().run(suite)