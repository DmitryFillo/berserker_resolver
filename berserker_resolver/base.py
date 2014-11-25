# -*- coding: utf-8 -*-

from functools import reduce
from collections import defaultdict
from berserker_resolver.compat import get_version

_version = get_version()

def set_kwargs(obj, kwargs, keywords=[]):
    '''
    Gets keywords from kwargs, deletes it and sets to obj.
    '''
    for i in keywords:
        try:
            setattr(obj, i, kwargs.pop(i))
        except KeyError:
            pass
    return kwargs

def fold(l):
    '''
    Folds list of tuples comprising key and set by combining (union) sets of the same keys.

    Example:
    l = [('xxx', {1,2,3}), ('xxx', {1,4}), ('yyy', {1,2,3})]
    result = [('xxx', {1,2,3,4}), ('yyy', {1,2,3})]
    '''
    union = lambda x, y: (x[0], x[0].__setitem__(y[0], x[0][y[0]].union(y[1])))
    result = reduce(union, l, (defaultdict(set),))[0]
    if _version == 3:
        result = result.items()
    elif _version == 2:
        result = result.iteritems()
    return result
