import pytest
from namespacedict import NamespaceDict


@pytest.fixture
def ns():
    return NamespaceDict()


def test_init(ns):
    assert ns.data == {}

    d = object()
    ns = NamespaceDict(d)
    assert ns.data is d


def test_name(ns):
    ns['x'] = 1
    assert ns['x'] == 1


def test_constant(ns):
    assert ns['1'] == 1
    with pytest.raises(SyntaxError):
        ns['1'] = 2


def test_subscript(ns):
    ns['x'] = [0]
    assert ns['x[0]'] == 0
    ns['x[0]'] = 1
    assert ns['x[0]'] == 1


def test_slice(ns):
    ns['x'] = [0, 1, 2]
    assert ns['x[0:2]'] == [0, 1]
    ns['x[0:2]'] = [4, 3]
    assert ns['x[::-1]'] == [2, 3, 4]


def test_attribute(ns):
    ns['x'] = lambda x: x
    ns['x.__doc__'] = 'doc'
    assert ns['x.__doc__'] == 'doc'


def test_tuple(ns):
    ns['x, y, z'] = 1, 2, 3
    assert ns['x, y, z'] == (1, 2, 3)
    assert type(ns['x, y, z']) is tuple

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
