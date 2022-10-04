from PyMongoWrapper.mongobase import MongoOperand
from PyMongoWrapper import QueryExprParser, Fn, MongoOperand, QueryExpressionError, QueryExprEvaluator, F
import json
import datetime
import time
from bson import ObjectId, Binary


def _test(got, should_be=None, approx=None):
    if got == should_be or (approx and abs(got - should_be) <= approx):
        print('   ... OK')
    else:
        # json.dumps(got, ensure_ascii=False, indent=2))
        print('>>> Got:\n', got)
        if should_be:
            print('>>> Should be:\n', should_be)  # json.dumps(
            # should_be, ensure_ascii=False, indent=2))
            exit()


def test_query_parser():

    def _groupby(params):
        if isinstance(params, MongoOperand):
            params = params()
        return Fn.group(orig=Fn.first('$$ROOT'), **params), Fn.replaceRoot(newRoot=Fn.mergeObjects('$orig', {'group_id': '$_id'}, {k: f'${k}' for k in params if k != '_id'}))

    p = QueryExprParser(verbose=True, allow_spacing=True, abbrev_prefixes={None: 'tags=', '#': 'source='}, functions={
        'groupby': _groupby,
        'now': lambda x: datetime.datetime.utcnow(),
    })

    p.set_shortcut('test', 'groupby(id=keywords)')

    def test_expr(expr, should_be=None, approx=None):
        print('>', expr)
        e = p.parse(expr)
        _test(e, should_be, approx)
        print()

    test_expr('#kd,%glass,laugh>=233', {'source': 'kd', 'tags': {
        '$regex': 'glass', '$options': 'i'}, 'laugh': {'$gte': 233}})

    test_expr('%glass,%grass', {'$and': [{'tags': {
        '$regex': 'glass', '$options': 'i'}}, {'tags': {'$regex': 'grass', '$options': 'i'}}]})

    test_expr("(glass|tree),%landscape,(created_at<2020-12-31|images$size=3)",
              {'$and': [{'$or': [{'tags': 'glass'}, {'tags': 'tree'}], 'tags': {'$regex': 'landscape', '$options': 'i'}},
                        {'$or': [{'created_at': {'$lt': 1609344000.0}}, {'images': {'$size': 3}}]}]})

    test_expr(r'escaped="\'ab\ncde\\"', {'escaped': '\'ab\ncde\\'})

    test_expr(r'\u53931234', {'tags': '\u53931234'})

    test_expr('单一,%可惜', {'$and': [{'tags': '单一'}, {
        'tags': {'$regex': '可惜', '$options': 'i'}}]})

    test_expr('1;2;`3;`', [1, 2, "3;"])
    test_expr('a=()', {'a': {}})
    test_expr('a()', {'$a': {}})

    test_expr(r'`as\nis`', {'tags': "as\\nis"})

    test_expr(r'"`escap\ning\`\'"', {'tags': "`escap\ning`'"})

    test_expr('1;2;3;4;', [1, 2, 3, 4])

    test_expr('match(tags=aa)=> \ngroupby(_id=$name,count=sum(1))=>\nsort(count=-1)', [{'$match': {'tags': 'aa'}}, {'$group': {'orig': {'$first': '$$ROOT'}, '_id': '$name', 'count': {
        '$sum': 1}}}, {'$replaceRoot': {'newRoot': {'$mergeObjects': ['$orig', {'group_id': '$_id'}, {'count': '$count'}]}}}, {'$sort': {'count': -1}}])

    test_expr('$ad>$eg', {'$gt': ['$ad', '$eg']})

    test_expr('$eg>size($images)', {'$gt': ['$eg', {'$size': '$images'}]})

    test_expr('size($images)=$eg', {'$eq': [{'$size': '$images'}, '$eg']})
    test_expr('''
            a;
            b;
            '//';
            //unwind($tags); group(_id=$tags,count=sum(1));
            //c; d;'e';
            'g';
            ''', ['a', 'b', '//', 'g'])

    test_expr(";;;;;;;;;", [])

    test_expr('2021-1-1T8:00:00Z+08:00', 1609516800.0)

    test_expr('-3H', int(datetime.datetime.utcnow().timestamp()-3600*3), 1)

    test_expr('ObjectId("1a2b3c4d5e6f708090a0b0c0")',
              ObjectId("1a2b3c4d5e6f708090a0b0c0"))

    test_expr('a;b;(c;d);e', ['a', 'b', ['c', 'd'], 'e'])

    test_expr('a=>b=>(c=>d)=>e', ['a', 'b', 'c', 'd', 'e'])

    print(json.dumps(p.parse("set(collection='abcdef');'';")))

    test_expr('foo([a,b])', {'$foo': ['a', 'b']})

    test_expr('foo(a)', {'$foo': 'a'})

    test_expr('[]', [])

    test_expr('[set(a=1)]', [{'$set': {'a': 1}}])

    test_expr('[[],1]', [[], 1])

    test_expr('[[a],[2]]', [['a'], [2]])

    test_expr('images=[]', {'images': []})

    test_expr('test=1=>:test', [{'test': 1}] +
              list(_groupby(F._id == 'keywords')))

    test_expr('[a,b,c(test=[def]),1]', [
              'a', 'b', {'$c': {'test': ['def']}}, 1])

    test_expr('match(a);other(b)',  [
              {"$match": {"tags": "a"}}, {"$other": "b"}])

    test_expr('match($a>$b)', {'$match': {'$expr': {'$gt': ['$a', '$b']}}})

    test_expr('match(t,$a>$b)', {"$match": {
        "$and": [{"tags": "t"}, {"$gt": ["$a", "$b"]}]}})
    test_expr('size($source)=5', {'$eq': [{'$size': '$source'}, 5]})

    test_expr('empty(hash)', {'$or': [
        {'hash': ''},
        {'hash': Binary(b'')},
        {'hash': None}
    ]})

    test_expr('-3m', datetime.datetime.utcnow().timestamp() - 3*30*86400, 1)

    test_expr('objectId(2022-01-01)',
              ObjectId.from_datetime(datetime.datetime(2022, 1, 1)))


