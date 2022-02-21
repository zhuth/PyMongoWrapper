import datetime
from typing import Any, Callable, Dict, Iterable, List, Optional, TypeVar, Union
import pymongo
import pymongo.collection
from bson import ObjectId
import base64
import re

from .mongobase import MongoOperand
from .mongoaggregator import MongoAggregator
from .mongoresultset import MongoResultSet
from .mongoqueryexpr import QueryExprParser


class classproperty(object):
    """Provide class-specific property"""

    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class MongoConnection:
    """Provide Mongo connection object"""

    def __init__(self, connstr: str) -> None:
        """Initialize a MongoDB connection

        Args:
            connstr (str): MongoDB connection string
        """
        self.connstr = connstr
        self.cursors = {}
        self.db = pymongo.MongoClient(self.connstr)[
            self.connstr.split('/')[-1]]

    def __getitem__(self, name: str) -> pymongo.collection.Collection:
        """Get pymongo db collection object by name

        Args:
            name (str): collection name

        Returns:
            pymongo.collection.Collection: collection object
        """
        if name not in self.cursors:
            self.cursors[name] = self.db[name]
        return self.cursors[name]

    @property
    def DbObject(self):
        """Bound DbObject

        Returns:
            type: Bound DbObject class for this connection
        """
        class _BoundDbObject(DbObject):
            pass
        return _BoundDbObject.bind(self)


class DbObjectInitializer:
    """Initialize a field for DbObject"""

    def __init__(self, func: Union[None, Callable[[Any], TypeVar("typ")], type] = None, typ: type = None):
        """Initialize a field for DbObject
        Args:
            func (Union[function, type, None]): the actual function to be called, it should accept one optional argument representing a value to be converted
            typ (type, optional): the retupytrn type of the function, i.e. the type for the initialized field. Leave typ to None to skip type checking
        """
        self.f = func
        self.type = typ

    def __call__(self, *args):
        """Call the function to initialize the field"""
        if self.f is None:
            return args[0] if len(args) == 1 else None
        try:
            return self.f(*args)
        except Exception as ex:
            raise ValueError(f'Unable to call initializer for {self.type}', ex)


