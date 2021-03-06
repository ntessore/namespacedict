import pytest
from namespacedict import NamespaceDict


@pytest.fixture
def ns():
    return NamespaceDict()


def test_abc(ns):
    from collections.abc import MutableMapping
    assert isinstance(ns, MutableMapping)


def test_init(ns):
    assert ns.data == {}

    d = object()
    ns = NamespaceDict(d)
    assert ns.data is d


def test_mapping(ns):
    ns.data = {'x': 1, 'y': 2, 'z': 3}
    assert len(ns) == 3
    assert list(k for k in ns) == ['x', 'y', 'z']
    assert list(ns.keys()) == ['x', 'y', 'z']
    assert list(ns.values()) == [1, 2, 3]
    assert list(ns.items()) == [('x', 1), ('y', 2), ('z', 3)]


def test_invalid(ns):
    with pytest.raises(TypeError):
        ns[0]

    for key in ('f()', 'lambda: None', 'x = y', 'import sys', 'type(())',
                '().__class__.__bases__[0].__subclasses__()'):
        with pytest.raises(SyntaxError):
            ns[key]
        with pytest.raises(SyntaxError):
            key in ns


def test_name(ns):
    ns['x'] = 1
    assert ns['x'] == 1
    assert 'x' in ns
    del(ns['x'])
    assert 'x' not in ns


def test_constant(ns):
    assert ns['1'] == 1
    assert '1' in ns
    assert ns['"a"'] == 'a'
    assert '"a"' in ns
    with pytest.raises(SyntaxError):
        ns['1'] = 2
    with pytest.raises(SyntaxError):
        del(ns['1'])


def test_subscript(ns):
    ns['x'] = [0]
    assert ns['x[0]'] == 0
    assert 'x[0]' in ns
    ns['x[0]'] = 1
    assert ns['x[0]'] == 1
    del(ns['x[0]'])
    assert len(ns['x']) == 0
    assert 'x[0]' not in ns
    assert 'y[0]' not in ns


def test_slice(ns):
    ns['x'] = [0, 1, 2]
    assert ns['x[0:2]'] == [0, 1]
    ns['x[0:2]'] = [4, 3]
    assert ns['x[::-1]'] == [2, 3, 4]
    del(ns['x[:2]'])
    assert len(ns['x']) == 1


def test_attribute(ns):
    ns['x'] = lambda x: x
    ns['x.myattrib'] = 'myval'
    assert ns['x.myattrib'] == 'myval'
    assert 'x.myattrib' in ns
    del(ns['x.myattrib'])
    with pytest.raises(AttributeError):
        ns['x.myattrib']
    assert 'x.myattrib' not in ns


def test_tuple(ns):
    ns['x, y, z'] = 1, 2, 3
    assert ns['x, y, z'] == (1, 2, 3)
    assert type(ns['x, y, z']) is tuple
    assert 'x, y, z' in ns
    del(ns['x, y'])
    assert 'x, y' not in ns
    assert 'x' not in ns and 'y' not in ns
    assert 'y, z' not in ns

    with pytest.raises(ValueError, match='too many values to unpack'):
        ns['x, y, z'] = 1, 2, 3, 4

    with pytest.raises(ValueError, match='not enough values to unpack'):
        ns['x, y, z'] = 1, 2

    with pytest.raises(TypeError, match='object is not iterable'):
        ns['x, y, z'] = 1


def test_list(ns):
    assert ns['[1, 2, 3]'] == [1, 2, 3]


def test_unary_op(ns):
    assert ns['+1'] == +1
    assert ns['-1'] == -1
    assert ns['not 1'] == (not 1)
    assert ns['~1'] == ~1
