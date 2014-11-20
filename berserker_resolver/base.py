# -*- coding: utf-8 -*-

from sys import version_info as vi

def get_version():
    return vi.major

def xrange_compat(*args, **kwargs):
    v = get_version()
    if v == 3:
        return range(*args, **kwargs)
    elif v == 2:
        return xrange(*args, **kwargs)

def set_kwargs(obj, kwargs, keywords=[]):
    for i in keywords:
        try:
            setattr(obj, i, kwargs.pop(i))
        except KeyError:
            pass

class MroFix(object):
    def __init__(self, **kwargs):
        pass
