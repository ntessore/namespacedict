namespacedict
=============

|tests| |coverage|

This package provides a `NamespaceDict` mapping which fully evaluates keys
using Python.  For example, it can perform nested lookups, attribute lookups,
and tuple splicing::

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
    >>> 
    >>> # set three items from a tuple
    >>> ns['a, b, c'] = 'A', 'B', 'C'
    >>> ns['b']
    'B'

Keys are parsed in a safe way using Python's AST library.  It is thus possible
to create complex dictionary queries as expected::

    >>> ns['one'] = 1
    >>> ns['two'] = 2
    >>> ns['x[0:two]'] = 5, 4
    >>> ns['x[::-one]']
    [3, 4, 5]


.. |tests| image:: https://github.com/ntessore/namespacedict/actions/workflows/test.yml/badge.svg
.. |coverage| image:: https://codecov.io/gh/ntessore/namespacedict/branch/main/graph/badge.svg?token=V0OKE8EBSY
