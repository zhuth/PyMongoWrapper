from .mongobase import MongoOperand
from .mongofield import MongoField, MongoFunction


class MongoAggregatingFunction:

    def __init__(self, name, aggreagtor):
        self.aggreagtor = aggreagtor
        self.f = MongoFunction(name)

    def __call__(self, *args, **kwargs):        
        self.aggreagtor.aggregators.append(self.f(*args, **kwargs)())
        return self.aggreagtor


class MongoAggregator:

    def __init__(self, performer=None, aggregators=None, raw=False):
        self.performer = performer
        self.raw = raw
        self.aggregators = aggregators or list()

    def __getattr__(self, name):
        return MongoAggregatingFunction(name, self)

    def __iter__(self):
        assert self.performer, 'Must assign a performer'
        for r in self.performer.db.aggregate(self.aggregators, allowDiskUse=True):
            if self.raw:
                yield r
            else:
                yield self.performer().fill_dict(r)

    def perform(self, performer=None, raw=False):
        if performer:
            self.performer = performer
        self.raw = raw
        return self
    
    def __len__(self):
        return self.count()

    def count(self):
        agg = list(self.aggregators)
        agg.append({'$group': {'_id': 1, 'count': {'$sum': 1}}})
        try:
            a = next(self.performer.db.aggregate(agg))
            return a['count']
        except StopIteration:
            return 0
