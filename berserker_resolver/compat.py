# -*- coding: utf-8 -*-

from sys import version_info as vi

def get_version():
    return vi.major

_version = get_version()

def xrange_compat(*args, **kwargs):
    if _version == 3:
        return range(*args, **kwargs)
    elif _version == 2:
        return xrange(*args, **kwargs)
