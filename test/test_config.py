
from sisyphus.config import TaskConfig


def test_merge_dict_with_empty():
    dic = {'a': 1, 'b': 2}
    assert TaskConfig._merge(dic, {}) == dic
    assert TaskConfig._merge({}, dic) == dic
    assert TaskConfig._merge({}, {}) == {}


def test_merge_dict_recursively():
    d1 = {
        'a': 1,
        'b': {1: 2,  3: 4, 5: {6: 7}},
        'c': {}
    }
    d2 = {
        'b': {5: {6: 7, 8: 9}},
        'c': {10: 11, 12: 13},
        'd': 1
    }
    assert TaskConfig._merge(d1, d2) == {
        'a': 1,
        'b': {1: 2, 3: 4, 5: {6: 7, 8: 9}},
        'c': {10: 11, 12: 13},
        'd': 1
    }


def test_merge_dict_preference():
    assert TaskConfig._merge({1: 2}, {1: 3}) == {1: 2}


def test_without_key():
    d = {1: {2: 3}, 4: 5}
    assert TaskConfig._without_key(d, 1) == {4: 5}
    assert d == {1: {2: 3}, 4: 5}
    assert TaskConfig._without_key({1: 2}, 2) == {1: 2}

