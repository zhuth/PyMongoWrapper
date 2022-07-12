"""Parse query expressions"""

import datetime
import json
import re
from typing import Any, List, Tuple, Union, Iterable
import base64
from bson import Binary

import dateutil.parser
from bson import ObjectId

from .mongobase import MongoOperand
from .mongofield import MongoField

OBJECTID_PATTERN = re.compile(r'^[0-9A-Fa-f]{24}$')
SPACING_PATTERN = re.compile(r'\s')


class _str:
    """String with line, col, and extra (bundle) info"""

    def __init__(self, literal, line=0, col=0, bundle=None) -> None:
        self.literal = str(literal)
        if line == 0 and col == 0 and isinstance(literal, _str):
            line, col = literal.line, literal.col
        self.line, self.col = line, col
        self.bundle = bundle

    def __repr__(self) -> str:
        return f'{self.literal}/{type(self).__name__}(@{self.line}:{self.col})'

    def __str__(self) -> str:
        return self.literal

    def __add__(self, another):
        if not isinstance(another, _str):
            another = _str(another, 1 << 31, 1 << 31)
        return _str(self.literal + another.literal,
                    min(self.line, another.line), min(self.col, another.col))

    def __getitem__(self, key):
        return _str(self.literal[key], self.line, self.col)

    def __eq__(self, obj: object) -> bool:
        return str(obj) == self.literal

    def __hash__(self) -> int:
        return hash(self.literal)

    def __len__(self):
        return len(self.literal)

    def startswith(self, prefixes: Union[Tuple, str]):
        """Check if _str startwith prefix(es)
        """
        return self.literal.startswith(prefixes)


class _Literal(_str):
    """Representing a literal string"""

    def __repr__(self) -> str:
        return f'{repr(self.literal)}/{type(self).__name__}(@{self.line}:{self.col})'


class _Operator(_str):
    """Representing an operator"""


class _DefaultOperator(_Operator):
    """Representing an operator with default field name"""


class _list:
    """Representing a list object"""

    def __init__(self, init: List = None, bundle: object = None):
        if init and not isinstance(init, list):
            init = list(init)
        self.literal = [] if init is None else init
        self.bundle = bundle

    def append(self, element):
        """Appending element to the list"""
        self.literal.append(element)

    def __iter__(self):
        return self.literal

    def __add__(self, another: Iterable):
        self.literal += list(another)

    def __repr__(self):
        return f'{repr(self.literal)}/bundle={id(self.bundle)&0xffff:04x}'

    def __str__(self):
        return str(self.literal)


class QueryExpressionError(Exception):
    """Query Expression Error
    """

    def __init__(self, token) -> None:
        """Initialize with token (_str)

        Args:
            token (_str): token
        """
        super().__init__()
        if not isinstance(token, _str):
            token = _str(token, 0, 0)
        self.token = token

    def __str__(self) -> str:
        """Print out position info off the token

        Returns:
            str: _description_
        """
        return f'{type(self).__name__}: {repr(self.token)}'


