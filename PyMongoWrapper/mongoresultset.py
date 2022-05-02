"""Result set"""

from typing import Union
from bson.son import SON
import pymongo.cursor
from .mongobase import MongoOperand
from .mongofield import MongoField


class MongoResultSet:
    """Mongo Result Set
    """

    def __init__(self, ele_cls, mongo_cond: Union[MongoOperand, dict, pymongo.cursor.Cursor], sort=None, limit=None, skip=None):
        """
        Args:
            ele_cls (type): Element
            mongo_cond (Union[MongoOperand, dict, pymongo.cursor.Cursor]): Internal result set or condition for query
            sort (str, optional): Sorting expression. Defaults to None.
            limit (int, optional): Limit the returned results. Defaults to None.
            skip (int, optional): Skip results. Defaults to None.
        """
        self.ele_cls = ele_cls
        if isinstance(mongo_cond, MongoOperand):
            self.result_set = self.ele_cls.db.find(
                mongo_cond(), no_cursor_timeout=True)
            self.mongo_cond = mongo_cond
        elif isinstance(mongo_cond, dict):
            self.result_set = self.ele_cls.db.find(
                mongo_cond, no_cursor_timeout=True)
            self.mongo_cond = MongoOperand(mongo_cond)
        else:
            self.result_set = mongo_cond
            self.mongo_cond = None

        self._sort = sort
        self._limit = limit
        self._skip = skip

    def build_raw_rs(self):
        """Build up raw pymongo cursor
        """

        def _examine_fields(cond, prefix='', targets=[]):
            """Examine whether query condition refers to external collections

            Args:
                cond (dict): MongoDB query
                prefix (str, optional): prefix
                targets (list, optional): targets

            Returns:
                Iterable[str]: Fields that refers to external collection
            """
            targets = set(self.ele_cls.extended_fields.keys()
                          ) if not targets else targets
            ext_fields = []
            if not isinstance(cond, dict):
                return []
            for k in cond:
                k_ = prefix + k
                if k in ('$and', '$or'):
                    for ffs in map(_examine_fields, cond[k]):
                        ext_fields += ffs
                elif k.startswith('$'):
                    continue
                elif '.' in k_ and k_.split('.')[0] in targets:
                    # prefix = '', k_ = k, k in the form of '<field>.<subfield>' where field is extended, True
                    # prefix = <field> where field is extended, k_ = '<field>.<subfield>', True
                    ext_fields.append(k.split('.')[0])
                elif k in targets and _examine_fields(cond[k], k + '.'):
                    ext_fields.append(k)
            return set(ext_fields)

        result_set = self.result_set

        if self.mongo_cond:
            ext_fields = self.ele_cls.extended_fields
            if ext_fields:
                # extended query
                ext_before = list(_examine_fields(self.mongo_cond()))
                ext_after = [_ for _ in ext_fields if _ not in ext_before]
                aggregation = self.ele_cls.aggregator
                for field in ext_before:
                    aggregation.lookup(
                        from_=ext_fields[field].db.name, localField=field, foreignField='_id', as_=field)
                if self.mongo_cond():
                    aggregation.match(self.mongo_cond())
                for field in ext_after:
                    aggregation.lookup(
                        from_=ext_fields[field].db.name, localField=field, foreignField='_id', as_=field)
                result_set = aggregation

        if self._sort is not None:
            if self._sort == [('random', 1)]:
                if isinstance(result_set, pymongo.cursor.Cursor):
                    result_set = self.ele_cls.aggregator.match(
                        MongoOperand(self.mongo_cond)())
                result_set.sample(size=self._limit)
                self._limit = None
            else:
                if isinstance(result_set, pymongo.cursor.Cursor):
                    result_set.sort(self._sort)
                else:
                    result_set.sort(SON(self._sort))

        if self._skip is not None:
            result_set = result_set.skip(self._skip)
        if self._limit is not None:
            result_set = result_set.limit(self._limit)

        return result_set

    def __iter__(self):
        result_set = self.build_raw_rs()
        if not isinstance(result_set, pymongo.cursor.Cursor):
            result_set = result_set.perform(raw=True)

        for result in result_set:
            yield self.ele_cls().fill_dict(result)

    def __len__(self):
        return self.count()

    def first(self):
        """Returns only first result. None if no matched results.
        """
        for r in self:
            return r
        return self.ele_cls()

    def update(self, updt, **update_kwargs):
        """Perform update on current result set.

        Args:
            updt (dict): Update info
        """
        assert self.mongo_cond is not None, 'Must use pure MongoOperand objects'
        updt = MongoOperand(updt)()
        update_kwargs = {MongoOperand._repr(
            k): v for k, v in update_kwargs.items()}
        return self.ele_cls.db.update_many(self.mongo_cond(), updt, **update_kwargs)

    def remove(self):
        """Remove all matched results.
        """
        assert self.mongo_cond is not None, 'Must use pure MongoOperand objects'
        return self.ele_cls.db.remove(self.mongo_cond())

    def delete(self):
        """Delete all matched results. Alias for `remove`.
        """
        return self.remove()

    def sort(self, *sort_args, **sort_kwargs):
        """Sort all matched results
        """
        sorts = MongoField.parse_sort(*sort_args, **sort_kwargs)
        return MongoResultSet(self.ele_cls, self.mongo_cond or self.result_set, sort=sorts)

    def skip(self, offset):
        """Skip offset
        """
        return MongoResultSet(self.ele_cls, self.mongo_cond or self.result_set, sort=self._sort, limit=self._limit, skip=offset)

    def limit(self, size):
        """Limit result count
        """
        return MongoResultSet(self.ele_cls, self.mongo_cond or self.result_set, sort=self._sort, limit=size, skip=self._skip)

    def count(self):
        """Count all matched results, regardless of offset and limit info.
        """
        return self.build_raw_rs().count()
