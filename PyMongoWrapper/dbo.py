import time
import random
import pymongo
from bson import ObjectId

from .mongobase import MongoOperand
from .mongoaggregator import MongoAggregator
from .mongoresultset import MongoResultSet

CURSORS = {}

connstr = ''

def mongodb(name):
    assert connstr, 'Must set `dbo.connstr` first.'
    if name not in CURSORS:
        CURSORS[name] = pymongo.MongoClient(connstr)[connstr.split('/')[-1]][name]
    return CURSORS[name]


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class DbObjectInitiator:

    def __init__(self, func):
        self.f = func

    def __call__(self):
        return self.f()


class DbObject:

    _fields = []

    def __init__(self, **kwargs):
        self._orig = {}
        self._id = None
        self.__dict__.update(**kwargs)

    def __getitem__(self, key):
        assert isinstance(key, str)
        if hasattr(self, key): return getattr(self, key)
        raise KeyError

    @classproperty
    def db(cls):
        if hasattr(cls, '_collection'): name = cls._collection
        else: name = cls.__name__.lower()
        return mongodb(name)

    @classproperty
    def fields(cls):
        if not cls._fields:
            cls._fields = list(set([
                k for k in dir(cls)
                if not k.startswith('_') and k != 'fields' and isinstance(
                    getattr(cls, k), (type, DbObjectInitiator)
                )]))
        return cls._fields

    @property
    def id(self):
        return self._id

    def fill_dict(self, d):
        if d:
            self._orig = d
            self._id = d.get('_id')
        return self

    def __getattribute__(self, k):
        if k in type(self).fields and k not in self.__dict__:
            initiator = type(self).__dict__[k]
            if self._orig and k in self._orig:
                v = self._orig[k]
                if isinstance(v, bytes):
                    v = ''.join(['%02x' % _ for _ in v])
                elif isinstance(v, list):
                    v = list(v)
                elif isinstance(v, dict):
                    v = dict(v)
                if isinstance(initiator, DbObject) and v:
                    if isinstance(v, str) and len(v) == 24:
                        v = ObjectId(v)
                    if isinstance(v, ObjectId):
                        v = initiator.db.find_one({'_id': v})
                    elif isinstance(v, list) and v and isinstance(v[0], ObjectId):
                        v = initiator.db.find({'_id': {'$in': v}})
                    v = initiator().fill_dict(v)
            else:
                v = initiator()
            setattr(self, k, v)
            return v
        else:
            return object.__getattribute__(self, k)

    def as_dict(self, expand=False):
        d = dict(self._orig)
        d.update(**self.__dict__)
        if '_orig' in d: del d['_orig']
        if '_id' in d and d['_id'] is None: del d['_id']

        for k in type(self).fields:
            if k not in d:
                d[k] = type(self).__dict__[k]()

        for k, v in d.items():
            if k.startswith('_') or not isinstance(type(self).__dict__.get(k, object), (type, DbObjectInitiator)):
                continue
            d[k] = v
            if isinstance(d[k], DbObject):
                if expand:
                    d[k] = d[k].as_dict(expand)
                else:
                    if not d[k].id: d[k].save()
                    d[k] = d[k].id
            elif isinstance(d[k], list):
                d[k] = [(_.as_dict(expand) if expand else _.id) if isinstance(_, DbObject) else _ for _ in d[k]]

        return d

    def save(self):
        d = self.as_dict()
        if self._orig and self._orig.get('_id'):
            for k, v in self._orig.items():
                if k in d and d[k] == v:
                    del d[k]
            if d:
                self.db.update_one(
                    {'_id': self._orig['_id']}, {'$set': d})
            d['_id'] = self._orig['_id']
        else:
            d['_id'] = self.db.insert_one(d).inserted_id
            self._id = d['_id']
            self._orig = d
        return self

    def delete(self):
        self.db.remove({'_id': self.id})
        self._orig = {}

    @classmethod
    def query(cls, cond : MongoOperand):
        d = MongoOperand(cond)
        return MongoResultSet(cls, d)
        
    @classmethod
    def first(cls, cond : MongoOperand):
        for p in cls.query(cond):
            return p

    @classproperty
    def aggregator(cls):
        return MongoAggregator(cls)

    @classmethod
    def aggregate(cls, aggregates, raw=False, **kwargs):
        for r in cls.db.aggregate(aggregates, **kwargs):
            if raw:
                yield r
            else:
                yield cls().fill_dict(r)


class DbObjectCollection(DbObject, DbObjectInitiator):

    def __init__(self, eleType, arr=None):
        self.eleType = eleType
        self.a = arr or list()
        self.db = self.eleType.db

    def __call__(self):
        return DbObjectCollection(self.eleType)

    def append(self, v):
        self.a.append(v)

    def clear(self):
        self.a = list()

    def __getitem__(self, idx):
        return self.a[idx]

    def __setitem__(self, idx, v):
        self.a[idx] = v

    def __iter__(self):
        return self.a.__iter__()

    def __contains__(self, item):
        return item in self.a

    def remove(self, item):
        return self.a.remove(item)

    @property
    def id(self):
        for _ in self.a:
            if not _.id: _.save()
        return [_.id for _ in self.a]

    def save(self):
        for _ in self.a:
            _.save()

    def as_dict(self, expand=False):
        return [_.as_dict(expand) for _ in self.a]

    def fill_dict(self, v):
        self.a = [self.eleType().fill_dict(_) if isinstance(_, dict) else _ for _ in v]
        return self


def create_dbo_json_encoder(base_cls):
    class DBOJsonEncoder(base_cls):

        def default(self, o):
            if isinstance(o, bytes):
                return ''.join(['%02x' % _ for _ in o])
            if isinstance(o, ObjectId):
                return str(o)
            if isinstance(o, DbObject):
                return o.as_dict()
            else:
                return base_cls.default(self, o)
    return DBOJsonEncoder
    