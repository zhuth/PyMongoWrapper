import random
import re
import time
import uuid

import pymongo
from bson import SON, ObjectId


class MongoOperand:

    @staticmethod
    def _repr(k):
        if k == '_id': return k
        k = re.sub(r'^_+', lambda m: '$'*len(m.group(0)), k)
        k = re.sub(r'_+$', '', k)
        return k

    def __init__(self, literal):

        if isinstance(literal, MongoOperand):
            literal = literal()
        elif isinstance(literal, (list, tuple)):
            literal = [MongoOperand(_)() for _ in literal]
        elif isinstance(literal, SON):
            literal = literal
        elif isinstance(literal, dict):
            literal = {MongoOperand._repr(k): MongoOperand(
                v)() for k, v in literal.items()}
        self._literal = literal

    def __call__(self):
        return self._literal

    def __and__(self, a):
        def __merge(a):
            if isinstance(a, MongoOperand): a = a()
            r = dict(self._literal)
            for k, v in a.items():
                r[k] = v
            return MongoOperand(r)

        def __mergeable(a):
            if not isinstance(self._literal, dict): return False
            if isinstance(a, MongoOperand): a = a()
            for k in a:
                if k.startswith('$'): return False
                if k in self._literal: return False
            return True

        if isinstance(self._literal, dict) and '$and' in self._literal:
            d = dict(self._literal)
            d['$and'].append(a)
            return MongoOperand(d)
        elif __mergeable(a):
            return __merge(a)

        return MongoOperand({'$and': [self(), a]})

    def __or__(self, a):
        if isinstance(self._literal, dict) and '$or' in self._literal:
            d = dict(self._literal)
            d['$or'].append(a)
            return MongoOperand(d)
        return MongoOperand({'$or': [self(), a]})

    def __invert__(self):
        if not isinstance(self._literal, dict) or not self._literal:
            return MongoOperand({})
        if len([_ for _ in self._literal if not _.startswith('$')]) > 1:
            ors = [~MongoOperand({k_: v_}) for k_, v_ in self._literal.items()]
            return MongoOperand({'$or': [or_() for or_ in ors]})
        else:
            (k_, v_), *_ = self._literal.items()
            if not k_.startswith('$'):
                if isinstance(v_, dict):
                    return MongoOperand({k_: (~MongoOperand(v_))()})
                else:
                    return MongoOperand({k_: {'$ne': v_}})
            if k_ == '$and':
                return MongoOperand({'$or': [(~MongoOperand(_))() for _ in v_]})
            elif k_ == '$or':
                return MongoOperand({'$and': [(~MongoOperand(_))() for _ in v_]})
            elif k_ == '$in':
                return MongoOperand({'$nin': v_})
            elif k_ == '$gt':
                return MongoOperand({'$lte': v_})
            elif k_ == '$gte':
                return MongoOperand({'$lt': v_})
            elif k_ == '$lt':
                return MongoOperand({'$gte': v_})
            elif k_ == '$lte':
                return MongoOperand({'$gt': v_})
            elif k_ == '$ne':
                return MongoOperand({'$eq': v_})
            elif k_ == '$eq':
                return MongoOperand({'$ne': v_})
            else:
                return MongoOperand({'$not': self._literal})
    
    def __ne__(self, a):
        return MongoOperand({'$ne': [self(), a]})

    def __eq__(self, a):
        return MongoOperand({'$eq': [self(), a]})

    def __lt__(self, a):
        return MongoOperand({self(): {'$lt': MongoOperand(a)()}})

    def __gt__(self, a):
        return MongoOperand({self(): {'$gt': MongoOperand(a)()}})

    def __lte__(self, a):
        return MongoOperand({self(): {'$lte': MongoOperand(a)()}})

    def __gte__(self, a):
        return MongoOperand({self(): {'$gte': MongoOperand(a)()}})

    def between(self, lower, upper):
        return MongoOperand({self(): {'$gt': MongoOperand(lower)(), '$lte': MongoOperand(upper)()}})


class MongoVariable(MongoOperand):

    def __init__(self, var_name):
        super().__init__('$' + var_name)


class MongoFunction(MongoVariable):

    def __init__(self, func_name):
        super().__init__(func_name)

    def __call__(self, *args, **kwargs):
        assert (len(args) > 0) != (len(kwargs) > 0), 'Must choose only one form between args and kwargs'
        if len(args) == 1:
            return MongoOperand({self._literal: MongoOperand(args[0])()})
        elif len(args) > 1:
            return MongoOperand({self._literal: MongoOperand(args)()})
        elif kwargs:
            return MongoOperand({self._literal: MongoOperand(kwargs)()})
