from PyMongoWrapper import QueryExprParser

p = QueryExprParser(verbose=True, allow_spacing=True, abbrev_prefixes={None: 'tags=', '#': 'source='})


def test_expr(expr, should_be=None):
    print('>', expr)
    e = p.eval(expr)
    if e == should_be:
        print('   ... OK')
    else:
        print(expr)
        print('>>> Get', e)
        if should_be:
            print('>>> Should be', should_be)
    print()


test_expr('#kd,%glass,laugh>=233', {'source': 'kd', 'tags': {'$regex': 'glass', '$options': '-i'}, 'laugh': {'$gte': 233}})

test_expr('%glass,%grass', {'$and': [{'tags': {'$regex': 'glass', '$options': '-i'}}, {'tags': {'$regex': 'grass', '$options': '-i'}}]})

test_expr("(glass|tree),%landscape,(created_at<2020-12-31|images$size=3)", 
    {'$and': [{'$or': [{'tags': 'glass'}, {'tags': 'tree'}], 'tags': {'$regex': 'landscape', '$options': '-i'}}, 
    {'$or': [{'created_at': {'$lt': 1609344000.0}}, {'images': {'$size': 3}}]}]})

test_expr(r'escaped=`\`ab\ncde\\`', {'escaped': '`ab\ncde\\'})

test_expr(r'\u53931234', {'tags': '\u53931234'})

test_expr('单一,%可惜')