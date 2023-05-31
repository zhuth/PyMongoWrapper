"""DBO module"""

import base64
from collections import deque
from collections.abc import Iterable as IterableClass
import datetime
import re
import threading
from typing import (Any, Callable, Dict, Iterable, List, Optional, Tuple,
                    TypeVar, Union)

import pymongo
import pymongo.collection
from bson import ObjectId

from .mongofield import MongoField

from .mongoaggregator import MongoAggregator
from .mongobase import MongoOperand
from .qxparser import QExprParser
from .mongoresultset import MongoResultSet


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

    def __init__(self,
                 func: Union[None, Callable[[Any],
                                            TypeVar("typ")], type] = None,
                 typ: type = None):
        """Initialize a field for DbObject
        Args:
            func (Union[function, type, None]): the actual function to be called, 
            it should accept one optional argument representing a value to be converted
            typ (type, optional): the retupytrn type of the function, i.e. the type for
            the initialized field. Leave typ to None to skip type checking
        """
        self.func = func
        self.type = typ

    def __call__(self, *args):
        """Call the function to initialize the field"""
        if self.func is None:
            return args[0] if len(args) == 1 else None
        try:
            return self.func(*args)
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
        if copy:
            if isinstance(copy, DbObject):
                self._orig = DbObject._copy(copy._orig)
                self._id = copy._id
            elif isinstance(copy, dict):
                self._orig = DbObject._copy(copy)
                self._id = copy._id
            else:
                raise ValueError(f'Unable to copy from {type(copy).__name__}')
        for field, value in kwargs.items():
            setattr(self, field, value)

    # Allow dict-like access to fields

    def __contains__(self, k: str) -> bool:
        """Check if the object has a field called `k`"""
        return k in self._orig or hasattr(self, k)
    
    def __getitem__(self, k: str) -> Any:
        """Get field according to key"""
        assert isinstance(k, str), 'key must be a string'
        return self.__getattribute__(k)

    def __setitem__(self, k: str, value):
        """Set field value of the object"""
        self.__setattr__(k, value)

    def __delitem__(self, k: str):
        """Delete field from the object"""
        assert isinstance(k, str)
        self.__delattr__(k)

    @classproperty
    def db(cls):
        """Get pymongo cursor for DbObject class"""
        assert cls._binding, 'DbObject must be bound to a MongoConnection instance. Use bind method before use.'
        if hasattr(cls, '_collection'):
            name = cls._collection
        else:
            name = cls.__name__.lower()
        return cls._binding[name]

    @classmethod
    def on_initialize(cls):
        """Executed when initializing DbObject class"""
        pass

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
                if not k.startswith('_') and
                k not in ('db', 'fields', 'ensure_index', 'set_field', 'extended_fields') and
                isinstance(getattr(cls, k), (type, DbObjectInitializer))
            }

            cls.on_initialize()
        return cls._fields

    @classmethod
    def set_field(cls, field, initializer: Union[type, DbObjectInitializer, None]):
        """Set initializer for field"""

        if initializer is None:
            if field in cls.fields:
                del cls.fields[field]
            return

        if isinstance(initializer, type):
            initializer = _DefaultInitializers.get(initializer)
        assert isinstance(initializer, DbObjectInitializer), \
            "initializer must be a type or a DbObjectInitializer, or None to unset."

        cls.fields[field] = initializer

    @classproperty
    def extended_fields(cls) -> Dict[str, type]:
        """Find out fields that refers to other collection"""
        result = {}
        for key, val in cls.fields.items():
            val_type = val.type
            if val_type is DbObjectCollection:
                val_type = val.ele_type
            if not isinstance(val_type, type):
                continue
            if issubclass(val_type, DbObject):
                result[key] = val_type
        return result

    @classmethod
    def ensure_index(cls, *fields: Union[str, MongoOperand]):
        """Ensure index"""
        fields = MongoField.parse_sort(*fields)
        if fields:
            for existent in cls.db.index_information().values():
                if existent['key'] == fields:
                    return
            cls.db.create_index(fields)

    @property
    def id(self) -> Union[ObjectId, None]:
        """Get ID of the object, None if not saved"""
        return self._id

    @id.setter
    def id(self, val):
        """Set ID of the object, None if unset ID"""
        self._id = val
        if val is None and '_id' in self._orig:
            del self._orig['_id']

    def fill_dict(self, filled_with: Dict):
        """Fill the values of the object from a dict"""
        if filled_with:
            self._orig = filled_with
            self._id = filled_with.get('_id')
        return self

    def __getattribute__(self, key: str) -> Any:
        """Get field value of the object if exists, 
        otherwise call the function to initialize the field"""

        assert isinstance(key, str), 'key must be a string'

        if key.startswith('_') or key in self.__dict__:
            return object.__getattribute__(self, key)

        # k is not set yet
        if key in type(self).fields:
            # field is defined

            initializer = type(self).fields[key]
            val = None
            try:
                if self._orig and key in self._orig:
                    # field present in _orig, try convert it to correct type
                    # make a copy first
                    val = self._orig[key]
                    if isinstance(val, list):
                        val = list(val)
                    elif isinstance(val, dict):
                        val = dict(val)

                    if initializer.type and not isinstance(val, initializer.type):
                        # need convertion
                        # now initializer must be a DbObjectInitializer, call it
                        val = initializer(val)
                else:
                    # field not present in _orig, create a new instance
                    val = initializer()
                self[key] = val
            except ValueError:
                raise ValueError(
                    f'Error while handling field {key} of value {val}, ' +
                    f'target type: {initializer.type}')
            return val

        elif key in self._orig:
            # field is not defined, but existing in _orig, so just return it
            val = self._orig[key]
            self[key] = val
            return val

        else:
            # field is not defined, and not existing in _orig, try object
            try:
                return object.__getattribute__(self, key)
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
        """Copy objects"""
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
        
        if '_id' in d and d['_id'] is None:
            del d['_id']
            
        for k in type(self).fields:
            if k not in d or expand:
                d[k] = self[k]
                
        d = {k: v for k, v in d.items() if not k.startswith('_') or k == '_id'}

        for k, v in d.items():
            if isinstance(v, DbObject):
                if expand:
                    d[k] = v.as_dict(expand)
                else:
                    if not v.id:
                        v.save()
                    d[k] = v.id
            elif not isinstance(v, (str, dict, bytes)) and hasattr(v, '__iter__'):
                # if iterable and not dict/str/bytes,
                # convert to list and expand DbObjects if needed
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
        self.db.delete_one({'_id': self.id})
        self._orig = {}

    @classmethod
    def query(cls, *conds: Tuple[Union[Dict, MongoOperand]], logic='and') -> MongoResultSet:
        """Query the database according to a condition"""
        assert logic in ('and', 'or'), "logic must be `and` or `or`"
        if len(conds) == 0:
            d = MongoOperand({})
        elif len(conds) == 1:
            d = MongoOperand(conds[0])
        else:
            d = MongoOperand(
                {'$' + logic: [MongoOperand.literal(cond) for cond in conds]})
        return MongoResultSet(cls, d)

    @classmethod
    def find(cls, *conds) -> MongoResultSet:
        """Alias for query"""
        return cls.query(*conds)

    @classmethod
    def first(cls, *conds: Tuple[Union[Dict, MongoOperand]]):
        """Return the first object in the database matching the condition, None if not found"""
        for p in cls.query(*conds):
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
        """Get initializer for given type

        Args:
            t (Union[None, type, DbObjectInitializer]): type

        Raises:
            TypeError: Cannot specify or convert to that type

        Returns:
            DbObjectInitializer: Initializer for given type
        """

        if isinstance(t, DbObjectInitializer):
            return t

        def _to_bytes(x: Union[str, bytes, None] = None):
            if x is None:
                return b''
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
            if x is None:
                return ObjectId()
            if isinstance(x, ObjectId):
                return x
            elif isinstance(x, str) and re.match(r'^[a-f0-9]{24}$', x):
                return ObjectId(x)
            elif isinstance(x, bytes) and len(bytes) == 12:
                return ObjectId(x.hex())
            raise TypeError(f'Cannot convert {x} to ObjectId')

        def _to_dbobj(cls: type, x: Union[str, bytes, ObjectId, Dict, DbObject, None] = None):
            if x is None:
                return cls()
            if isinstance(x, DbObject):
                return x
            elif isinstance(x, dict):
                return cls().fill_dict(x)
            try:
                return cls.first({'_id': _to_objid(x)})
            except TypeError:
                raise TypeError(f'Cannot convert {x} to {cls.__name__}')

        def _to_datetime(x: Union[str, int, float, ObjectId, datetime.datetime, None] = None):
            if x is None:
                return datetime.datetime.utcnow()
            if isinstance(x, datetime.datetime):
                return x
            elif isinstance(x, ObjectId):
                return x.generation_time
            elif isinstance(x, (float, int)):  # timestamp
                return datetime.datetime.fromtimestamp(x, datetime.timezone.utc)
            elif isinstance(x, str):
                parser = QExprParser(allow_spacing=False)
                return parser.parse_literal(x)
            else:
                raise TypeError(
                    f'Cannot convert {x} of type {type(x)} to datetime')

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
            return DbObjectInitializer(
                lambda *x: t(x[0]) if len(x) == 1 and x[0] is not None else t(), t)