class DbObject:
    """Provide a base class for DB objects"""

    _fields = None

    _binding = None

    def __init__(self, copy=None, **kwargs):
        """Initialize the object fields"""
        self._orig = {}
        self._id = None
        if copy and isinstance(copy, DbObject):
            self._orig = DbObject._copy(copy._orig)
            self._id = copy._id
        self.__dict__.update(**kwargs)

    # Allow dict-like access to fields
    def __getitem__(self, k: str) -> Any:
        """Get field according to key"""
        assert isinstance(k, str), 'key must be a string'
        return self.__getattribute__(k)
    
    def __setitem__(self, k : str, value):
        """Set field value of the object"""
        self.__setattr__(k, value)

    @classproperty
    def db(cls):
        assert cls._binding, 'DbObject must be bound to a MongoConnection instance. Use bind method before use.'
        if hasattr(cls, '_collection'):
            name = cls._collection
        else:
            name = cls.__name__.lower()
        return cls._binding[name]

    @classmethod
    def bind(cls, conn: MongoConnection):
        """Bind a MongoConnection instance to this DbObject class"""
        cls._binding = conn
        return cls

    @classproperty
    def fields(cls) -> List[str]:
        """Get defined fields of the object"""
        if not cls._fields:
            cls._fields = {
                k: _DefaultInitializers.get(getattr(cls, k)) for k in dir(cls)
                if not k.startswith('_') and k not in ('db', 'fields') and isinstance(
                    getattr(cls, k), (type, DbObjectInitializer)
                )}
        return cls._fields

    @property
    def id(self) -> Union[ObjectId, None]:
        """Get ID of the object, None if not saved"""
        return self._id

    def fill_dict(self, d: Dict):
        """Fill the values of the object from a dict"""
        if d:
            self._orig = d
            self._id = d.get('_id')
        return self

    def __getattribute__(self, k: str) -> Any:
        """Get field value of the object if exists, otherwise call the function to initialize the field"""

        assert isinstance(k, str), 'key must be a string'

        if k.startswith('_') or k in self.__dict__:
            return object.__getattribute__(self, k)

        # k is not set yet
        if k in type(self).fields:
            # field is defined

            initializer = type(self).fields[k]
            v = None
            try:
                if self._orig and k in self._orig:
                    # field present in _orig, try convert it to correct type
                    # make a copy first
                    v = self._orig[k]
                    if isinstance(v, list):
                        v = list(v)
                    elif isinstance(v, dict):
                        v = dict(v)

                    if initializer.type and not isinstance(v, initializer.type):
                        # need convertion
                        # now initializer must be a DbObjectInitializer, call it
                        v = initializer(v)
                else:
                    # field not present in _orig, create a new instance
                    v = initializer()
                setattr(self, k, v)
            except ValueError:
                raise ValueError(f'Error while handling field {k} of value {v}, target type: {initializer.type}')
            return v

        elif k in self._orig:
            # field is not defined, but existing in _orig, so just return it
            v = self._orig[k]

            setattr(self, k, v)
            return v

        else:
            # field is not defined, and not existing in _orig, try object
            try:
                return object.__getattribute__(self, k)
            except AttributeError:
                return None

    def __setattr__(self, key: str, value: Any) -> None:
        """Set field value of the object"""
        if key in type(self).fields:
            # field is defined, so set it and convert to correct type if needed
            initializer = type(self).fields[key]
            if initializer.type and not isinstance(value, initializer.type):
                value = initializer(value)

        object.__setattr__(self, key, value)

    @staticmethod
    def _copy(x):
        if isinstance(x, list):
            return [DbObject._copy(r) for r in x]
        elif isinstance(x, dict):
            return {k: DbObject._copy(v) for k, v in x.items()}
        else:
            return x

    def as_dict(self, expand=False) -> Dict:
        """Export the object as a dict"""

        d = dict(self._orig)
        d.update(**self.__dict__)
        if '_orig' in d:
            del d['_orig']
        if '_id' in d and d['_id'] is None:
            del d['_id']

        for k in type(self).fields:
            if k not in d or expand:
                d[k] = self[k]

        for k, v in d.items():
            if isinstance(v, DbObject):
                if expand:
                    d[k] = v.as_dict(expand)
                else:
                    if not v.id:
                        v.save()
                    d[k] = v.id
            elif not isinstance(d[k], (str, dict, bytes)) and hasattr(d[k], '__iter__'):
                # if iterable and not dict/str/bytes, convert to list and expand DbObjects if needed
                d[k] = [(_.as_dict(expand) if expand else _.id)
                        if isinstance(_, DbObject) else _ for _ in v]

        return d

    def save(self):
        """Save the current object to database"""
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
        
        self._orig.update(**DbObject._copy(d))

        return self

    def delete(self):
        """Delete the current object from database"""
        self.db.remove({'_id': self.id})
        self._orig = {}

    @classmethod
    def query(cls, cond : Union[Dict, MongoOperand] = {}) -> MongoResultSet:
        """Query the database according to a condition"""
        d = MongoOperand(cond)
        return MongoResultSet(cls, d)

    @classmethod
    def first(cls, cond: MongoOperand):
        """Return the first object in the database matching the condition, None if not found"""
        for p in cls.query(cond):
            return p

    @classproperty
    def aggregator(cls) -> MongoAggregator:
        """Get a MongoAggregator instance for this class"""
        return MongoAggregator(cls)

    @classmethod
    def aggregate(cls, aggregates, raw=False, **kwargs):
        """Perform an aggregation query on this class"""
        return MongoAggregator(cls, aggregates, raw)


