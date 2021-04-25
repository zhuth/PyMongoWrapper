from PyMongoWrapper import QueryExprParser
p = QueryExprParser(verbose=True, allow_spacing=True, abbrev_prefixes={None: 'tags='})
v = p.eval('match(a,b,c)=>proj(s=1)=>def(ax:ja)')
print(v)
