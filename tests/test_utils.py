from cornet.utils import merge_dict, dict_without_key, match_any


def test_merge_dict_with_empty():
    dic = {'a': 1, 'b': 2}
    assert merge_dict(dic, {}) == dic
    assert merge_dict({}, dic) == dic
    assert merge_dict({}, {}) == {}


def test_merge_dict_recursively():
    d1 = {
        'a': 1,
        'b': {1: 2, 3: 4, 5: {6: 7}},
        'c': {},
        'arr': [1, 2, 3]
    }
    d2 = {
        'b': {5: {6: 7, 8: 9}},
        'c': {10: 11, 12: 13},
        'd': 1,
        'arr': [3, 4]
    }
    assert merge_dict(d1, d2) == {
        'a': 1,
        'b': {1: 2, 3: 4, 5: {6: 7, 8: 9}},
        'c': {10: 11, 12: 13},
        'd': 1,
        'arr': [1, 2, 3, 4]
    }


def test_merge_dict_preference():
    assert merge_dict({1: 2}, {1: 3}) == {1: 2}


def test_without_key():
    d = {1: {2: 3}, 4: 5}
    assert dict_without_key(d, 1) == {4: 5}
    assert d == {1: {2: 3}, 4: 5}
    assert dict_without_key({1: 2}, 2) == {1: 2}


def test_matches_any():
    assert not match_any(['a', 'b', 'c'], 'aa')
    assert match_any(['aa', 'c'], 'aa')
    assert match_any(['aa.*', 'c'], 'aabb')