class QueryExprParser:
    """Query expression parser
    """

    def __init__(self,
                 abbrev_prefixes=None,
                 functions=None,
                 force_timestamp=True,
                 allow_spacing=False,
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
            verbose (bool, optional): Show debug info. Defaults to False.
        """

        self.force_timestamp = force_timestamp
        if verbose:
            self.logger = print
        else:
            self.logger = lambda *a: ''

        self.allow_spacing = allow_spacing

        self.shortcuts = {}
        self.operators = {
            '>': '$gt',
            '<': '$lt',
            '>=': '$gte',
            '<=': '$lte',
            '%': '$regex',
            '!=': '$ne',
            '%%': '$search'
        }

        priorities = {
            '.': 99,
            '__fn__': 50,
            '=': 30,
            '~': 5,
            ',': 4,
            '&': 4,
            '|': 3,
            '=>': 2,
            ';': 2,
            '__sep__': 2,
            '__list__': 2,
        }

        for operator in self.operators:
            priorities[operator] = 20
        priorities = {_str(k, 0, 0): v for k, v in priorities.items()}
        self.priorities = priorities
        self.max_operator_len = max(
            map(lambda x: len(x) if not x.startswith('__') else 0, self.priorities))

        self.default_field = '$text'
        self.default_op = '%%'

        self.abbrev_prefixes = {}
        if abbrev_prefixes is not None:
            if None in abbrev_prefixes:
                self.default_field, self.default_op, _ = self.split_field_ops(
                    abbrev_prefixes[None])
                del abbrev_prefixes[None]

            for k in abbrev_prefixes:
                abbrev_prefixes[k] = self.tokenize_expr(abbrev_prefixes[k])

            self.abbrev_prefixes = abbrev_prefixes

        self.functions = functions or {}

        def _empty(param=''):
            if isinstance(param, str) and not param.startswith('$'):
                param = MongoField(param)
            else:
                param = MongoOperand(param)
            return (param == '') | (param == Binary(b'')) | (param == None)

        def _json(x):
            return json.loads(str(x))

        def _object_id(x):
            if isinstance(x, (int, float)):
                x = datetime.datetime.fromtimestamp(x)
            if isinstance(x, datetime.datetime):
                return ObjectId.from_datetime(x)
            return ObjectId(x)

        def _bin_data(x):
            if isinstance(x, str):
                x = base64.b64decode(x)
            return Binary(x)

        self.functions['JSON'] = self.functions['json'] = _json
        self.functions['ObjectId'] = self.functions['objectId'] = _object_id
        self.functions['BinData'] = self.functions['binData'] = _bin_data
        self.functions['empty'] = _empty

    def tokenize_expr(self, expr: str):
        """Tokenizes the expression

        Args:
            expr (str): Expression string

        Returns:
            list: List of tokens
        """
        line, col = 1, 0

        if not expr:
            return []

        expr += '~'
        tokens = []
        word = ''
        quoted = ''

        abbrevs = sorted(self.abbrev_prefixes.items(),
                         key=lambda x: len(x[0]), reverse=True)

        def _finish(word):
            for pref, lookup in abbrevs:
                if word.startswith(pref):
                    ret = list(lookup)
                    ret += [self.parse_literal(word[len(pref):])
                            ] if word != pref else []
                    return ret

            if word.startswith(':') and word[1:] in self.shortcuts:
                return self.shortcuts[word[1:]]
            return [self.parse_literal(word)] if word else []

        def _test_op(last, char):
            for last_char in range(self.max_operator_len-1, 0, -1):
                if _Operator(last[-last_char:] + char) in self.priorities:
                    char = _Operator(last[-last_char:] + char)
                    return last_char, char
            if _Operator(char) in self.priorities:
                return 0, char
            return -1, ''

        escaped = False
        commented = False

        for char in expr:
            # skip comments
            col += 1

            if char == '\n':
                line += 1
                col = 1

            if char == '\n' and commented:
                commented = False
                continue

            if not quoted and char == '/' and word.endswith('/'):
                word = word[:-1]
                commented = True
                continue

            if commented:
                continue

            # dealing escapes and quotes
            if char == '\\' and not escaped and quoted != '`':
                escaped = True
                continue
            if escaped is True:
                if char in 'ux':
                    escaped = char
                else:
                    word += {
                        'n': '\n',
                        'b': '\b',
                        't': '\t',
                        'f': '\f',
                        'r': '\r',
                    }.get(char, char)
                    escaped = False
                continue
            elif isinstance(escaped, (_str, str)):
                if escaped.startswith('u'):
                    escaped += char
                    if len(escaped) == 5:
                        word += chr(int(escaped[1:], 16))
                        escaped = False
                elif escaped.startswith('x'):
                    escaped += char
                    if len(escaped) == 3:
                        word += chr(int(escaped[1:], 16))
                        escaped = False
                continue

            if char in '`\'"':
                if quoted:
                    if quoted == char:
                        quoted = ''
                        tokens.append(_Literal(word, line, col))
                        word = ''
                        continue
                else:
                    quoted = char
                    continue
            if quoted:
                word += char
                continue

            # hereafter, not quoted
            if self.allow_spacing and SPACING_PATTERN.match(char):
                continue

            # single parentheses
            if char in '()':
                tokens += _finish(word)
                if char == '(' and ((word and word not in self.priorities and word != '(')
                                    or (not word and len(tokens) > 0 and tokens[-1] == ')')):
                    tokens.append(_Operator('__fn__', line, col))
                elif char == ')' and len(tokens) > 0 and tokens[-1] == '(':
                    tokens.append({})
                word = ''
                tokens.append(_Operator(char, line, col))
                continue

            # list
            if char in '[]':
                tokens += _finish(word)
                if char == '[':
                    if (word and word not in self.priorities and word != '[') \
                            or (not word and len(tokens) > 0 and tokens[-1] == ']'):
                        tokens.append(_Operator('__fn__', line, col))
                    tokens.append(_Operator('(', line, col))
                    tokens.append(_Operator('__list__', line, col))
                    tokens.append(_Operator('[', line, col))
                else:
                    if tokens and tokens[-1] == '[':
                        tokens.append([])
                    tokens.append(_Operator(']', line, col))
                    tokens.append(_Operator(')', line, col))

                word = ''
                continue

            # dealing with multi-character operators
            if not word and tokens and isinstance(tokens[-1], _Operator):
                flag, operator = _test_op(tokens[-1], char)
                if operator:
                    if flag:
                        tokens[-1] = tokens[-1][:-flag]
                        if tokens[-1] == '':
                            tokens = tokens[:-1]
                    tokens.append(_Operator(operator, line, col))
                    continue
            elif word:
                flag, operator = _test_op(word, char)
                if operator:
                    if flag:
                        word = word[:-flag]
                    tokens += _finish(word)
                    word = ''
                    tokens.append(_Operator(operator, line, col))
                    continue
            elif char in self.priorities:
                tokens.append(_Operator(char, line, col))
                continue

            word += char

        stack = []
        result = []
        last_t = _Operator
        for token in tokens[:-1]:
            token_type = type(token)
            if token == ',' and stack and stack[-1] == '[':
                token = _Operator('__sep__', line, col, bundle=stack[-1])
            elif token_type is _Operator and token in self.operators and last_t is _Operator \
                    and (not stack or stack[-1] != '['):
                token = _DefaultOperator(token, line, col)
            if token == '(':
                stack.append(token)
            elif token == '[':
                stack.append(token)
            elif token == ')' and stack and stack[-1] == '(':
                stack.pop()
            elif token == ']' and stack and stack[-1] == '[':
                stack.pop()
            result.append(token)
            last_t = token_type if token not in ('(', ')') else _str

        self.logger(' '.join([repr(_) for _ in result]))
        return result

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
        if re.match(r'^[\+\-]?\d+(\.\d+)?$', expr):
            return float(expr) if '.' in expr else int(expr)
        elif expr.lower() in ['true', 'false']:
            return expr.lower() == 'true'
        elif expr.lower() in ['none', 'null']:
            return None
        elif re.match(r'^[\+\-]?(\d+)[ymdHMS]$', expr):
            offset = int(expr[:-1])
            offset *= {'y': 365, 'm': 30}.get(expr[-1], 1)
            unit = {
                'H': 'hours',
                'M': 'minutes',
                'S': 'seconds',
                'd': 'days',
                'm': 'days',
                'y': 'days'
            }[expr[-1]]
            dateval = datetime.datetime.utcnow(
            ) + datetime.timedelta(**{unit: offset})
            if self.force_timestamp:
                dateval = dateval.timestamp()
            return dateval
        elif re.match(r'^(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{4})([\sT]|$)', expr):
            dateval = dateutil.parser.parse(expr)
            if self.force_timestamp:
                dateval = dateval.timestamp()
            return dateval
        return expr

    def expand_query(self, token: Any, operator: str, opa: MongoOperand):
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
                operator == '=' and var_token):
            operator = self.operators.get(operator, '$eq')
            if operator == '$regex':
                return {
                    '$regexMatch': {
                        'input': token,
                        'regex': opa,
                        'options': '-i'
                    }
                }
            return {
                operator: [token, opa]
            }

        if operator in self.operators:
            opa = {self.operators[operator]: opa}
            if self.operators[operator] == '$regex':
                opa['$options'] = '-i'
                opa['$regex'] = str(opa['$regex'])

        elif operator == '__fn__':
            token = f'${token}'
            operator = '='

        if isinstance(token, (_str, str)):
            if token == 'id' or token.endswith('.id'):
                token = token[:-2] + '_id'
            if (token == '_id' or token.endswith('._id')) and isinstance(opa, (_str, str))\
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

        elif isinstance(token, _list):
            token = token.literal
            return token

        return token

    def split_field_ops(self, token):
        """Split field name and operator

        Args:
            token (str): String with field name and operator

        Returns:
            Tuple[str, str]: A type of (<field name>, <operator>)
        """
        for operator in sorted(self.priorities, key=len, reverse=True):
            operator = str(operator)
            if operator in token:
                qfield, opa = token.split(operator, 1)
                if not qfield:
                    qfield = self.default_field
                return qfield, operator, opa
        return self.default_field, self.default_op, token

    def force_operand(self, arg):
        """Force input value to convert to MongoOperand

        Args:
            v (Any): Any valid value

        Returns:
            MongoOperand: Result
        """
        if isinstance(arg, (_str, str)):
            return MongoOperand(self.expand_query(self.default_field, self.default_op, str(arg)))
        if isinstance(arg, _list):
            return MongoOperand(arg.literal)
        if isinstance(arg, MongoOperand):
            return arg
        return MongoOperand(arg)

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
            if not isinstance(token, _Operator):
                post.append(token)
            else:
                if token not in (')', ']') and \
                    (not stack or token in ('(', '[') or stack[-1] in ('(', '[')
                        or self.priorities[token] > self.priorities[stack[-1]]):
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
                                self.priorities[token] <= self.priorities[stack[-1]]:
                            post.append(stack.pop())
                        else:
                            stack.append(token)
                            break

        while stack:
            post.append(stack.pop())

        self.logger(' '.join([repr(_) for _ in post]))

        opers = []
        for token in post:
            self.logger(repr(token), 'opers=', opers)
            try:
                if not isinstance(token, _Operator):
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

                    if opers:
                        op_a = opers.pop()
                        if isinstance(op_a, MongoOperand):
                            op_a = op_a()
                        if isinstance(op_a, _str):
                            op_a = str(op_a)

                    if opers:
                        op_b = opers.pop()
                        if isinstance(op_b, MongoOperand):
                            op_b = op_b()
                        if isinstance(op_b, _str):
                            op_b = str(op_b)

                        if isinstance(op_b, (list, _list)):
                            val = list(op_b)
                        else:
                            val = [MongoOperand(op_b)()]

                        if isinstance(op_a, (list, _list)) and token == '=>':
                            val += op_a
                        else:
                            val.append(op_a)
                    else:
                        val = op_a
                    opers.append(MongoOperand(val))
                elif token == '__sep__':
                    op_b = _list([], token.bundle)
                    if len(opers) >= 2:
                        op_a, op_b = opers.pop(), opers.pop()
                        if isinstance(op_b, _list) and op_b.bundle is token.bundle:
                            op_b.append(MongoOperand(op_a)())
                        else:
                            op_b = _list([op_b, op_a], token.bundle)
                    opers.append(op_b)
                elif token == '__list__':
                    if opers:
                        op_b = opers.pop()
                        if isinstance(op_b, _list):
                            op_b = op_b.literal
                            opers.append(op_b)
                        elif isinstance(op_b, list):
                            opers.append(op_b)
                        elif isinstance(op_b, _Operator):
                            opers.append(op_b)
                            opers.append([])
                        elif isinstance(op_b, _str):
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
                elif token in self.priorities:
                    opa = opers.pop()
                    if isinstance(opa, _str):
                        opa = str(opa)
                    elif isinstance(opa, _list):
                        opa = opa.literal

                    qfield = self.default_field if isinstance(
                        token, _DefaultOperator) else opers.pop()
                    if isinstance(qfield, _str):
                        opa = str(qfield)
                    if token == '__fn__':
                        if isinstance(qfield, MongoOperand):
                            val, *_ = qfield().values()
                            val.update(**opa())
                            opers.append(qfield)
                        elif qfield in self.functions:
                            func_result = self.functions[qfield](opa)
                            opers.append(MongoOperand(func_result))
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
