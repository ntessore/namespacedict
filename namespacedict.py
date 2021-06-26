# author: Nicolas Tessore <n.tessore@ucl.ac.uk>
# license: MIT

__version__ = '0.2.0'

__all__ = ['NamespaceDict']

import ast
from collections import UserDict


class NamespaceDict(UserDict):
    def __init__(self, data=None):
        super().__init__()
        if data is not None:
            self.data = data

    def __getitem__(self, key):
        return self._dispatch(key, self._get)

    def __setitem__(self, key, value):
        return self._dispatch(key, self._set, value)

    def __delitem__(self, key):
        return self._dispatch(key, self._del)

    @staticmethod
    def _syntax_error(key, node):
        details = ('<key>', node.lineno, node.col_offset+1, key)
        raise SyntaxError('invalid syntax', details)

    def _dispatch(self, key, meth, *args):
        if not isinstance(key, str):
            raise TypeError('key is not a string')
        expr = ast.parse(key, filename='<key>', mode='eval')
        return meth(key, expr.body, *args)

    def _get(self, key, node):
        meth = getattr(self, f'_get_{node.__class__.__name__}', None)
        if meth is None:
            self._syntax_error(key, node)
        return meth(key, node)

    def _set(self, key, node, value):
        meth = getattr(self, f'_set_{node.__class__.__name__}', None)
        if meth is None:
            self._syntax_error(key, node)
        return meth(key, node, value)

    def _del(self, key, node):
        meth = getattr(self, f'_del_{node.__class__.__name__}', None)
        if meth is None:
            self._syntax_error(key, node)
        return meth(key, node)

    def _get_Name(self, key, node):
        return self.data[node.id]

    def _set_Name(self, key, node, value):
        self.data[node.id] = value

    def _del_Name(self, key, node):
        del(self.data[node.id])

    def _get_Num(self, key, node):
        return node.n

    def _get_Str(self, key, node):
        return node.s

    def _get_Constant(self, key, node):
        return node.value

    def _get_Subscript(self, key, node):
        return self._get(key, node.value)[self._get(key, node.slice)]

    def _set_Subscript(self, key, node, value):
        self._get(key, node.value)[self._get(key, node.slice)] = value

    def _del_Subscript(self, key, node):
        del(self._get(key, node.value)[self._get(key, node.slice)])

    def _get_Slice(self, key, node):
        lower = node.lower and self._get(key, node.lower)
        upper = node.upper and self._get(key, node.upper)
        step = node.step and self._get(key, node.step)
        return slice(lower, upper, step)

    def _get_Index(self, key, node):
        return self._get(key, node.value)

    def _get_Attribute(self, key, node):
        return getattr(self._get(key, node.value), node.attr)

    def _set_Attribute(self, key, node, value):
        setattr(self._get(key, node.value), node.attr, value)

    def _del_Attribute(self, key, node):
        delattr(self._get(key, node.value), node.attr)

    def _get_Tuple(self, key, node):
        return tuple(self._get(key, e) for e in node.elts)

    def _set_Tuple(self, key, node, value):
        i = iter(value)
        n = 0
        for e in node.elts:
            try:
                v = next(i)
            except StopIteration:
                raise ValueError(f'not enough values to unpack '
                                 f'(expected {len(node.elts)}, got {n})')
            self._set(key, e, v)
        try:
            next(i)
        except StopIteration:
            pass
        else:
            raise ValueError(f'too many values to unpack '
                             f'(expected {len(node.elts)})')

    def _del_Tuple(self, key, node):
        for e in node.elts:
            self._del(key, e)

    def _get_List(self, key, node):
        return [self._get(key, e) for e in node.elts]

    def _get_UnaryOp(self, key, node):
        op = getattr(self, f'_op_{node.op.__class__.__name__}', None)
        if op is None:
            self._bad_node(key, node)
        return op(self._get(key, node.operand))

    @staticmethod
    def _op_UAdd(operand):
        return +operand

    @staticmethod
    def _op_USub(operand):
        return -operand

    @staticmethod
    def _op_Not(operand):
        return not operand

    @staticmethod
    def _op_Invert(operand):
        return ~operand
