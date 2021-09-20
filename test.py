from PyMongoWrapper.mongobase import MongoOperand
from PyMongoWrapper import QueryExprParser, Fn, MongoOperand, EvaluationError
import json


def _groupby(params):
    if isinstance(params, MongoOperand):
        params = params()
    return Fn.group(orig=Fn.first('$$ROOT'), **params), Fn.replaceRoot(newRoot=Fn.mergeObjects('$orig', {'group_id': '$_id'}, {k: f'${k}' for k in params if k != '_id'}))


p = QueryExprParser(verbose=True, allow_spacing=True, abbrev_prefixes={None: 'tags=', '#': 'source='}, functions={
    'groupby': _groupby
})


def test_expr(expr, should_be=None):
    print('>', expr)
    e = p.eval(expr)
    if e == should_be:
        print('   ... OK')
    else:
        print(expr)
        print('>>> Got:\n', json.dumps(e, ensure_ascii=False, indent=2))
        if should_be:
            print('>>> Should be:\n', json.dumps(should_be, ensure_ascii=False, indent=2))
    print()


test_expr('#kd,%glass,laugh>=233', {'source': 'kd', 'tags': {
          '$regex': 'glass', '$options': '-i'}, 'laugh': {'$gte': 233}})

test_expr('%glass,%grass', {'$and': [{'tags': {
          '$regex': 'glass', '$options': '-i'}}, {'tags': {'$regex': 'grass', '$options': '-i'}}]})

test_expr("(glass|tree),%landscape,(created_at<2020-12-31|images$size=3)",
          {'$and': [{'$or': [{'tags': 'glass'}, {'tags': 'tree'}], 'tags': {'$regex': 'landscape', '$options': '-i'}},
                    {'$or': [{'created_at': {'$lt': 1609344000.0}}, {'images': {'$size': 3}}]}]})

test_expr(r'escaped="\'ab\ncde\\"', {'escaped': '\'ab\ncde\\'})

test_expr(r'\u53931234', {'tags': '\u53931234'})

test_expr('单一,%可惜', {'$and': [{'tags': '单一'}, {
          'tags': {'$regex': '可惜', '$options': '-i'}}]})

test_expr('1;2;`3;`', [1, 2, "3;"])

test_expr('a=()', {'a': {}})

test_expr('a()', {'$a': {}})

test_expr(r'`as\nis`', {'tags': "as\\nis"})

test_expr(r'"`escap\ning\`\'"', {'tags': "`escap\ning`'"})

test_expr('1;2;3;4;', [1,2,3,4])

test_expr('match(tags=aa); \ngroupby(_id=$name,count=sum(1));\nsort(count=-1)', [{'$match': {'tags': 'aa'}}, {'$group': {'orig': {'$first': '$$ROOT'}, '_id': '$name', 'count': {
          '$sum': 1}}}, {'$replaceRoot': {'newRoot': {'$mergeObjects': ['$orig', {'group_id': '$_id'}, {'count': '$count'}]}}}, {'$sort': {'count': -1}}])

test_expr('$ad>$eg', {'$expr': {'$gt': ['$ad', '$eg']}})

test_expr('''
          a;
          b;
          //c; d;e;
          g;
          ''', ['a', 'b', 'g'])

try:
    test_expr('a,')
except EvaluationError as ee:
    print(ee, '... OK')
