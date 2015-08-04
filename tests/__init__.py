import unittest

def get_suite():
    from tests.test_resolver import BaseResolverTestCase, ResolverTestCase
    from tests.test_utils import UtilsTestCase

    base_resolver = unittest.TestLoader().loadTestsFromTestCase(BaseResolverTestCase)
    resolver = unittest.TestLoader().loadTestsFromTestCase(ResolverTestCase)
    utils = unittest.TestLoader().loadTestsFromTestCase(UtilsTestCase)

    return unittest.TestSuite([base_resolver, resolver, utils])
