"""Parse query expressions"""

import datetime
import json
import base64
from bson import Binary, SON, ObjectId
import re
from antlr4 import *
from dateutil.parser import parse as dtparse

from .mongobase import MongoOperand
from .mongofield import MongoField, Fn
from ._parser.QueryExprLexer import QueryExprLexer
from ._parser.QueryExprParser import QueryExprParser


OBJECTID_PATTERN = re.compile(r'^[0-9A-Fa-f]{24}$')
SPACING_PATTERN = re.compile(r'\s')


class QueryExpressionError(Exception):

    def __init__(self, message='', ctx=None, *args: object) -> None:
        if ctx and isinstance(ctx, ParserRuleContext):
            message += type(ctx).__name__ + \
                ' {}@{}'.format(ctx.getText(), ctx.getSourceInterval())
        super().__init__(message, *args)


class MongoUndetermined(MongoOperand):
    pass


class MongoConcating(MongoOperand):

    def __iter__(self):
        yield from self._literal


class QueryExprVisitor(ParseTreeVisitor):

    operators = {
        '>': '$gt',
        '<': '$lt',
        '>=': '$gte',
        '<=': '$lte',
        '=': '$eq',
        '%': '$regex',
        '!=': '$ne',
        '%%': '$search',
        '+': '$add',
        '-': '$subtract',
        '/': '$divide',
        '*': '$multiply',
        '~': '$not'
    }

    def __init__(self, default_field='_id', default_operator='=', shortcuts=None, functions=None, logger=None) -> None:
        super().__init__()
        self.default_field = MongoField(default_field)
        self.default_operator = default_operator

        assert self.default_operator in self.operators, f'`{default_operator}` not allowed as default operator'

        self.shortcuts = shortcuts or {}
        self.functions = functions or {}
        self.context_stack = []
        self.logger = lambda *_: None if logger is None else logger

    def _findAncestor(self, ctx, stmt_names) -> ParserRuleContext:
        if isinstance(stmt_names, str):
            stmt_names = (stmt_names,)
        stmt_names = {
            f'{name.capitalize()}Context'
            for name in stmt_names
        }
        parent = ctx
        while parent := parent.parentCtx:
            ctx_name = type(parent).__name__
            if ctx_name in stmt_names:
                break
        return parent

    def _expandOperand(self, operand) -> MongoOperand:
        if isinstance(operand, MongoUndetermined) or not isinstance(MongoOperand.literal(operand), (list, dict)):
            return self._expandBinaryOperator(self.default_operator, self.default_field, MongoOperand.operand(operand))
        elif isinstance(MongoOperand.literal(operand), list):
            return self.combineAnds(operand)
        return MongoOperand.operand(operand)

    def _expandBinaryOperator(self, op: str, left: MongoOperand, right: MongoOperand, ctx=None):
        if op == '&':
            return self._expandOperand(left) & self._expandOperand(right)
        elif op == '|':
            return self._expandOperand(left) | self._expandOperand(right)

        if op == '=>':
            left, right = left(), right()
            if not isinstance(left, list):
                left = [left]
            if not isinstance(right, list):
                right = [right]
            return MongoOperand(left + right)

        if op == '.':
            return MongoField(f"{MongoOperand.literal(left)}.{MongoOperand.literal(right)}")

        assert op in self.operators, f'Unknown operator: {op}'

        op = self.operators[op]
        result = {op: right()}
        if op == '$regex':
            result['$options'] = 'i'

        if isinstance(left, (MongoUndetermined, MongoField)) and not left().startswith('$'):
            if op == '$eq':
                result = {
                    left(): right()
                }
            else:
                result = {
                    left(): result
                }
        else:
            left, right = MongoOperand.literal(
                left), MongoOperand.literal(right)
            if op == '$regex':
                result = {
                    '$regexMatch': {
                        'input': left,
                        'regex': right,
                        'options': 'i'
                    }
                }
            elif op in ('$add', '$subtract') and (type(left) is type(right) and isinstance(left, (int, float))) or (isinstance(left, datetime.datetime) and isinstance(left, (datetime.datetime, datetime.timedelta))):
                result = left + right if op == '$add' else left - right
            else:
                result = {
                    op: [left, right]
                }

        return MongoOperand.operand(result)

    def visitStmts(self, ctx: QueryExprParser.StmtsContext):
        try:
            return self.statements(ctx.stmt())
        except AssertionError as ex:
            raise QueryExpressionError from ex

    def visitStmt(self, ctx: QueryExprParser.StmtContext):
        if ctx.getText() == ';':
            return None
        elif stmt_body := ctx.expr():
            return self.visitExpr(stmt_body)
        elif stmt_body := ctx.assignment():
            return self.visitAssignment(stmt_body)
        elif stmt_body := ctx.ifStmt():
            return self.visitIfStmt(stmt_body)
        elif stmt_body := ctx.repeatStmt():
            return self.visitRepeatStmt(stmt_body)
        elif stmt_body := ctx.break_():
            return self.visitBreak(stmt_body)
        elif stmt_body := ctx.continue_():
            return self.visitContinue(stmt_body)
        elif stmt_body := ctx.halt():
            return self.visitHalt(stmt_body)
        elif stmt_body := ctx.sepExpr():
            return self.visitSepExpr(stmt_body)
        else:
            raise QueryExpressionError(f'Unknown context', ctx)

    def visitIfStmt(self, ctx: QueryExprParser.IfStmtContext):
        cond = self.visitExpr(ctx.cond)
        if_true = self.visitStmts(ctx.if_true)
        if_false = []
        if ctx.if_false:
            if_false = self.visitElse(ctx.if_false)

        return MongoOperand({
            '$_FCConditional': {
                'cond': cond,
                'if_true': if_true,
                'if_false': if_false
            }
        })

    def visitElse(self, ctx: QueryExprParser.ElseContext):
        return self.visitStmts(ctx.pipeline)

    def visitRepeatStmt(self, ctx: QueryExprParser.RepeatStmtContext):
        cond = self.visitExpr(ctx.cond)
        pipeline = self.visitStmts(ctx.pipeline)
        return MongoOperand({
            '$_FCRepeat': {
                'cond': cond(),
                'pipeline': pipeline()
            }
        })

    def visitForStmt(self, ctx: QueryExprParser.ForStmtContext):
        target = ctx.assign.target
        iterable = self.visitExpr(ctx.assign.val)
        pipeline = self.visitStmts(ctx.pipeline)
        return MongoOperand({
            '$_FCForEach': {
                'value': target.text,
                'iterable': iterable(),
                'pipeline': pipeline()
            }
        })

    def visitBreak(self, ctx: QueryExprParser.BreakContext):
        ancestor = self._findAncestor(
            ctx, ('RepeatStmt', 'ForStmt'))
        assert ancestor, 'Missing `repeat` or `for` statement for `break`'
        return MongoOperand({
            '$_FCBreak': id(ancestor)
        })

    def visitContinue(self, ctx: QueryExprParser.ContinueContext):
        ancestor = self._findAncestor(
            ctx, ('RepeatStmt', 'ForStmt'))
        assert ancestor, 'Missing `repeat` or `for` statement for `continue`'
        return MongoOperand({
            '$_FCContinue': id(ancestor)
        })

    def visitHalt(self, ctx: QueryExprParser.HaltContext):
        return MongoOperand({
            '$_FCHalt': {}
        })

    def visitAssignment(self, ctx: QueryExprParser.AssignmentContext):
        return MongoOperand({
            '$addFields': {
                ctx.target.text: self.visitExpr(ctx.val)
            }
        })

    # Visit a parse tree produced by QueryExprParser#expr.
    def visitExpr(self, ctx: QueryExprParser.ExprContext):
        result = None

        if op := ctx.op1 or ctx.op2 or ctx.op3 or ctx.op4 or ctx.op5 or ctx.op6:
            op = op.getText()
            left = self.visitExpr(ctx.left)
            right = self.visitExpr(ctx.right)
            result = self._expandBinaryOperator(op, left, right, ctx)

        elif op := ctx.uniop or ctx.notop:
            op = op.getText()
            right = self.visitExpr(ctx.right)
            if ctx.uniop.binOp():
                result = self._expandBinaryOperator(
                    op, self.default_field, right, ctx)
            elif op == '~':
                result = ~self._expandOperand(right)
            else:
                right = right()
                if op == '-':
                    if isinstance(right, (int, float, datetime.timedelta)):
                        result = -right
                    else:
                        result = {
                            '$minus': right
                        }
                elif op == '+':
                    if isinstance(right, (int, float, datetime.timedelta)):
                        result = right
                    elif isinstance(right, str):
                        result = float(right)
                    else:
                        result = {
                            '$toFloat': right
                        }
                elif op == '%%':
                    result = {
                        '$text': {
                            '$search': right
                        }
                    }
                else:
                    result = {
                        self.operators[op]: right
                    }
                result = MongoOperand.operand(result)

        elif ctx.parred:
            result = self.visitExpr(ctx.parred)

        elif ctx.value():
            result = MongoOperand.operand(self.visitValue(ctx.value()))

        elif ctx.func():
            result = self.visitFunc(ctx.func())

        elif ctx.arr():
            result = self.visitArr(ctx.arr())

        elif ctx.obj():
            result = self.visitObj(ctx.obj())

        elif ctx.idExpr():
            text = ctx.idExpr().getText()
            if text == 'id':
                result = MongoField('_id')
            elif text.startswith('$'):
                result = MongoOperand(text)
            else:
                result = MongoUndetermined(text)

        elif ctx.expr():
            result = self.visitExpr(ctx.expr())

        if isinstance(ctx.parentCtx, (QueryExprParser.StmtContext, QueryExprParser.SnippetContext)):
            result = self.combineAnds([result])

        return result

    # Visit a parse tree produced by QueryExprParser#value.
    def visitValue(self, ctx: QueryExprParser.ValueContext):
        text = ctx.getText()

        if text in ('true', 'false'):
            return text == 'true'

        if text == 'null':
            return None

        if ctx.STRING():
            if text.startswith('\''):
                text = '"' + text[1:-1] + '"'
            if text.startswith('"'):
                return json.loads(text.replace('\\\'', "'"))
            if text.startswith('`'):
                return text[1:-1]

        if ctx.DATETIME():
            return dtparse(text[2:-1])

        if ctx.TIME_INTERVAL():
            offset = int(text[:-1])
            offset *= {'y': 365, 'm': 30}.get(text[-1], 1)
            unit = {
                'H': 'hours',
                'h': 'hours',
                'M': 'minutes',
                'i': 'minutes',
                'S': 'seconds',
                's': 'seconds',
                'd': 'days',
                'm': 'days',
                'y': 'days'
            }[text[-1]]
            interval = datetime.timedelta(**{unit: offset})
            return interval

        if ctx.NUMBER():
            if '.' in text or 'e' in text.lower():
                return float(text)
            return int(text)

        if ctx.SHORTCUT():
            assert text[1:] in self.shortcuts, f'Unknown shortcut: {text[1:]}'
            snippet = self.shortcuts[text[1:]]
            if isinstance(snippet(), list):
                return MongoConcating(snippet())
            else:
                return snippet

        if ctx.OBJECT_ID():
            return ObjectId(text[2:-1])

        raise QueryExpressionError('Unknown form of Value', ctx)

    def visitArr(self, ctx: QueryExprParser.ArrContext):
        return self.visitSepExpr(ctx.sepExpr())

    def combineObj(self, dicts):
        result = {}
        if dicts and isinstance(dicts, list) and \
                not [_ for _ in dicts if not isinstance(_, dict) or len(_) != 1 or list(_)[0].startswith('$')]:
            # all are dicts, all dict contains only one key, not starting with '$'
            for val in dicts:
                result.update(val)
        return MongoOperand.operand(result)

    def combineAnds(self, ands):
        a = None
        ands = MongoOperand.literal(ands)

        for e in ands:
            if not e:
                continue
            if isinstance(MongoOperand.literal(e), str) and not isinstance(e, MongoField) and self.default_field:
                e = self._expandBinaryOperator(
                    self.default_operator, self.default_field, MongoOperand(e))
            else:
                e = MongoOperand.operand(e)
            if a is None:
                a = e
            else:
                a = a & e
        return a or MongoOperand({})

    def visitObj(self, ctx: QueryExprParser.ObjContext):
        return MongoOperand.operand(self.combineAnds(self.visitSepExpr(ctx.sepExpr())))

    def visitSepExpr(self, ctx: QueryExprParser.SepExprContext):
        seplist = []
        if ctx and ctx.expr():
            seplist = [
                self.visitExpr(expr) for expr in ctx.expr()
            ]
        if ctx and isinstance(ctx.parentCtx, (QueryExprParser.StmtContext, QueryExprParser.SnippetContext)):
            seplist = self.combineAnds(seplist)
        return MongoOperand.operand(seplist)

    def visitFunc(self, ctx: QueryExprParser.FuncContext):

        func_name = ctx.func_name.text
        if func_name.startswith(':'):
            func_name = func_name[1:]
            args = [self.visitValue(ctx.value())
                    if ctx.value() else ctx.idExpr().getText()]
        else:
            if ctx.sepExpr():
                args = self.visitSepExpr(ctx.sepExpr())()
            else:
                args = {}

        args = self.combineObj(args)() or args
        if len(args) == 1 and isinstance(args, list):
            args = args[0]

        if func_name in self.functions:
            func = self.functions[func_name]
            if isinstance(args, dict):
                for arg_name in ('input', 'in', 'as', 'from', 'to'):
                    if arg_name in args:
                        args[arg_name + '_'] = args.pop(arg_name)
                if 'id' in args:
                    args['_id'] = args.pop('id')
                result = func(**args)
            elif isinstance(args, list):
                result = func(*args)
            else:
                result = func(args)
        else:
            result = {
                '$' + func_name: args
            }
        return MongoOperand.operand(result)

    def statements(self, nodes):
        result = []
        for stmt in nodes:
            stmt = self.visitStmt(stmt)
            if isinstance(stmt, MongoConcating):
                result += stmt()
            elif stmt:
                result.append(MongoOperand.literal(stmt))
        return result

    def visitSnippet(self, ctx: QueryExprParser.SnippetContext):
        stmts = []
        if ctx.stmt():
            stmts = ctx.stmt()
        elif ctx.stmts():
            stmts = ctx.stmts().children
        if stmts:
            return self.statements(stmts)
        elif ctx.expr():
            return self.visitExpr(ctx.expr())
        elif ctx.sepExpr():
            return self.visitSepExpr(ctx.sepExpr())
        elif ctx.getText() == '':
            return None
        else:
            raise QueryExpressionError('Unknown snippet', ctx)


