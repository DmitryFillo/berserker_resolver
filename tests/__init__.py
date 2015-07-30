import unittest

def get_suite():
    from tests.test_query import QueryTestCase
    from tests.test_resolver import BaseResolverTestCase, ResolverTestCase
    from tests.test_utils import UtilsTestCase

    query = unittest.TestLoader().loadTestsFromTestCase(QueryTestCase)
    base_resolver = unittest.TestLoader().loadTestsFromTestCase(BaseResolverTestCase)
    resolver = unittest.TestLoader().loadTestsFromTestCase(ResolverTestCase)
    utils = unittest.TestLoader().loadTestsFromTestCase(UtilsTestCase)

    return unittest.TestSuite([query, base_resolver, resolver, utils])
