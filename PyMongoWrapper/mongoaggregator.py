"""Aggregation"""

from .mongobase import MongoOperand
from .mongofield import MongoField, MongoFunction


class MongoAggregatingFunction:
    """Representing aggreagtion pipeline in MongoDB
    """

    def __init__(self, name, aggreagtor):
        self.aggreagtor = aggreagtor
        self.f = MongoFunction(name)

    def __call__(self, *args, **kwargs):
        self.aggreagtor.aggregators.append(self.f(*args, **kwargs)())
        return self.aggreagtor


class MongoAggregator:
    """Aggregator"""

    def __init__(self, performer=None, aggregators=None, raw=False):
        """Initialize an aggregator

        Args:
            performer (DbObject, optional): Bound DbObject to perform aggregation. Defaults to None.
            aggregators (list, optional): Pipeline for aggregation. Defaults to None.
            raw (bool, optional): Returns dict instead of bound DbObject. Defaults to False.
        """
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
        """Perform aggregation

        Args:
            performer (DbObject, optional): Specify performer explictly. Defaults to None.
            raw (bool, optional): Returns dict instead of bound DbObject. Defaults to False.

        Returns:
            Iterable: Iterable MongoAggregator object (self)
        """
        if performer:
            self.performer = performer
        self.raw = raw
        return self

    def __len__(self):
        """Returns the length of aggregation pipeline

        Returns:
            int: Length of aggregation pipeline
        """
        return self.count()

    def count(self):
        """Count results

        Returns:
            int: Number of results matching that aggregation
        """
        agg = list(self.aggregators)
        agg.append({'$group': {'_id': 1, 'count': {'$sum': 1}}})
        try:
            a = next(self.performer.db.aggregate(agg))
            return a['count']
        except StopIteration:
            return 0