def test_query_evaluator():
    p = QueryExprParser(allow_spacing=True, verbose=False,
                        force_timestamp=False)
    ee = QueryExprEvaluator()

    def test_eval(expr, obj, should_be=None):
        print(expr)
        parsed = p.parse(f'expr({expr})')
        e = ee.evaluate(parsed, obj)
        _test(e, should_be)
        print()

    test_eval('$source', {'source': 1}, 1)

    test_eval('first($source)', {'source': [1]}, 1)

    test_eval('dateDiff(startDate=$st,endDate=$ed,unit=day)',
              {'st': p.parse_literal('2022-1-1'), 'ed': p.parse_literal('2022-5-1')}, 120)

    test_eval('year(toDate("2021-1-1"))', {}, 2021)

    test_eval('avg($source)', {'source': [1, 2, 3, 4, 5]}, 3)

    test_eval('max(concatArrays($source;[12];[34]))', {
        'source': [1, 2, 3, 4, 5]}, 34)

    test_eval('map(input=$source,as=t,in=add($$t;1))',
              {'source': [1, 2, 3]}, [2, 3, 4])

    test_eval('cond($test>10;11;22)', {'test': 1}, 22)

    test_eval('lang=in(chs;cht)', {'lang': 'chs'}, True)

    test_eval('lang%`(chs|cht)`', {'lang': 'chs'}, True)

    test_eval('$lang%`chs`', {'lang': 'chs'}, True)

    test_eval('keywords%a', {
        'keywords': ['ac', 'bc', 'dc']
    }, True)

    print(' '.join(ee.implemented_functions))


def test_dbobject():

    from PyMongoWrapper.dbo import DbObject, DbObjectCollection

    class Elem(DbObject):
        pass

    class Test(DbObject):
        title = str
        keywords = set
        content = str
        pdate = datetime.datetime
        elements = DbObjectCollection(Elem)
        
    t = Test(title='abc', keywords=['def'])
    _test(t.title, 'abc')
    
    t.keywords.append('ghi')
    _test(len(t.keywords), 2)
    
    t.elements = [Elem(), Elem()]
    ele_a, ele_b = t.elements
    ele_a['_id'] = ObjectId()
    ele_b['_id'] = ObjectId()
    
    t.elements.remove(ele_a)
    _test(len(t.elements), 1)
    
    t.elements.remove(ele_b.id)
    _test(len(t.elements), 0)

    t.new_field = 'abc'
    _test(t.new_field, 'abc')

    del t.new_field
    _test('new_field' not in t.as_dict(), True)

    t.new_field = 'abc'
    del t['new_field']
    _test('new_field' not in t.as_dict(), True)

    t.keywords = ['a', 'b', 'c']
    _test(isinstance(t.keywords, set), True)

    _test(Test(t)._orig, t._orig)
    
    t._test = 1
    _test('_test' in t.as_dict(), False)

    try:
        Test('1')
        assert False, 'should raise ValueError'
    except ValueError:
        pass
        
    _test(isinstance(Test().fill_dict(
        {'keywords': ['a', 'b', 'c']}).keywords, set), True)

    _test(Test().fill_dict(
        {'keywords': ['a', 'b', 'c']}).as_dict()['keywords'].__class__.__name__, 'list')

    _test(MongoOperand([Fn.set(keywords='a')])(), [{'$set': {'keywords': 'a'}}])


if __name__ == '__main__':
    for k, func in dict(globals()).items():
        if k.startswith('test_') and hasattr(func, '__call__'):
            print(f"\n\n{k.upper().replace('_', ' ')}\n{'=' * len(k)}\n")
            func()
