namespacedict
=============

|tests| |coverage|

This package provides a ``NamespaceDict`` mapping which fully evaluates keys
using Python syntax.  For example, it can perform nested lookups, attribute
lookups, and tuple splicing::

    >>> from namespacedict import NamespaceDict
    >>>
    >>> # create a new namespace
    >>> ns = NamespaceDict()
    >>>
    >>> # nested lookup from a list
    >>> ns['x'] = [1, 2, 3]
    >>> ns['x[1]']
    2
    >>> # set a docstring attribute
    >>> ns['y'] = lambda x: x
    >>> ns['y.__doc__'] = 'my function'
    >>> ns['y.__doc__']
    'my function'
    >>>
    >>> # set three items from a tuple
    >>> ns['a, b, c'] = 'A', 'B', 'C'
    >>> ns['b']
    'B'

Keys are parsed in a safe way using Python's AST library.  It is thus possible
to create complex dictionary queries that work as expected::

    >>> ns['one'] = 1
    >>> ns['two'] = 2
    >>> ns['x[0:two]'] = 5, 4
    >>> ns['x[::-one]']
    [3, 4, 5]

The ``NamespaceDict`` type can also be used as an adapter for other mappings,
by passing the underlying data structure on initialisation::

    >>> # create a numpy array with named columns
    >>> import numpy as np
    >>> a = np.empty(5, dtype=[('col1', int), ('col2', int), ('col3', int)])
    >>>
    >>> # use NamespaceDict to access array
    >>> ns = NamespaceDict(a)
    >>>
    >>> # access named columns through namespace
    >>> ns['col1, col2, col3'] = 1, 2, 3
    >>> ns['col2']
    array([2, 2, 2, 2, 2])

The mapping can be retrieved using the ``.data`` attribute.

.. |tests| image:: https://github.com/ntessore/namespacedict/actions/workflows/test.yml/badge.svg
   :target: https://github.com/ntessore/namespacedict/actions/workflows/test.yml
.. |coverage| image:: https://codecov.io/gh/ntessore/namespacedict/branch/main/graph/badge.svg?token=V0OKE8EBSY
   :target: https://codecov.io/gh/ntessore/namespacedict
