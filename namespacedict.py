# author: Nicolas Tessore <n.tessore@ucl.ac.uk>
# license: MIT

__version__ = '0.1.0'

__all__ = ['NamespaceDict']

import ast


class NamespaceDict:
    def __init__(self, data=None):
        self.data = data if data is not None else {}

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise TypeError('key is not a string')
        expr = ast.parse(key, filename='<key>', mode='eval')
        return self._get(key, expr.body)

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError('key is not a string')
        expr = ast.parse(key, filename='<key>', mode='eval')
        return self._set(key, expr.body, value)

    @staticmethod
    def _bad_node(key, node):
        details = ('<key>', node.lineno, node.col_offset+1, key)
        raise SyntaxError('invalid syntax', details)

    def _get(self, key, node):
        meth = getattr(self, f'_get_{node.__class__.__name__}', None)
        if meth is None:
            self._bad_node(key, node)
        return meth(key, node)

    def _set(self, key, node, value):
        meth = getattr(self, f'_set_{node.__class__.__name__}', None)
        if meth is None:
            self._bad_node(key, node)
        return meth(key, node, value)

    def _get_Name(self, key, node):
        return self.data[node.id]

    def _set_Name(self, key, node, value):
        self.data[node.id] = value

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

    def _get_List(self, key, node):
        return [self._get(key, e) for e in node.elts]

    def _get_UnaryOp(self, key, node):
        return self._unary_op(key, node.op, self._get(key, node.operand))

    def _unary_op(self, key, op, operand):
        meth = getattr(self, f'_unary_op_{op.__class__.__name__}', None)
        if meth is None:
            self._bad_node(key, op)
        return meth(operand)

    def _unary_op_UAdd(self, operand):
        return +operand

    def _unary_op_USub(self, operand):
        return -operand

    def _unary_op_Not(self, operand):
        return not operand

    def _unary_op_Invert(self, operand):
        return ~operand
