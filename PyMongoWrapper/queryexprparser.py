"""Parse query expressions"""

import datetime
import json
import base64
from bson import Binary, SON

from bson import ObjectId

from .mongobase import MongoOperand
from .mongofield import MongoField, Fn

from ._queryexprtokenizer import *


class MongoParserConcatingList(MongoOperand):
    """Append the current literal list"""

    def __iter__(self):
        yield from self._literal


class QueryExprParser:
    """Query expression parser
    """

    def __init__(self,
                 abbrev_prefixes=None,
                 functions=None,
                 force_timestamp=True,
                 allow_spacing=False,
                 arithmetic=False,
                 verbose=False):
        """
        Args:
            abbrev_prefixes (dict, optional): Abbreviative prefixes. Defaults to {}.
            functions (dict, optional): Python functions to handle special function calls
                in expression. Defaults to {}.
            force_timestamp (bool, optional): Force the use of timestamp instead of
                datetime.datetime objects. Defaults to True.
            allow_spacing (bool, optional): Allow (ignore) spacing in expressions.
                Defaults to False.
            operators (dict, optional): Mapping operators to MongoDB functions (operators).
            priorities (dict, optional): Specify priority info for operators.
            arithmetic (bool, optional): Use +,-,*,/ for arithmetic operators without calc() context.
            verbose (bool, optional): Show debug info. Defaults to False.
        """

        self.force_timestamp = force_timestamp
        if verbose:
            self.logger = print
        else:
            self.logger = lambda *a: ''

        self.allow_spacing = allow_spacing
        self.functions = functions or {}
        self.arithmetic = arithmetic
        self.abbrevs = []
        self.shortcuts = {}

        self.default_field, self.default_op = '$text', '%%'
        self._literal_tokenizer = self._get_tokenizer()
        
        self.operators = dict(self._literal_tokenizer.operators)
        self.operators.update(
            self._literal_tokenizer.arithmetic_operators
        )
        
        if abbrev_prefixes is not None:
            if None in abbrev_prefixes:
                self.default_field, self.default_op, _ = self._split_field_ops(
                    abbrev_prefixes[None])
                del abbrev_prefixes[None]

            for k in abbrev_prefixes:
                abbrev_prefixes[k] = self.tokenize_expr(abbrev_prefixes[k])

            self.abbrevs = sorted(abbrev_prefixes.items(),
                                  key=lambda x: len(x[0]), reverse=True)

        self._initialize_functions()

    def _initialize_functions(self):

        def _empty(param=''):
            if isinstance(param, str) and not param.startswith('$'):
                param = MongoField(param)
            else:
                param = MongoOperand(param)
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

        def _sort(sort_str='', **params):
            if sort_str:
                params = SON(self.parse_sort(sort_str))
            return {'$sort': params}

        def _sorted(input_, by=1):
            if isinstance(by, str):
                by = dict(self.parse_sort(by))
            return {'$sortArray': {'input': input_, 'sortBy': by}}

        def _join(field):
            params = str(field).lstrip('$')

            return MongoParserConcatingList([
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

        def _replaceRoot(newRoot):
            return Fn.replaceRoot(newRoot=newRoot)

        def _group(_id, **params):
            return Fn.group(_id=_id, **params)

        _bytes = bytes.fromhex

        _let = Fn.addFields

        def _calc(*anyliteral, **anything): return anyliteral or anything

        self.functions.update({
            k[1:]: v
            for k, v in locals().items()
            if k.startswith('_') and hasattr(v, '__call__')
        })

        self.functions['JSON'] = self.functions['json']
        self.functions['ObjectId'] = self.functions['objectId']
        self.functions['BinData'] = self.functions['binData']

    def _get_tokenizer(self):
        return QueryExprTokenizer(self.arithmetic, self.allow_spacing, self.force_timestamp, None,
                                  self.abbrevs, self.default_field, self.default_op,
                                  self.shortcuts, logger=self.logger)

    def _split_field_ops(self, token):
        """Split field name and operator

        Args:
            token (str): String with field name and operator

        Returns:
            Tuple[str, str]: A type of (<field name>, <operator>)
        """
        priorities = dict(self._literal_tokenizer.priorities)
        if self.arithmetic:
            priorities.update(self._literal_tokenizer.arithmetic_priorities)
        for operator in sorted(priorities, key=len, reverse=True):
            operator = str(operator)
            if operator in token:
                qfield, opa = token.split(operator, 1)
                if not qfield:
                    qfield = self.default_field
                return qfield, operator, opa
        return self.default_field, self.default_op, token

    def tokenize_expr(self, expr: str):
        """Tokenizes the expression

        Args:
            expr (str): Expression string

        Returns:
            list: List of self._tokens
        """
        tokenizer = self._get_tokenizer()
        return tokenizer.tokenize(expr)

    def force_operand(self, arg):
        """Force input value to convert to MongoOperand

        Args:
            v (Any): Any valid value

        Returns:
            MongoOperand: Result
        """
        if isinstance(arg, (EStr, str)):
            return MongoOperand(self.expand_query(self.default_field, self.default_op, str(arg)))
        if isinstance(arg, EList):
            return MongoOperand(arg.literal)
        if isinstance(arg, MongoOperand):
            return arg
        return MongoOperand(arg)

    def set_shortcut(self, name: str, expr: str):
        """Set shortcut names

        Args:
            name (str): Shortcut name
            expr (str): Equivalent expression
        """
        if expr:
            self.shortcuts[name] = self.tokenize_expr(expr)
        else:
            if name in self.shortcuts:
                del self.shortcuts[name]

    def parse_literal(self, expr: str):
        """Parse literals

        Args:
            expr (str): A string representing a literal value

        Returns:
            Any: The represented literal value
        """
        return self._literal_tokenizer.literal(expr)

    def expand_query(self, token, operator: str, opa: MongoOperand):
        """Parse token, operator, and operand

        Args:
            token (Any): Token
            operator (str): Operator
            opa (MongoOperand): MongoOperand

        Returns:
            Any: Result after opration
        """
        self.logger('expand', token, operator, opa)

        if isinstance(token, MongoOperand):
            token = token()
        if isinstance(opa, MongoOperand):
            opa = opa()

        var_token = MongoOperand.get_key(token).startswith('$')
        var_opa = MongoOperand.get_key(opa).startswith('$')
        if (operator in self.operators and (var_token or var_opa)) or (
                operator == '=' and var_token) or (operator in self._literal_tokenizer.arithmetic_operators):
            operator = self.operators.get(operator, '$eq')
            if operator == '$regex':
                return {
                    '$regexMatch': {
                        'input': token,
                        'regex': opa,
                        'options': 'i'
                    }
                }
            return {
                operator: [token, opa]
            }

        if operator in self.operators:
            opa = {self.operators[operator]: opa}
            if self.operators[operator] == '$regex':
                opa['$options'] = 'i'
                opa['$regex'] = str(opa['$regex'])

        elif operator == '__fn__':
            token = f'${token}'
            operator = '='

        if isinstance(token, (EStr, str)):
            if token == 'id' or token.endswith('.id'):
                token = token[:-2] + '_id'
            if (token == '_id' or token.endswith('._id')) and isinstance(opa, (EStr, str))\
                    and OBJECTID_PATTERN.match(opa):
                opa = ObjectId(str(opa))
            if token == '$match':
                if not isinstance(opa, (dict, list)):
                    opa = self.expand_query(
                        self.default_field, self.default_op, opa)
                if MongoOperand.get_key(opa) in self.operators.values() \
                        or MongoOperand.get_key(opa) == '$eq':
                    opa = {'$expr': opa}

            fields = str(token).split('$')

            if len(fields) > 1:
                val = {fields[0]: {}}
                res = val[fields[0]]
                for field in fields[1:-1]:
                    res['$' + field] = {}
                    res = res['$' + field]
                res['$' + fields[-1]] = opa
            else:
                val = {fields[0]: opa}

            if '' in val:
                val = val['']

            return val

        elif isinstance(token, EList):
            token = token.literal
            return token

        return token

    def get_priority(self, token):
        return self._literal_tokenizer.priorities.get(token,
                                                      self._literal_tokenizer.arithmetic_priorities.get(
                                                          token,
                                                      0))

    def parse_tokens(self, tokens):
        """Parse query expression tokens

        Args:
            tokens (list): List of tokens

        Raises:
            QueryExpressionError: Evaluation error

        Returns:
            Any: The result, preferably a dict for pymongo to handle
        """
        post = []
        stack = []
        for token in tokens:
            if not isinstance(token, EOperator):
                post.append(token)
            else:
                if token not in (')', ']') and \
                    (not stack or token in ('(', '[') or stack[-1] in ('(', '[')
                        or self.get_priority(token) > self.get_priority(stack[-1])):
                    stack.append(token)
                elif token == ')':
                    while stack and stack[-1] != '(':
                        post.append(stack.pop())
                    if stack:
                        stack.pop()
                    else:
                        raise QueryExpressionError(token)
                elif token == ']':
                    while stack and stack[-1] != '[':
                        post.append(stack.pop())
                    if stack:
                        stack.pop()
                    else:
                        raise QueryExpressionError(token)
                else:
                    while True:
                        if stack and stack[-1] not in ('(', '[') and \
                                self.get_priority(token) <= self.get_priority(stack[-1]):
                            post.append(stack.pop())
                        else:
                            stack.append(token)
                            break

        while stack:
            post.append(stack.pop())

        self.logger(' '.join([repr(_) for _ in post]))

        opers = []
        for token in post:
            self.logger(repr(token), 'opers(%i):' % len(opers), opers)
            try:
                if not isinstance(token, EOperator):
                    opers.append(token)
                    continue
                if token == '&' or token == ',':
                    op_a, op_b = self.force_operand(
                        opers.pop()), self.force_operand(opers.pop())
                    opers.append(op_b & op_a)
                elif token == '|':
                    op_a, op_b = self.force_operand(
                        opers.pop()), self.force_operand(opers.pop())
                    opers.append(op_b | op_a)
                elif token in ('=>', ';'):
                    op_a = []
                    concating = False

                    if opers:
                        op_a = opers.pop()
                        if isinstance(op_a, MongoParserConcatingList):
                            concating = True
                        if isinstance(op_a, MongoOperand):
                            op_a = op_a()
                        if isinstance(op_a, EStr):
                            op_a = str(op_a)

                    if opers:
                        op_b = opers.pop()
                        if isinstance(op_b, MongoParserConcatingList):
                            concating = True
                        if isinstance(op_b, MongoOperand):
                            op_b = op_b()
                        if isinstance(op_b, EStr):
                            op_b = str(op_b)

                        if isinstance(op_b, (list, EList)):
                            val = list(op_b)
                        else:
                            val = [op_b]

                        if (isinstance(op_a, (list, EList)) and token == '=>') \
                                or concating:
                            val += op_a
                        else:
                            val.append(op_a)
                    else:
                        val = op_a
                    opers.append(MongoOperand(val))
                elif token == '__sep__':
                    op_b = EList([], token.bundle)
                    if len(opers) >= 2:
                        op_a, op_b = opers.pop(), opers.pop()
                        if isinstance(op_b, EList) and op_b.bundle is token.bundle:
                            op_b.append(MongoOperand(op_a)())
                        else:
                            op_b = EList([op_b, op_a], token.bundle)
                    opers.append(op_b)
                elif token == '__list__':
                    if opers:
                        op_b = opers.pop()
                        if isinstance(op_b, EList):
                            op_b = op_b.literal
                            opers.append(op_b)
                        elif isinstance(op_b, list):
                            opers.append(op_b)
                        elif isinstance(op_b, EOperator):
                            opers.append(op_b)
                            opers.append([])
                        elif isinstance(op_b, EStr):
                            opers.append([str(op_b)])
                        else:
                            opers.append([MongoOperand(op_b)()])
                    else:
                        opers.append([])
                elif token == '~':
                    opers.append(~self.force_operand(opers.pop()))
                elif token == '.':
                    op_a, op_b = opers.pop(), opers.pop()
                    opers.append(self.parse_literal(f'{op_b}.{op_a}'))
                elif self.get_priority(token):
                    opa = opers.pop()
                    if isinstance(opa, EStr):
                        opa = str(opa)
                    elif isinstance(opa, EList):
                        opa = opa.literal

                    qfield = self.default_field if isinstance(
                        token, EDefaultOperator) else opers.pop()
                    if isinstance(qfield, EStr):
                        opa = str(qfield)
                    if token == '__fn__':
                        if isinstance(qfield, MongoOperand):
                            val, *_ = qfield().values()
                            val.update(**opa())
                            opers.append(qfield)
                        elif qfield in self.functions:
                            func = self.functions[qfield]
                            if isinstance(opa, MongoOperand):
                                opa = opa()
                            if isinstance(opa, dict):
                                for arg_name in ('input', 'in', 'as', 'from', 'to'):
                                    if arg_name in opa:
                                        opa[arg_name + '_'] = opa.pop(arg_name)
                                func_result = func(**opa)
                            elif isinstance(opa, list):
                                func_result = func(*opa)
                            else:
                                func_result = func(opa)
                            if not isinstance(func_result, MongoOperand):
                                func_result = MongoOperand(func_result)
                            opers.append(func_result)
                        else:
                            opers.append(
                                MongoOperand(self.expand_query(qfield, token, opa)))
                    else:
                        opers.append(
                            MongoOperand(self.expand_query(qfield, token, opa)))
                else:
                    opers.append(token)
            except Exception as ex:
                raise QueryExpressionError(token) from ex

        return opers[0] if opers else None

    def parse(self, expr):
        """Parse the expression

        Args:
            expr (str): Expression

        Returns:
            Any: Parsed result
        """
        val = self.parse_tokens(self.tokenize_expr(expr))
        if val is None or isinstance(val, (list, dict)):
            return val
        return self.force_operand(val)()

    def parse_sort(self, sort_str):
        """Parse sorting expression

        Args:
            sort_str (str): Sorting expression

        Returns:
            List[Tuple[str, int]]: Sorting object
        """
        return MongoField.parse_sort(*sort_str.split(','))
