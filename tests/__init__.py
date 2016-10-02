import unittest


def suite():
    return unittest.TestLoader().discover('.')
