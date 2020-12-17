# PyMongoWrapper

Examples:

```python
import time
from PyMongoWrapper import dbo, F
dbo.connstr = 'mongodb://localhost:27017/db'

class Post(dbo.DbObject):
    title = str
    content = str
    pubdate = dbo.DbObjectInitiator(lambda: int(time.time()))
    
    
p = Post(title='Hello', content='Hello World!').save()
print(p.id)

print(p.query(F.title.regex(r'^[A-Z]') & (F.content == 'Hello World!')).count())

print(p.first(F.title == 'Hello'))
```
