import math
from antlr4 import *
from PyMongoWrapper import QExprInterpreter, Fn, F, \
    MongoOperand, QExprEvaluator, MongoConcating, \
    AntlrQExprParser
import json
import datetime
import click
from decimal import Decimal
from bson import ObjectId, Binary, SON


parser = QExprInterpreter(
    verbose=True, default_field='tags', default_operator='=')


class TraverseVisitor(ParseTreeVisitor):

    def __init__(self) -> None:
        super().__init__()
        self.indent = ''

    def visitSnippet(self, tree):
        self.visit(tree)

    def visit(self, tree):
        if isinstance(tree, TerminalNode):
            print('{}{}/{}'.format(self.indent, tree.getText(),
                  AntlrQExprParser.symbolicNames[tree.symbol.type]))
        else:
            print('{}{}'.format(self.indent,
                  AntlrQExprParser.ruleNames[tree.getRuleIndex()]))
            self.indent += '  '
            for child in tree.children:
                self.visit(child)
            self.indent = self.indent[:-2]


def _print(expr):

    print(parser.get_tokens_string(parser.tokenize(expr)))
    parser.parse(expr, visitor=TraverseVisitor())


def _test(got, should_be=None, approx=None):
    if should_be is not None and (got == should_be or (approx and abs(got - should_be) <= approx)):
        print('   ... OK')
        return True
    else:
        print('>>> Got:\n', got)
        if should_be is not None:
            print('>>> Should be:\n', should_be)
        return False


