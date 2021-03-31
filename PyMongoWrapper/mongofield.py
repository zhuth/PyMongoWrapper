from .mongobase import MongoFunction, MongoOperand
from bson import ObjectId


class MongoFieldFunction(MongoFunction):

    def __init__(self, field_name, func_name):
        super().__init__(func_name)
        self.field_name = field_name
    
    def __call__(self, *args, **kwargs):
        f = super().__call__(*args, **kwargs)
        return MongoOperand({
            self.field_name: f()
        })


class MongoField(MongoOperand):

    def __init__(self, name):
        super().__init__(name)

    def __getattr__(self, fname):
        return MongoFieldFunction(self._literal, fname)

    def __neg__(self):
        return MongoField('-' + self())

    def __ne__(self, a):
        return MongoOperand({self(): {'$ne': a}})

    def __eq__(self, a):
        return MongoOperand({self(): a})

    def empty(self):
        return self.exists(0) | (self == None) | (self == '') | (self == 0)


class MongoIdField(MongoField):

    def __init__(self):
        super().__init__('_id')

    def __eq__(self, a):
        return MongoOperand({'_id': ObjectId(a)})

    def __ne__(self, a):
        return MongoOperand({'_id': {'$ne': ObjectId(a)}})


class MongoOperandFactory:

    def __init__(self, class_):
        self.class_ = class_

    def __getattr__(self, name):
        return self.class_(MongoOperand._repr(name))

    def __getitem__(self, name):
        return self.class_(MongoOperand._repr(name))
        
