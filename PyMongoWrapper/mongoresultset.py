from .mongobase import MongoOperand
from .mongofield import MongoField


class MongoResultSet:

    def __init__(self, ele_cls, mongo_cond):
        self.ele_cls = ele_cls
        if isinstance(mongo_cond, MongoOperand):
            self.rs = self.ele_cls.db.find(mongo_cond(), no_cursor_timeout=True)
            self.mongo_cond = mongo_cond
        else:
            self.rs = mongo_cond
            self.mongo_cond = None

    def __iter__(self):
        for r in self.rs:
            yield self.ele_cls().fill_dict(r)

    def __len__(self):
        return self.rs.count()

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
        sorts = []
        if sort_kwargs: sorts = list(sort_kwargs.items())
        elif sort_args:
            for s in sort_args:
                if isinstance(s, MongoField):
                    s = s()
                if isinstance(s, str):
                    if s.startswith('-'):
                        sorts.append([s[1:], -1])
                    else:
                        sorts.append([s, 1])
        return MongoResultSet(self.ele_cls, self.rs.sort(sorts))

    def skip(self, offset):
        return MongoResultSet(self.ele_cls, self.rs.skip(offset))

    def limit(self, size):
        return MongoResultSet(self.ele_cls, self.rs.limit(size))

    def count(self):
        return self.rs.count()