def test_query_parser():

    def _groupby(_id, **params):
        lst = Fn.group(orig=Fn.first('$$ROOT'), _id=_id, **params), Fn.replaceRoot(newRoot=Fn.mergeObjects(
            '$orig', {'group_id': '$_id'}, {k: f'${k}' for k in params}))
        return MongoConcating(lst)

    parser.functions.update({
        'groupby': _groupby,
    })

    parser.set_shortcut('test', 'groupby($keywords)')

    parser.set_shortcut('g', '%`^#`')

    def test_lexer(expr, should_be=''):
        print('L>', expr)
        tokens = parser.get_tokens_string(parser.tokenize(expr))
        if not _test(tokens, should_be.strip()):
            exit()
        print()

    test_lexer('%glass', '%/Mod glass/ID')

    test_lexer('#abcd', '#abcd/ID')

    test_lexer(
        '1+3*4-5/6', '1/NUMBER +/Plus 3/NUMBER */Star 4/NUMBER -/Minus 5/NUMBER //Div 6/NUMBER')

    test_lexer('d"2023-1-1"', 'd"2023-1-1"/DATETIME')
    
    def test_expr(expr, should_be=None, approx=None, context=None):
        print('P>', expr)
        e = parser.parse(expr, context=context)
        if not _test(e, should_be, approx):
            _print(expr)
            if not click.confirm('Continue?', True):
                exit()
        print()

    test_expr('~:g,test',  {'$and': [{'tags': {
              '$not': {'$regex': '^#', '$options': 'i'}}}, {'tags': 'test'}]})
    
    test_expr('~"test"', {'tags': {'$ne': 'test'}})
        
    test_expr('1+134', 135)

    test_expr('$id>o"0123456789ab0123456789ab"', {
        '$gt': ['$_id', ObjectId('0123456789ab0123456789ab')]
    })
    
    test_expr('#test;sort(id);',  [{'tags': '#test'}, {'$sort': SON([('_id', 1)])}])
        
    test_expr('now()-10d', datetime.datetime.utcnow() - datetime.timedelta(days=10), datetime.timedelta(seconds=1))

    test_expr('call(something,())', {'$call': ['something', {}]})

    test_expr('pipelines.0.user="",pipelines.1.allow=false',  {
              'pipelines.0.user': '', 'pipelines.1.allow': False})

    test_expr('%glass,laugh>=233', {'tags': {
        '$regex': 'glass', '$options': 'i'}, 'laugh': {'$gte': 233}})

    test_expr('%glass,%grass', {'$and': [{'tags': {
        '$regex': 'glass', '$options': 'i'}}, {'tags': {'$regex': 'grass', '$options': 'i'}}]})

    test_expr('a,b|(c,d,e,f);',  [{'$and': [{'tags': 'a'}, {'$or': [{'tags': 'b'}, {
              '$and': [{'tags': 'c'}, {'tags': 'd'}, {'tags': 'e'}, {'tags': 'f'}]}]}]}])

    test_expr("(glass|tree),%landscape,(created_at<d'2020-12-31'|images=size(3))",
              {'$and': [{'$or': [{'tags': 'glass'}, {'tags': 'tree'}]},
                        {'tags': {'$regex': 'landscape', '$options': 'i'}},
                        {'$or': [{'created_at': {'$lt': datetime.datetime(2020, 12, 31)}}, {'images': {'$size': 3}}]}]})

    test_expr(r'escaped="\'ab\ncde\\"', {'escaped': '\'ab\ncde\\'})

    test_expr(r'"\u53931234"', {'tags': '\u53931234'})

    test_expr(r'concat(a,b,c,concat(d,e,$x),toString(1),$a)', {'$concat': ['abcde', '$x', {'$toString': 1}, '$a']})
    
    test_expr('context(test)', 100, context={'test': 100})

    test_expr('单一,%可惜', {'$and': [{'tags': '单一'}, {
        'tags': {'$regex': '可惜', '$options': 'i'}}]})

    test_expr('[1,-2e+10,`3;`]', [1, -2e10, "3;"])
    test_expr('a=()', {'a': {}})
    test_expr('a()', {'$a': {}})

    test_expr(r'`as\nis`', {'tags': "as\\nis"})

    test_expr('$total/($count+1)=$a+1',
              {'$eq': [{'$divide': ['$total', {'$add': ['$count', 1]}]}, {'$add': ['$a', 1]}]})

    test_expr('1=>2=>3=>4', [1, 2, 3, 4])

    test_expr('$ad>$eg', {'$gt': ['$ad', '$eg']})

    test_expr('$eg>size($images)', {'$gt': ['$eg', {'$size': '$images'}]})

    test_expr('size($images)=$eg', {'$eq': [{'$size': '$images'}, '$eg']})
    test_expr('''
            a =>
            b =>
            '//' =>
            //unwind($tags); group(_id=$tags,count=sum(1)) =>
            //c; d;'e' =>
            'g'
            ''', ['a', 'b', '//', 'g'])

    test_expr(";;;;;;;;;", [])

    test_expr('d"2021-1-1T8:00:00"', datetime.datetime(2021, 1, 1, 8))

    test_expr('-3h', datetime.timedelta(hours=-3))

    test_expr('ObjectId("1a2b3c4d5e6f708090a0b0c0")',
              ObjectId("1a2b3c4d5e6f708090a0b0c0"))

    test_expr('a=>b=>(c=>d)=>e', ['a', 'b', 'c', 'd', 'e'])

    print(parser.get_tokens_string(
        parser.tokenize("set(collection='abcdef');'';")))
    print(json.dumps(parser.parse("set(collection='abcdef');'';")))

    test_expr('foo([a,b])', {'$foo': ['a', 'b']})

    test_expr('foo(a)', {'$foo': 'a'})

    test_expr('[]', [])

    test_expr('[set(a=1)]', [{'$set': {'a': 1}}])

    test_expr('[[],1]', [[], 1])

    test_expr('[[a],[2]]', [['a'], [2]])

    test_expr('images=[]', {'images': []})

    test_expr('test=1=>:test', [{'test': 1}] +
              list(_groupby('$keywords')))

    test_expr(':test //', list(_groupby('$keywords')))

    test_expr('`^.*\s$`im', {'$regex': '^.*\s$', '$options': 'im'})

    test_expr('(a=1,b=2)', {'a': 1, 'b': 2})

    test_expr('test=1;groupby($keywords);',  [{'test': 1}] +
              list(_groupby('$keywords')))

    test_expr('[a,b,c(test=[def]),1]', [
              'a', 'b', {'$c': {'test': ['def']}}, 1])

    test_expr('match($a>$b)', {'$match': {'$expr': {'$gt': ['$a', '$b']}}})

    test_expr('match(t,$a>$b)', {'$match': {
              '$and': [{'tags': 't'}, {'$expr': {'$gt': ['$a', '$b']}}]}})
    test_expr('size($source)=5', {'$eq': [{'$size': '$source'}, 5]})

    test_expr('empty(hash)', {'$or': [
        {'hash': ''},
        {'hash': Binary(b'')},
        {'hash': None}
    ]})
    
    test_expr(':pass { if ($arg > 10) { return $arg - 10; } else { return $arg; } }', [])
    test_expr('pass(1); :pass 12;', [1, 2])

    test_expr('sort(-pdate)', {'$sort': SON([['pdate', -1]])})

    test_expr('objectId(d"2022-01-01")',
              ObjectId.from_datetime(datetime.datetime(2022, 1, 1)))

    test_expr('''
              if (hash = 1) {
                  do(this);
              } else {
                  do(that);
              }
              ''',  [{'$_FCConditional': {'cond': {'hash': 1}, 'if_true': [{'$do': 'this'}], 'if_false': [{'$do': 'that'}]}}]
              )

    test_expr('match(tags=aa)=> \ngroupby(_id=$name,count=sum(1))=>\nsort(-count)', [{'$match': {'tags': 'aa'}}, {'$group': {'orig': {'$first': '$$ROOT'}, '_id': '$name', 'count': {
        '$sum': 1}}}, {'$replaceRoot': {'newRoot': {'$mergeObjects': ['$orig', {'group_id': '$_id'}, {'count': '$count'}]}}}, {'$sort': {'count': -1}}])

    test_expr('''
              @example,:g;
              gid: 1;
              ''',  [{'$and': [{'tags': '@example'}, {'tags': {'$regex': '^#', '$options': 'i'}}]}, {'$addFields': {'gid': 1}}])

    parser.set_shortcut('r', 'F(rating)')
    print(parser.shortcuts['r'])
    test_expr(':r>1', {'rating': {'$gt': 1}})
    
    test_expr(':rr test', {'$rr': 'test'})

    test_expr('a:=filter(input=$images,cond=($$this.item_type=image));',   [{'$addFields': {'a': {
              '$filter': {'input': '$images', 'cond': {'$eq': ['$$this.item_type', 'image']}, 'as': 'this'}}}}])

    test_expr('id=o"1234567890ab1234567890ab"', {
              '_id': ObjectId('1234567890ab1234567890ab')})

    test_expr("kws:=filter($keywords,~($$this%'^[a-z]+$'));",  [{'$addFields': {'kws': {'$filter': {
              'input': '$keywords', 'cond': {'$not': {'$regexMatch': {'input': '$$this', 'regex': '^[a-z]+$', 'options': 'i'}}}, 'as': 'this'}}}}])


