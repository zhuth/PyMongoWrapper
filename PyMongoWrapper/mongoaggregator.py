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

    def __init__(self, performer=None, aggregators=None, raw=False, session=None):
        """Initialize an aggregator

        Args:
            performer (DbObject, optional): Bound DbObject to perform aggregation. Defaults to None.
            aggregators (list, optional): Pipeline for aggregation. Defaults to None.
            raw (bool, optional): Returns dict instead of bound DbObject. Defaults to False.
        """
        self._performer = performer
        self._raw = raw
        self._session = session
        self.aggregators = aggregators or list()

    def __getattr__(self, name):
        return MongoAggregatingFunction(name, self)

    def __iter__(self):
        assert self._performer, 'Must assign a performer'
        for result in self._performer.db.aggregate(self.aggregators, allowDiskUse=True, session=self._session):
            if self._raw:
                yield result
            else:
                yield self._performer().fill_dict(result)

    def perform(self, performer=None, raw=None):
        """Perform aggregation

        Args:
            performer (DbObject, optional): Specify performer explictly. Defaults to None.
            raw (bool, optional): Returns dict instead of bound DbObject. Defaults to None.

        Returns:
            Iterable: Iterable MongoAggregator object (self)
        """
        if performer is not None:
            self._performer = performer
        if raw is not None:
            self._raw = raw
        return self

    def raw(self, raw=True):
        """Set raw flag"""
        self._raw = raw

    def session(self, session=None):
        """Set session"""
        self._session = session

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
            a = next(self._performer.db.aggregate(agg, allowDiskUse=True))
            return a['count']
        except StopIteration:
            return 0