class DbObjectCollection(DbObject, DbObjectInitializer):
    """
    Representing a collection of DbObjects. All elements should be of the same type.
    As a DbObject, it can be embedded in another DbObject.
    As a DbObjectInitializer, it can initialize an empty field, or do convertion by calling it.
    """

    def __init__(self,
                 ele_type: Union[type, DbObjectInitializer],
                 arr: Optional[List] = None,
                 allow_duplicates=True):
        """
        Args:
            ele_type (type): type of elements
            arr (list, optional): Initial value for the collection, with type checking.
                Defaults to None.
            allow_duplicates (bool, optional): Allow duplicate elements in the collection.
                Defaults to True.
        """
        self.ele_type = ele_type
        self._checker = _DefaultInitializers.get(self.ele_type) if isinstance(
            self.ele_type, type) else self.ele_type
        self.type = DbObjectCollection
        self.allow_duplicates = allow_duplicates
        self._orig = []
        for i in arr or []:
            x = self._checker(i)
            if x:
                self._orig.append(x)
        if not self.allow_duplicates:
            self._uniq()

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
        a = DbObjectCollection(self.ele_type, self._orig, self.allow_duplicates)
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
        """Set the element at the index to the value.
        Will raise TypeError if the type is not consistent"""
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

    def __eq__(self, another):
        return self._orig == another

    def __ne__(self, another):
        return self._orig != another

    def remove(self, item_or_index: Union[DbObject, ObjectId, Iterable[ObjectId], int]):
        """Remove the item or index or ObjectIds from the collection"""
        if isinstance(item_or_index, int):
            del self._orig[item_or_index]
        elif isinstance(item_or_index, ObjectId):
            self._orig = [x for x in self._orig if x.id != item_or_index]
        elif isinstance(item_or_index, IterableClass):
            self._orig = [x for x in self._orig if x.id not in item_or_index]
        else:
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
        
    def _uniq(self):
        results = []
        ids = set()
        for ele in self._orig:
            eid = getattr(ele, 'id', ele)
            if eid not in ids:
                ids.add(eid)
                results.append(ele)
        self._orig = results

    def save(self):
        """Save the items to database"""
        if not issubclass(self.ele_type, DbObject):
            return
        if not self.allow_duplicates:
            self._uniq()
        for _ in self._orig:
            _.save()

    def as_dict(self, expand=False):
        """Return a list of element ids (default), or dicts representing elements 
        (expand set to True) in the collection"""
        if not self.allow_duplicates:
            self._uniq()
        if not issubclass(self.ele_type, DbObject):
            return self._orig
        if expand:
            return [_.as_dict(True) for _ in self._orig]
        else:
            return [_.id for _ in self._orig]

    def fill_dict(self, v: List):
        """Fill the collection with elements from a list of dicts, 
        check the type of each element"""
        self._orig = []
        for x in v:
            self.append(x)
        return self
    
    