Anything = DbObjectInitializer()


class _DefaultInitializers:
    """Default initializers. Specifically, `None` means accept everything"""

    @staticmethod
    def get(t: Union[None, type, DbObjectInitializer]) -> DbObjectInitializer:

        if isinstance(t, DbObjectInitializer): return t

        def _to_bytes(x: Union[str, bytes, None] = None):
            if x is None: return b''
            if isinstance(x, bytes):
                return x
            elif isinstance(x, str):
                if re.match(r'^[a-f0-9]+$', x) and len(x) % 2 == 0:
                    return bytes.fromhex(x)
                else:
                    return x.encode('utf-8')
            elif isinstance(x, int):
                return bytes.fromhex(f'{x:016x}')
            else:
                raise TypeError(f'Cannot convert {x} to bytes')

        def _to_objid(x: Union[str, bytes, ObjectId, None] = None) -> ObjectId:
            if x is None: return ObjectId()
            if isinstance(x, ObjectId):
                return x
            elif isinstance(x, str) and re.match(r'^[a-f0-9]{24}$', x):
                return ObjectId(x)
            elif isinstance(x, bytes) and len(bytes) == 12:
                return ObjectId(x.hex())
            raise TypeError(f'Cannot convert {x} to ObjectId')

        def _to_dbobj(cls: type, x: Union[str, bytes, ObjectId, Dict, DbObject, None] = None):
            if x is None: return cls()
            if isinstance(x, DbObject):
                return x
            elif isinstance(x, dict):
                return cls().fill_dict(x)
            try:
                return cls.first({'_id': _to_objid(x)})
            except TypeError:
                raise TypeError(f'Cannot convert {x} to {cls.__name__}')

        def _to_datetime(x: Union[str, int, float, ObjectId, datetime.datetime, None] = None):
            if x is None: return datetime.datetime.utcnow()
            if isinstance(x, datetime.datetime):
                return x
            elif isinstance(x, ObjectId):
                return x.generation_time
            elif isinstance(x, (float, int)): # timestamp
                return datetime.datetime.fromtimestamp(x, datetime.timezone.utc)
            elif isinstance(x, str):
                parser = QueryExprParser(allow_spacing=False)
                return parser.parse_literal(x)
            else:
                raise TypeError(f'Cannot convert {x} of type {type(x)} to datetime')

        if t is None:
            return DbObjectInitializer()
        elif t is bytes:
            return DbObjectInitializer(_to_bytes, bytes)
        elif t is ObjectId:
            return DbObjectInitializer(_to_objid, ObjectId)
        elif t is datetime.datetime:
            return DbObjectInitializer(_to_datetime, datetime.datetime)
        elif issubclass(t, DbObject):
            return DbObjectInitializer(lambda *x: _to_dbobj(t, *x), t)
        else:
            return DbObjectInitializer(lambda *x: t(x[0]) if len(x) == 1 and x[0] is not None else t(), t)