class QueryExprInterpreter:
    """Query expression interpreter
    """

    shortcuts = {}

    def __init__(self,
                 default_field,
                 default_operator,
                 functions=None,
                 verbose=False):
        """
        Args:
            default_field (str): Default field
            default_operator (str): Default operator
            functions (dict, optional): Python functions to handle special function calls
                in expression. Defaults to {}.
            verbose (bool, optional): Show debug info. Defaults to False.
        """

        if verbose:
            self.logger = print
        else:
            self.logger = lambda *a: ''

        self.functions = functions or {}
        self.default_field = default_field
        self.defualt_operator = default_operator

        self._initialize_functions()

    def _initialize_functions(self):

        def _empty(param=''):
            if isinstance(param, str) and not param.startswith('$'):
                param = MongoField(param)
            else:
                param = MongoOperand.operand(param)
            return (param == '') | (param == Binary(b'')) | (param == None)

        def _json(x):
            return json.loads(str(x))

        def _objectId(x):
            if isinstance(x, (int, float)):
                x = datetime.datetime.fromtimestamp(x)
            if isinstance(x, datetime.datetime):
                return ObjectId.from_datetime(x)
            return ObjectId(x)

        def _binData(x):
            if isinstance(x, str):
                x = base64.b64decode(x)
            return Binary(x)

        def _now(param=''):
            result = datetime.datetime.now()
            if isinstance(param, datetime.timedelta):
                result += param
            return result

        def _sort(*sort_strs, **params):
            joined = ''
            if sort_strs:
                joined = ''
                for ss in sort_strs:
                    ss = MongoOperand.literal(ss)
                    if isinstance(ss, dict) and MongoOperand.get_key(ss) == '$minus':
                        ss = '-' + ss['$minus']
                    joined += ss + ','
                joined = joined[:-1]
            params = self.parse_sort(joined or params)
            return Fn.sort(params)

        def _sorted(input_, by=1):
            if isinstance(by, str):
                by = dict(self.parse_sort(by))
            return Fn.sortArray(input=input_, sortBy=by)

        def _join(field):
            params = str(field).lstrip('$')

            return MongoConcating([
                Fn.addFields({
                    params: Fn.reduce(input='$' + params,
                                      initialValue=[],
                                      in_=Fn.concatArrays('$$value', '$$this'))
                })
            ])

        def _strJoin(input_, delimiter=' '):
            output = Fn.reduce(
                input=input_, initialValue='', in_=Fn.concat('$$value', delimiter, '$$this')
            )
            if delimiter:
                output = Fn.replaceOne(
                    input=output,
                    find='^.{' + str(len(delimiter)) + '}',
                    replacement='')
            return output

        def _sample(size):
            return Fn.sample(size=size)

        def _replaceRoot(newroot='', **obj):
            return Fn.replaceRoot(newRoot=newroot or obj)

        def _group(_id, **params):
            return Fn.group(_id=_id, **params)

        def _filter(input_, cond, as_='this'):
            return Fn.filter({'input': input_, 'cond': cond, 'as': as_})

        def _match(*ands, **params):

            def _addExprStructure(d):
                for k in d:
                    if k.startswith('$'):
                        if k in ('$and', '$or', '$text'):
                            d[k] = [_addExprStructure(d) for d in d[k]]
                        else:
                            return {'$expr': d}
                return d

            if ands:
                ands = list(ands) + [params]
                params = QueryExprVisitor(
                    self.default_field, self.defualt_operator).combineAnds(ands)()

            params = _addExprStructure(params)
            return Fn.match(**params)

        def _replaceOne(input_, find, replacement):
            return Fn.replaceOne(input=input_, find=find, replacement=replacement)

        def _replaceAll(input_, find, replacement):
            return Fn.replaceAll(input=input_, find=find, replacement=replacement)

        _bytes = bytes.fromhex

        _let = Fn.addFields

        def _F(string):
            return MongoField(string)

        self.functions.update({
            k[1:]: v
            for k, v in locals().items()
            if k.startswith('_') and hasattr(v, '__call__')
        })

        self.functions['JSON'] = self.functions['json']
        self.functions['ObjectId'] = self.functions['objectId']
        self.functions['BinData'] = self.functions['binData']

    def set_shortcut(self, name: str, expr: str):
        """Set shortcut names

        Args:
            name (str): Shortcut name
            expr (str): Equivalent expression
        """
        if expr:
            try:
                self.logger(f'set shortcut :{name} to {expr}')
                self.shortcuts[name] = self.parse(expr, as_operand=True)
            except Exception as ex:
                self.logger('Error while parsing shortcut:',
                            name, '=', expr, ex)
        else:
            if name in self.shortcuts:
                del self.shortcuts[name]

    def _get_lexer(self, expr):
        return QueryExprLexer(InputStream(expr))
    
    def get_symbol(self, type_):
        return QueryExprParser.symbolicNames[type_]
    
    def get_tokens_string(self, tokens):
        return ' '.join(['{}/{}'.format(token.text, self.get_symbol(token.type)) for token in tokens])

    def tokenize(self, expr):
        lexer = self._get_lexer(expr)
        tokens = lexer.getAllTokens()
        return tokens

    def parse(self, expr, literal=False, visitor=None, as_operand=False):
        if not expr:
            return {}

        parser = QueryExprParser(CommonTokenStream(self._get_lexer(expr)))
        visitor = visitor or \
            QueryExprVisitor(self.default_field, self.defualt_operator,
                             self.shortcuts, self.functions, self.logger)

        result = None
        if literal:
            node = parser.value()
            result = visitor.visitValue(node)
        else:
            node = parser.snippet()
            result = visitor.visitSnippet(node)
        if as_operand:
            return MongoOperand.operand(result)
        else:
            return MongoOperand.literal(result)

    def parse_literal(self, expr: str):
        """Parse literals

        Args:
            expr (str): A string representing a literal value

        Returns:
            Any: The represented literal value
        """
        return self.parse(expr, literal=True)

    def parse_sort(self, sort_info):
        """Parse sorting expression

        Args:
            sort_info (Union[str|dict]): Sorting expression

        Returns:
            List[Tuple[str, int]]: Sorting object
        """
        if isinstance(sort_info, str):
            return SON(MongoField.parse_sort(*sort_info.split(',')))
        elif isinstance(sort_info, dict):

            def _sort_info(d):
                if not isinstance(d, dict):
                    yield (str(d), 1)
                elif '$and' in d:
                    for val in d['$and']:
                        yield from _sort_info(val)
                elif '$minus' in d:
                    yield (d['$minus'], -1)
                else:
                    yield from d.items()

            return SON(_sort_info(sort_info))
