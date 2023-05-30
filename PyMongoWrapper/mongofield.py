"""Representing fields"""

from typing import Any
from bson import ObjectId, Binary

from .mongobase import MongoFunction, MongoOperand, MongoVariable


class MongoFieldFunction(MongoFunction):
    """Functions on fields"""

    def __init__(self, field_name, func_name):
        super().__init__(func_name)
        self.field_name = MongoField(field_name)()

    def __call__(self, *args, **kwargs):
        func = super().__call__(*args, **kwargs)
        return MongoOperand({
            self.field_name: func()
        })


class MongoField(MongoOperand):
    """Representing fields"""

    def __getattr__(self, fname: str):
        return MongoFieldFunction(self._literal, fname)

    def __neg__(self):
        return MongoField('-' + self())

    def __ne__(self, another: Any):
        return MongoOperand({self(): {'$ne': another}})

    def __eq__(self, another: Any):
        return MongoOperand({self(): another})

    def __gt__(self, another: Any):
        return MongoOperand({self(): {'$gt': another}})

    def __ge__(self, another: Any):
        return MongoOperand({self(): {'$gte': another}})

    def __lt__(self, another: Any):
        return MongoOperand({self(): {'$lt': another}})

    def __le__(self, another: Any):
        return MongoOperand({self(): {'$lte': another}})

    def empty(self):
        """Shortcut to check if the field is empty
        """
        return self.exists(0) | (self == None) | (self == '') | (self == 0) | (self == Binary(b''))

    @staticmethod
    def parse_sort(*sort_args, **sort_kwargs):
        """Parse MongoField objects to sorting

        Returns:
            List[Tuple[str, int]]: Sorting object
        """
        sorts = []
        if sort_kwargs:
            sorts = list(sort_kwargs.items())
        elif sort_args:
            for field in sort_args:
                if isinstance(field, MongoField):
                    field = field()
                if isinstance(field, str):
                    sign = 1
                    if field.startswith('-'):
                        field = field[1:]
                        sign = -1
                    field = F[field]()
                    sorts.append((field, sign))
        return sorts


class MongoIdField(MongoField):
    """Representing _id field"""

    def __init__(self):
        super().__init__('_id')

    def __eq__(self, a):
        return MongoOperand({'_id': ObjectId(a)})

    def __ne__(self, a):
        return MongoOperand({'_id': {'$ne': ObjectId(a)}})

    def __gt__(self, a):
        return MongoOperand({self(): {'$gt': ObjectId(a)}})

    def __ge__(self, a):
        return MongoOperand({self(): {'$gte': ObjectId(a)}})

    def __lt__(self, a):
        return MongoOperand({self(): {'$lt': ObjectId(a)}})

    def __le__(self, a):
        return MongoOperand({self(): {'$lte': ObjectId(a)}})


class MongoOperandFactory:
    """Factory class for MongoOperands
    """

    def __init__(self, class_):
        self.class_ = class_

    def __getattr__(self, name):
        return self[name]

    def __getitem__(self, name):
        return self.class_(MongoOperand.get_repr(name))


F = MongoOperandFactory(MongoField)
F.id = MongoIdField()
Fn = MongoOperandFactory(MongoFunction)
Var = MongoOperandFactory(MongoVariable)
