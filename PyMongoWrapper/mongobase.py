"""Representation of operands, functions, and variables"""

import re
from bson import SON


class MongoOperand:
    """Representing an operand"""

    @staticmethod
    def get_repr(name):
        """Convert _ to $ when necessary"""
        if name == '_id':
            return name
        name = re.sub(r'^_+', lambda m: '$'*len(m.group(0)), name)
        name = re.sub(r'_+$', '', name)
        return name

    @staticmethod
    def get_key(arg):
        """Get first key if is string in arg"""
        if not arg:
            return ''
        if isinstance(arg, dict):
            arg, *_ = arg.keys()
        if isinstance(arg, str):
            return arg
        return ''

    @staticmethod
    def add_expr(arg):
        """Convert to expr() when necessary"""
        k = MongoOperand.get_key(arg)
        if k in ('$eq', '$gt', '$ge', '$lt', '$le', '$ne'):
            return {'$expr': arg}
        return arg

    @staticmethod
    def literal(arg):
        if isinstance(arg, MongoOperand):
            return arg()
        return arg

    @staticmethod
    def operand(arg):
        if isinstance(arg, MongoOperand):
            return arg
        return MongoOperand(arg)

    def __init__(self, *literals):
        """Build a MongoOperand

        Args:
            literal (dict|str|float|int|bool): literal value
        """
        assert len(literals) <= 1, 'Must provide 0 or 1 literal value'
        if len(literals) == 0:
            literal = {}
        else:
            literal = literals[0]
        
        literal = MongoOperand.literal(literal)
        if isinstance(literal, (list, tuple, set)):
            literal = [MongoOperand.literal(_) for _ in literal]
        elif isinstance(literal, SON):
            pass
        elif isinstance(literal, dict):
            literal = {MongoOperand.get_repr(k): MongoOperand(
                v)() for k, v in literal.items()}
        self._literal = literal

    def __call__(self):
        return self._literal

    def __and__(self, another):
        another = MongoOperand.add_expr(another)

        def __merge(arg):
            arg = MongoOperand.literal(arg)
            result = dict(self._literal)
            for key, val in arg.items():
                result[key] = val
            return MongoOperand(result)

        def __mergeable(arg):
            if not isinstance(self._literal, dict):
                return False
            arg = MongoOperand.literal(arg)
            for key in arg:
                if key.startswith('$'):
                    return False
                if key in self._literal:
                    return False
            return True

        if isinstance(self._literal, dict) and '$and' in self._literal:
            res = dict(self._literal)
            res['$and'].append(another)
            return MongoOperand(res)
        elif __mergeable(another):
            return __merge(another)

        return MongoOperand({'$and': [self(), another]})

    def __or__(self, another):
        another = MongoOperand.add_expr(another)
        if isinstance(self._literal, dict) and '$or' in self._literal:
            res = dict(self._literal)
            res['$or'].append(another)
            return MongoOperand(res)
        return MongoOperand({'$or': [self(), another]})

    def __invert__(self):
        if not isinstance(self._literal, dict) or not self._literal:
            return MongoOperand({})
        if len([_ for _ in self._literal if not _.startswith('$')]) > 1:
            ors = [~MongoOperand({k_: v_}) for k_, v_ in self._literal.items()]
            return MongoOperand({'$or': [or_() for or_ in ors]})
        else:
            (key, val), *_ = self._literal.items()
            if not key.startswith('$'):
                if isinstance(val, dict):
                    return MongoOperand({key: (~MongoOperand(val))()})
                else:
                    return MongoOperand({key: {'$ne': val}})
            if key == '$and':
                return MongoOperand({'$or': [(~MongoOperand(_))() for _ in val]})
            elif key == '$or':
                return MongoOperand({'$and': [(~MongoOperand(_))() for _ in val]})
            elif key == '$in':
                return MongoOperand({'$nin': val})
            elif key == '$gt':
                return MongoOperand({'$lte': val})
            elif key == '$gte':
                return MongoOperand({'$lt': val})
            elif key == '$lt':
                return MongoOperand({'$gte': val})
            elif key == '$lte':
                return MongoOperand({'$gt': val})
            elif key == '$ne':
                return MongoOperand({'$eq': val})
            elif key == '$eq':
                return MongoOperand({'$ne': val})
            else:
                return MongoOperand({'$not': self._literal})

    def __ne__(self, another):
        return MongoOperand({'$ne': [self(), another]})

    def __eq__(self, another):
        return MongoOperand({'$eq': [self(), another]})

    def __lt__(self, another):
        return MongoOperand({self(): {'$lt': MongoOperand(another)()}})

    def __gt__(self, another):
        return MongoOperand({self(): {'$gt': MongoOperand(another)()}})

    def __lte__(self, another):
        return MongoOperand({self(): {'$lte': MongoOperand(another)()}})

    def __gte__(self, another):
        return MongoOperand({self(): {'$gte': MongoOperand(another)()}})

    def between(self, lower, upper):
        """Shortcut for lower < self <= upper
        """
        return MongoOperand({self(): {'$gt': MongoOperand(lower)(), '$lte': MongoOperand(upper)()}})

    def __repr__(self):
        return f'MongoOperand({repr(self._literal)})'


class MongoVariable(MongoOperand):
    """Representing a variable"""

    def __init__(self, name):
        super().__init__('$' + name)


class MongoFunction(MongoVariable):
    """Representing a function"""

    def __call__(self, *args, **kwargs):
        assert (len(args) > 0) != (len(kwargs) >
                                   0), 'Must choose only one form between args and kwargs'
        if len(args) == 1:
            return MongoOperand({self._literal: MongoOperand(args[0])()})
        elif len(args) > 1:
            return MongoOperand({self._literal: MongoOperand(args)()})
        elif kwargs:
            return MongoOperand({self._literal: MongoOperand(kwargs)()})
