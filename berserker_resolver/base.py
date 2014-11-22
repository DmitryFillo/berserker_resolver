# -*- coding: utf-8 -*-

from sys import version_info as vi
from functools import reduce
from collections import defaultdict

def get_version():
    return vi.major

def xrange_compat(*args, **kwargs):
    v = get_version()
    if v == 3:
        return range(*args, **kwargs)
    elif v == 2:
        return xrange(*args, **kwargs)

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
    result = list(reduce(union, l, (defaultdict(set),))[0].items())
    return result
