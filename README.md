# PyMongoWrapper

This is a simple wrapper for `pymongo`. Its aim is to avoid nesting `dict`s so as to make querying and aggregating easier.

```python
from PyMongoWrapper import F, Fn, Var

F.id # => '_id'
F.id == '5d9f10603a6d92fb73780b4a' # => { '_id': ObjectId('5d9f10603a6d92fb73780b4a') }
F.other_field >= 2 # => { 'other_field': { '$gte' : 2 } }
F.text.regex(r'[a-z]') # => { 'text': { '$regex': '[a-z]' } }
Fn.sum(Var.count) # => { '$sum': '$count' }
```

It also provides a DBO:

```python
import time
from PyMongoWrapper import dbo, F
db = dbo.MongoConnection('mongodb://localhost:27017/db')

class Post(db.DbObject):
    title = str
    content = str
    pubdate = dbo.DbObjectInitializer(lambda: int(time.time()))
    
    
p = Post(title='Hello', content='Hello World!').save()
print(p.id)

print(p.query(F.title.regex(r'^[A-Z]') & (F.content == 'Hello World!')).count())

print(p.first(F.title == 'Hello'))
```

You may use chained expressions to perform aggregation, mixing `Var`, `Fn`, `F` expressions with string literals:

```python
for p in Post.aggregator.match(F.created_at > datetime.datetime(2020, 1, 1).timestamp()).lookup(
            from_='item', localField=F.items, foreignField=F._id, as_=F.items
        ).project(
            _id=1, liked_at=1, created_at=1, source_url=1, tags=1,
            items=Fn.filter(input=Var.items, as_='i', cond=Fn.eq('$$i.flag', 0))
        ).perform():
    ... # deal with p
```

Also, to further simplify query, it contains a `QueryExprParser`. A query expression can be written as follows:

```
(glass|tree),landscape,(created_at<2020-12-31|images$size=3)
```

The interpretation of the expression is customizable, e.g.

```python
from PyMongoWrapper import QueryExprParser
parser = QueryExprParser(abbrev_prefixes={None: 'tags=', '_': 'images.'})
parser.eval("(glass|tree),%landscape,(created_at<2020-12-31|images$size=3|_width>200)")
# => {
#   '$and': [
#       {'$and': [
#           {'$or': [
#               {'tags': 'tree'},
#               {'tags': 'glass'}
#           ]},
#           {'tags': {'$regex': 'landscape', '$options': '-i'}}
#       ]},
#       {'$or': [
#           {'created_at': {'$lt': datetime.datetime(2020, 12, 31, 0, 0)}}
#           {'images': {'$size': 3}},
#           {'images.width': {'$gt': 200}}
#       ]},
#   ]}
parser.eval("`_width>200`")
# {'tags': '_width>200'}
```

Fields named `id` or `_id` will be considered as `ObjectId`, and the following string literal will be converted automatically. You may also enable/disable enforcing the use of timestamp instead of datetime by setting `force_timestamp`. However, query expression does not support things like `width>height` yet, as it will interpret only the first operand as field, and leave the second for literals (numbers, strings, dates rendered as `%Y-%m-%d`). 