def test_query_evaluator():
    p = QExprInterpreter('tags', '%', verbose=False)
    ee = QExprEvaluator(p.shortcuts)
    
    def test_eval(expr, obj, should_be=None):
        print(expr)
        print(p.get_tokens_string(p.tokenize(f'expr({expr})')))
        p.parse(expr, visitor=TraverseVisitor())
        parsed = p.parse(f'expr({expr})')
        e = ee.evaluate(parsed, obj)
        if not _test(e, should_be):
            _print(expr)
            if not click.confirm('Continue?', True):
                exit()
        print()
        
    def test_exec(expr, obj, should_be=None, obj_should_be=None):
        p.parse(expr, visitor=TraverseVisitor())
        parsed = p.parse(expr)
        e = ee.execute(parsed, obj)
        if not _test(e, should_be) or not _test(obj, obj_should_be):
            if not click.confirm('Continue?', True):
                exit()
        
    test_exec('''
              :fib {
                if ($arg <= 2) return 1; 
                return fib@($arg - 1) + fib@($arg - 2);
              }
              return fib@($arg);
              ''', {'arg': 6}, 8, {'arg': 6})
    
    test_exec('''
    obj.subobj.num := 1;
    return $obj.subobj.num;
    ''', {'obj': {}}, 1, {'obj': {'subobj': {'num': 1}}})

    test_eval('$source', {'source': 1}, 1)

    test_eval('first($source)', {'source': [1]}, 1)

    test_eval('dateDiff(startDate=$st,endDate=$ed,unit=day)',
              {'st': p.parse_literal("d'2022-1-1'"), 'ed': p.parse_literal("d'2022-5-1'")}, 120)

    test_eval('year(toDate("2021-1-1"))', {}, 2021)

    test_eval('toDate("abcdefg")=null', {}, True)

    test_eval('avg($source)', {'source': [1, 2, 3, 4, 5]}, 3)

    test_eval('val%`abc`', {'val': 'abc'}, True)
    
    test_eval('val%`abc`c', {'val': 'ABC'}, False)

    test_eval('val=`abc`im', {'val': 'ABC'}, True)

    test_eval('max(concatArrays([$source,[12],[34]]))', {
        'source': [1, 2, 3, 4, 5]}, 34)

    test_eval('map(input=$source,as=t,in=$$t+1)',
              {'source': [1, 2, 3]}, [2, 3, 4])

    test_eval('cond([$test>10,11,22])', {'test': 1}, 22)

    test_eval('lang=in([chs,cht])', {'lang': 'chs'}, True)

    test_eval('lang%`(chs|cht)`', {'lang': 'chs'}, True)

    test_eval('$lang%`chs`', {'lang': 'chs'}, True)
    
    test_eval('addFields(a=1)', {}, {'a': 1})

    test_eval('keywords%a', {
        'keywords': ['ac', 'bc', 'dc']
    }, True)

    test_eval('trunc(11.1, -1)', {}, 10)

    test_eval('topN(n=2, output=$a, sortBy=(a=1, b=-1), input=$test)', {'test':
                                                                        [
                                                                            {'a': 2,
                                                                                'b': 2},
                                                                            {'a': 1,
                                                                                'b': 3},
                                                                            {'a': 1,
                                                                                'b': 4},
                                                                            {'a': 0,
                                                                                'b': 4},
                                                                        ]
                                                                        },  [2, 1])

    test_eval('maxN(n=2, input=$scores)', {'scores': [1, 2, 3, 4]}, [4, 3])

    test_eval('lastN(n=2, input=$scores)', {'scores': [1, 2, 3, 4]}, [3, 4])

    test_eval('split("a b c  d", " ")', {}, "a b c  d".split(' '))

    test_eval('gt($a, $b)', {'a': 1, 'b': 2}, False)

    test_eval('sin($a)', {'a': 1}, math.sin(1))

    test_eval('objectToArray($$ROOT)', {'a': 1}, [{'k': 'a', 'v': 1}])

    test_eval('toDecimal("1.3")', {}, Decimal('1.3'))

    print(' '.join(ee.implemented_functions))


def test_querify():

    def test_querify(q):
        parsed = parser.parse(q)
        reconstructed = parser.querify(parsed)
        print('Q>', q)
        parsed2 = parser.parse(reconstructed)
        if not _test(parsed, parsed2):
            print(reconstructed)
            if not click.confirm('Continue?', True):
                exit()

    test_querify('a')
    test_querify('a>10,$b<=20')
    test_querify('match(something);groupby(author);')


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
        nodups = DbObjectCollection(Elem, allow_duplicates=False)

    t = Test(title='abc', keywords=['def'])
    _test(t.title, 'abc')

    t.keywords.add('ghi')
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

    _test(MongoOperand([Fn.set(keywords='a')])
          (), [{'$set': {'keywords': 'a'}}])

    oid = ObjectId('0'*24)
    _test(len(Test(nodups=[Elem(id=oid), Elem(id=oid)]).nodups), 1)


if __name__ == '__main__':
    for k, func in dict(globals()).items():
        if k.startswith('test_') and hasattr(func, '__call__'):
            print(f"\n\n{k.upper().replace('_', ' ')}\n{'=' * len(k)}\n")
            func()
