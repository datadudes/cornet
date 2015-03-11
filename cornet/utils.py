
import copy
import re


def merge_dict(a, b):
    """
    Merge dictionaries a and b recursively. If necessary, a overrides b .
    A new dictionary is returned, input arguments are not changed.
    """
    assert isinstance(a, dict), "First arg not a dict, but {0} ".format(a)
    assert isinstance(b, dict), "Second arg not a dict, but {0} ".format(b)

    merged = {}
    for key in set(a.keys() + b.keys()):
        if key not in b.keys():
            merged[key] = a[key]
        elif key not in a.keys():
            merged[key] = b[key]
        elif isinstance(a[key], dict) and isinstance(b[key], dict):
            merged[key] = merge_dict(a[key], b[key])
        elif isinstance(a[key], list) and isinstance(b[key], list):
            merged[key] = list(set(a[key] + b[key]))
        else:
            merged[key] = a[key]
    return merged


def dict_without_key(dict, key):
    """ Returned a new copy of dictionary without a specified key """
    d = copy.deepcopy(dict)
    if key in d:
        del d[key]
    return d


def match_any(patterns, string):
    """ Return true if s matches any of the regexps"""
    return any(re.match('^' + p + '$', string) for p in patterns)
