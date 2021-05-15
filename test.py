from PyMongoWrapper import QueryExprParser
p = QueryExprParser(verbose=True, allow_spacing=True, abbrev_prefixes={None: 'tags='})
print(p.eval('content!=``,%glass'))
v = p.eval("(glass|tree),landscape,(created_at<2020-12-31|images$size=3)")
print(v)
