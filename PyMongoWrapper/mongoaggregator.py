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
        for i in self.performer.aggregate(self.aggregators, raw=self.raw, allowDiskUse=True):
            yield i

    def perform(self, performer=None, raw=False):
        if performer:
            self.performer = performer
        self.raw = raw
        return self

    def count(self):
        for a in self.group(_id=1, count={'$sum': 1}).perform():
            return a._orig['count']
