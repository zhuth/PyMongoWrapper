# PyMongoWrapper

PyMongoWrapper is a Python library that provides a convenient wrapper for PyMongo, allowing for LINQ-style querying, enhanced database object handling, and support for a new query language called `QExpr`.

## Installation

To install PyMongoWrapper, use pip:

```shell
pip install PyMongoWrapper
```

## Features

- LINQ-style querying: PyMongoWrapper simplifies the process of querying MongoDB by providing a LINQ-inspired syntax that allows for expressive and intuitive queries.

- Enhanced database object handling: PyMongoWrapper extends the functionality of PyMongo by introducing additional methods and utilities for working with database objects, making it easier to interact with MongoDB collections.

- New query language support: PyMongoWrapper introduces a new query language that avoids nested dictionary when interacting with MongoDB. This language provides advanced features and syntax to enable more powerful and flexible queries.

## Usage

### Connecting to a MongoDB database

To connect to a MongoDB database using PyMongoWrapper, you can use the following code:

```python
from PyMongoWrapper import dbo

# Connect to the MongoDB server
db = dbo.MongoConnection('mongodb://localhost:27017/db')
```

### Querying the database

PyMongoWrapper provides a LINQ-style syntax for querying MongoDB. Here's an example of how to use it:

```python
import time

# create a class called Post, which maps to the `post` collection in MongoDB
class Post(db.DbObject):
    title = str
    author = str
    content = str
    pubdate = dbo.DbObjectInitializer(lambda: int(time.time()), int)
    
    
# let's create a post!
p = Post(title='Hello', content='Hello World!').save() # => equivalent to `p = Post(...); p.save()`
print(p.id) # => ObjectId for the newly created post
print(p.pubdate) # => Timestamp when Post instance is created
```

### Additional methods and utilities

PyMongoWrapper introduces additional methods and utilities to simplify working with database objects. Here are a few examples:

```python
from PyMongoWrapper import F, Fn, Var

F.id # => '_id'
F.id == '5d9f10603a6d92fb73780b4a' # => { '_id': ObjectId('5d9f10603a6d92fb73780b4a') }
F.other_field >= 2 # => { 'other_field': { '$gte' : 2 } }
F.text.regex(r'[a-z]') # => { 'text': { '$regex': '[a-z]' } }
Fn.sum(Var.count) # => { '$sum': '$count' }
```

### Using the query language

PyMongoWrapper introduces a query language called QExpr, which provides more features for more powerful and flexible queries. Here's an example:
```python
from PyMongoWrapper import QExprInterpreter
parser = QExprInterpreter(default_field='tags', default_operator='=')
parser.eval("(glass|tree),%landscape,(created_at<d'2020-12-31'|images=size(3)|images.width>200)")
# The above expression is equivalent to the following native MongoDB Query
# {'$and': [
#       {'$and': [
#           {'$or': [
#               {'tags': 'tree'},
#               {'tags': 'glass'}
#           ]},
#           {'tags': {'$regex': 'landscape', '$options': '-i'}}
#       ]},
#       {'$or': [
#           {'created_at': {'$lt': new Date(2020, 12, 31, 0, 0)}}
#           {'images': {'$size': 3}},
#           {'images.width': {'$gt': 200}}
#       ]},
#   ]}
```

Basically, you may speicify a query in favor of function calls and operators. It supports the use of

- arithmetic operators: `+`, `-`, `*`, `/`
- relational operators: `=`, `>`, `<`, `>=`, `<=`, `!=`
- logical operators: `~` (not), `&`, `|`, `,` (as an alias for `&` in contexts other than function calls)
- array operators: `;` and `=>` for concatenation

and function calls including

- native MongoDB aggregation pipelines and operators, such as `match`, `project`, `addFields`, `regexFindAll`, etc.
- builtin functions to simplify query, like `joinStr` (join an array of values to one string), `sorted` (sort array), `now` (a `Date` representing current time in UTC) etc.
- user defined functions.


### Using shortcuts and user defined functions

QExpr allows you to specify shortcuts for any separable part of the query. For instance, if you perform query for `pdate>now(-3d);sort(title);` quite often, you may specify a shortcut for it:

```python
parser.set_shortcut('title3', 'pdate>now(-3d);project(title=1);sort(title);')
```

and any query like `:title3` will resolve to the specified expression.

Shortcuts may be used like a function. For example, we may define the following shortcut for a grouping query:

```C#
:groups {
    group(id=$arg, posts=addToSet($$ROOT), count=sum(1));
    sort(-count);
 }
```

and by calling 

```python
'groups($author)'
```

The query will resolve to the equivalent of

```python
'group(id=$author, posts=addToSet($$ROOT), count=sum(1)); sort(-count);'
```

This is called parse-time functions. Runtime functions on other hand, functions in another way. The following snippet of QExpr defines a function that calculates Fibonacci series:

```C#
:fib {
    if ($arg <= 2) return 1; 
    return fib@($arg - 1) + fib@($arg - 2);
}
```

The extra `@` suffix specify that this function call should not be resolved in parse-time. By calling `execute` method of a `QExprEvaluator`, we may get the result of running this function:

```python
parsed = parser.parse('''
    :fib {
        if ($arg <= 2) return 1; 
        return fib@($arg - 1) + fib@($arg - 2);
    }
    return fib@($num);
''')
evaulator = QExprEvaluator()
evaluator.execute(parsed, {'num': 6}) 
print(result) # => get 8
```

For more information and detailed usage examples, please refer to `QExpr.g` and `README-QExpr.md`.

## Contribution

Contributions to PyMongoWrapper are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on the [GitHub repository](https://github.com/zhuth/PyMongoWrapper). You can also submit pull requests with new features or bug fixes.

## License

PyMongoWrapper is released under the MIT License. See the [LICENSE](https://github.com/zhuth/PyMongoWrapper/blob/master/LICENSE) file for more details.