class BatchOper:
    """Operate multiple documents in batches"""

    def __init__(self, batch_size: int = 100, performer = None) -> None:
        """
        Args:
            batch_size (int, optional): Batch size. Defaults to 100.
            saver (type, optional): Save to DbObject type. Defaults to None, using the type of first available element.
        """
        self.batch_size = batch_size
        self._queue = deque()
        self._lock = threading.Lock()
        self._performer = performer
        
    def __enter__(self, *_):
        return self
    
    def __exit__(self, *_):
        self.commit()
        
    def add(self, obj) -> None:
        """Add object to batch

        Args:
            obj (Union[dict, DbObject]): object
        """        
        if self._performer is None and isinstance(obj, DbObject):
            self._performer = type(obj)
        with self._lock:
            self._queue.append(obj)
        if len(self._queue) > self.batch_size:
            self.commit()
            
    def pop_queue(self):
        with self._lock:
            res = list(self._queue)
            self._queue.clear()
        return res
        
    def commit(self):
        """Commit batch
        """
        pass
    
    @property
    def has_results(self) -> bool:
        """Check if there are any results generated from commit

        Returns:
            bool: True if there are unread results
        """        
        return False
    
    @property
    def results(self):
        """Get unread results
        """        
        return []
        

class BatchSave(BatchOper):
    
    def __init__(self, batch_size: int = 100, performer=None, drop=False) -> None:
        """
        Args:
            batch_size (int, optional): Batch size. Defaults to 100.
            saver (type, optional): Save to DbObject type. Defaults to None, using the type of first available element.
            drop (bool, optional): Drop existent objects with same id before insertion.
                                   Defaults to False. Will raise error for duplicate keys.
        """        
        super().__init__(batch_size, performer)
        self.drop = drop
        
    def commit(self):
        objs = self.pop_queue()
        if objs:
            objs = [x.as_dict() if isinstance(x, DbObject) else x for x in objs]
    
            if self.drop:
                ids = [o['_id'] for o in objs]
                self._performer.query({'_id': {'$in': ids}}).delete()
    
            self._performer.db.insert_many(objs, ordered=False,
                                       bypass_document_validation=True)
        
        
class BatchQuery(BatchOper):
    
    def __init__(self, batch_size: int = 100, performer=None, cond: Callable = lambda x: x, on_query: Callable = lambda x: None) -> None:
        super().__init__(batch_size, performer)
        self._cond = cond
        self._results = []
        self._has_results = False
        self.on_query = on_query
        
    def commit(self):
        objs = self.pop_queue()
        if objs:
            objs = self._cond(objs)
            self._results = self._performer.query(objs)
            self.on_query(self._results)
            self._has_results = True
            
    @property
    def has_results(self) -> bool:
        return self._has_results
    
    @property
    def results(self):
        self._has_results = False
        return self._results


def create_dbo_json_encoder(base_cls):
    """Create a JSON encoder for DbObjects"""

    class DBOJsonEncoder(base_cls):
        """DBO JSON Encoder
        """

        def default(self, o):
            """Overwrite default encoding function"""
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
    """Create a JSON decoder for DbObjects, currently handles only datetime, 
    for other parts are handled by fill_dict"""

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
