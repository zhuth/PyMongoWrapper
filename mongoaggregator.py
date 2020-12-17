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

    def __init__(self, performer=None, aggregators=None):
        self.performer = performer
        self.aggregators = aggregators or list()

    def __getattr__(self, name):
        return MongoAggregatingFunction(name, self)

    def perform(self, performer=None):
        performer = performer or self.performer
        assert performer, 'Must assign a performer'
        return performer.aggregate(self.aggregators, allowDiskUse=True)