class DbObjectCollection(DbObject, DbObjectInitializer):
    """
    Representing a collection of DbObjects. All elements should be of the same type.
    As a DbObject, it can be embedded in another DbObject.
    As a DbObjectInitializer, it can initialize an empty field, or do convertion by calling it.
    """

    def __init__(self, ele_type: Union[type, DbObjectInitializer], arr: Optional[List] = None, allow_duplicates=True):
        """
        Args:
            ele_type (type): type of elements
            arr (list, optional): Initial value for the collection, with type checking. Defaults to None.
            allow_duplicates (bool, optional): Allow duplicate elements in the collection. Defaults to True.
        """
        self.ele_type = ele_type
        self._checker = _DefaultInitializers.get(self.ele_type) if isinstance(self.ele_type, type) else self.ele_type
        self.type = DbObjectCollection
        self._orig = []
        for i in arr or []:
            x = self._checker(i)
            if x: self._orig.append(x)
        self.allow_duplicates = allow_duplicates

    def __call__(self, arr: Optional[Iterable] = None):
        """Initialize a new collection of the same type"""
        return DbObjectCollection(self.ele_type, arr, self.allow_duplicates)
        
    def append(self, v):
        """Append an element to the collection if it passes the type check"""
        v = self._checker(v)
        if self.allow_duplicates or v not in self._orig:
            self._orig.append(v)

    def clear(self):
        """Clear the collection"""
        self._orig = list()

    def __add__(self, lst: Iterable):
        """Combine an iterable (list, set, etc.) to a new collection"""
        a = DbObjectCollection(self.ele_type, self._orig)
        for i in lst:
            a.append(i)
        return a

    def __len__(self):
        """Return the length of the collection"""
        return len(self._orig)

    def __getitem__(self, idx: int):
        """Get an element from the collection according to index"""
        return self._orig[idx]

    def __setitem__(self, idx: int, v: Union[ObjectId, Dict, DbObject]):
        """Set the element at the index to the value. Will raise TypeError if the type is not consistent"""
        v = self._checker(v)
        if not v:
            raise TypeError(f'{v} is not of type {self.ele_type}')
        self._orig[idx] = v

    def __iter__(self):
        """Iterate over the collection"""
        return self._orig.__iter__()

    def __contains__(self, item):
        """Check if the collection contains the item"""
        return item in self._orig

    def remove(self, item_or_index: Union[DbObject, int]):
        """Remove the item or index from the collection"""
        if isinstance(item_or_index, int):
            del self._orig[item_or_index]
        elif isinstance(item_or_index, self.ele_type):
            self._orig.remove(item_or_index)

    @property
    def id(self):
        """Get the ids of elements in the collection, and save them if necessary"""
        if issubclass(self.ele_type, DbObject):
            for _ in self._orig:
                if not _.id:
                    _.save()
            return [_.id for _ in self._orig]
        else:
            return self._orig

    def save(self):
        """Save the items to database"""
        if not issubclass(self.ele_type, DbObject):
            return
        if not self.allow_duplicates:
            self._orig = list(set(self._orig))
        for _ in self._orig:
            _.save()

    def as_dict(self, expand=False):
        """Return a list of element ids (default), or dicts representing elements (expand set to True) in the collection"""
        if not issubclass(self.ele_type, DbObject):
            return self._orig
        if expand:
            return [_.as_dict(True) for _ in self._orig]
        else:
            return [_.id for _ in self._orig]

    def fill_dict(self, v: List):
        """Fill the collection with elements from a list of dicts, check the type of each element"""
        self._orig = []
        for x in v:
            self.append(x)
        return self


def create_dbo_json_encoder(base_cls):
    """Create a JSON encoder for DbObjects"""

    class DBOJsonEncoder(base_cls):
        def default(self, o):
            if isinstance(o, bytes):
                return o.hex()
            if isinstance(o, ObjectId):
                return str(o)
            elif isinstance(o, DbObject):
                return o.as_dict()
            elif isinstance(o, datetime.datetime):
                return o.isoformat()
            elif isinstance(o, bytes):
                return f'{base64.b64encode(o).decode("ascii")}'
            else:
                return base_cls.default(self, o)
    return DBOJsonEncoder


def create_dbo_json_decoder(base_cls):
    """Create a JSON decoder for DbObjects, currently handles only datetime, for other parts are handled by fill_dict"""

    class JsonDecoder(base_cls):
        def __init__(self, *args, **kargs):
            _ = kargs.pop('object_hook', None)
            super().__init__(object_hook=self.decoder, *args, **kargs)

        def decoder(self, d):
            import dateutil.parser
            updt = {}
            for k, v in d.items():
                if isinstance(v, str):
                    if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z?$', v):
                        updt[k] = dateutil.parser.isoparse(v)
            if updt:
                d.update(**updt)
            return d

    return JsonDecoder
