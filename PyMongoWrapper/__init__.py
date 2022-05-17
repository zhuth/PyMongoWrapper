"""
PyMongoWrapper: A wrapper for pymongo
"""
from . import dbo
from .mongobase import *
from .mongofield import *
from .queryexprparser import QueryExpressionError, QueryExprParser
from .queryexpreval import QueryExprEvaluator
from .mongoresultset import *

F = MongoOperandFactory(MongoField)
F.id = MongoIdField()
Fn = MongoOperandFactory(MongoFunction)
Var = MongoOperandFactory(MongoVariable)
