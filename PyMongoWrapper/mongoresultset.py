from typing import Union
from bson.son import SON
import pymongo.cursor
from .mongobase import MongoOperand
from .mongofield import MongoField


class MongoResultSet:

    def __init__(self, ele_cls, mongo_cond : Union[MongoOperand, dict, pymongo.cursor.Cursor], sort=None, limit=None, skip=None):
        self.ele_cls = ele_cls
        if isinstance(mongo_cond, MongoOperand):
            self.rs = self.ele_cls.db.find(mongo_cond(), no_cursor_timeout=True)
            self.mongo_cond = mongo_cond
        elif isinstance(mongo_cond, dict):
            self.rs = self.ele_cls.db.find(mongo_cond, no_cursor_timeout=True)
            self.mongo_cond = MongoOperand(mongo_cond)
        else:
            self.rs = mongo_cond
            self.mongo_cond = None
        
        self._sort = sort
        self._limit = limit
        self._skip = skip

    def build_raw_rs(self):

        def __examine_fields(cond, prefix='', targets=[]):
            targets = set(self.ele_cls.extended_fields.keys()) if not targets else targets
            ext_fields = []
            if not isinstance(cond, dict):
                return []
            for k in cond:
                k_ = prefix + k
                if k in ('$and', '$or'):
                    for ffs in map(__examine_fields, cond[k]):
                        ext_fields += ffs
                elif k.startswith('$'):
                    continue
                elif '.' in k_ and k_.split('.')[0] in targets:
                    # prefix = '', k_ = k, k in the form of '<field>.<subfield>' where field is extended, True
                    # prefix = <field> where field is extended, k_ = '<field>.<subfield>', True
                    ext_fields.append(k.split('.')[0])
                elif k in targets and __examine_fields(cond[k], k + '.'):
                    ext_fields.append(k)
            return set(ext_fields)

        rs = self.rs

        if self.mongo_cond:
            ext_fields = self.ele_cls.extended_fields
            if ext_fields:
                # extended query
                ext_before = list(__examine_fields(self.mongo_cond()))
                ext_after = [_ for _ in ext_fields if _ not in ext_before]
                ag = self.ele_cls.aggregator
                for f in ext_before:
                    ag.lookup(from_=ext_fields[f].db.name, localField=f, foreignField='_id', as_=f)
                if self.mongo_cond():
                    ag.match(self.mongo_cond())
                for f in ext_after:
                    ag.lookup(from_=ext_fields[f].db.name, localField=f, foreignField='_id', as_=f)
                rs = ag

        if self._sort is not None: 
            if self._sort == [('random', 1)]:
                if isinstance(rs, pymongo.cursor.Cursor):
                    rs = self.ele_cls.aggregator.match(MongoOperand(self.mongo_cond)())
                rs.sample(size=self._limit)
                self._limit = None
            else:
                if isinstance(rs, pymongo.cursor.Cursor):
                    rs.sort(self._sort)
                else:
                    rs.sort(SON(self._sort))
        
        if self._skip is not None:
            rs = rs.skip(self._skip)
        if self._limit is not None:
            rs = rs.limit(self._limit)

        return rs

    def __iter__(self):
        rs = self.build_raw_rs()
        if not isinstance(rs, pymongo.cursor.Cursor):
            rs = rs.perform(raw=True)

        for r in rs:
            yield self.ele_cls().fill_dict(r)

    def __len__(self):
        return self.count()

    def first(self):
        for r in self:
            return r
        return self.ele_cls()

    def update(self, updt, **update_kwargs):
        assert self.mongo_cond is not None, 'Must use pure MongoOperand objects'
        updt = MongoOperand(updt)()
        update_kwargs = {MongoOperand._repr(k): v for k, v in update_kwargs.items()}
        return self.ele_cls.db.update_many(self.mongo_cond(), updt, **update_kwargs)

    def remove(self):
        assert self.mongo_cond is not None, 'Must use pure MongoOperand objects'
        return self.ele_cls.db.remove(self.mongo_cond())

    def delete(self):
        return self.remove()

    def sort(self, *sort_args, **sort_kwargs):
        sorts = MongoField.parse_sort(*sort_args, **sort_kwargs)
        return MongoResultSet(self.ele_cls, self.mongo_cond or self.rs, sort=sorts)

    def skip(self, offset):
        return MongoResultSet(self.ele_cls, self.mongo_cond or self.rs, sort=self._sort, limit=self._limit, skip=offset)

    def limit(self, size):
        return MongoResultSet(self.ele_cls, self.mongo_cond or self.rs, sort=self._sort, limit=size, skip=self._skip)

    def count(self):
        return self.build_raw_rs().count()
        