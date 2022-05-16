"""Parse query expressions"""

from .mongobase import *
from .mongofield import *
from bson import ObjectId
import datetime
import time
import json
import re
import math
import dateutil.parser


F = MongoOperandFactory(MongoField)
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
        return _str(self.literal + another.literal, min(self.line, another.line), min(self.col, another.col))

    def __getitem__(self, k):
        return _str(self.literal[k], self.line, self.col)

    def __eq__(self, o: object) -> bool:
        return str(o) == self.literal

    def __hash__(self) -> int:
        return hash(self.literal)

    def __len__(self):
        return len(self.literal)

    def startswith(self, w):
        return self.literal.startswith(w)


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

    def __init__(self, init=None, bundle=None):
        if init and not isinstance(init, list):
            init = list(init)
        self.literal = [] if init is None else init
        self.bundle = bundle

    def append(self, element):
        """Appending element to the list"""
        self.literal.append(element)

    def __iter__(self):
        return self.literal

    def __add__(self, another):
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

    def __init__(self, abbrev_prefixes={}, functions={}, force_timestamp=True, allow_spacing=False, operators={
        '>': '$gt',
        '<': '$lt',
        '>=': '$gte',
        '<=': '$lte',
        '%': '$regex',
        '!=': '$ne',
        '%%': '$search'
    }, priorities={
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
    }, verbose=False):
        """
        Args:
            abbrev_prefixes (dict, optional): Abbreviative prefixes. Defaults to {}.
            functions (dict, optional): Python functions to handle special function calls in expression. Defaults to {}.
            force_timestamp (bool, optional): Force the use of timestamp instead of datetime.datetime objects. Defaults to True.
            allow_spacing (bool, optional): Allow (ignore) spacing in expressions. Defaults to False.
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
        self.operators = operators
        for op in operators:
            priorities[op] = 20
        priorities = {_str(k, 0, 0): v for k, v in priorities.items()}
        self.priorities = priorities
        self.max_operator_len = max(
            map(lambda x: len(x) if not x.startswith('__') else 0, self.priorities))

        self.default_field = '$text'
        self.default_op = '%%'
        if None in abbrev_prefixes:
            self.default_field, self.default_op, _ = self.split_field_ops(
                abbrev_prefixes[None])
            del abbrev_prefixes[None]

        self.abbrev_prefixes = {}
        for k in abbrev_prefixes:
            abbrev_prefixes[k] = self.tokenize_expr(abbrev_prefixes[k])
        self.abbrev_prefixes = abbrev_prefixes

        self.functions = functions
        self.functions['json'] = lambda x: json.loads(str(x))
        self.functions['ObjectId'] = self.functions['objectId'] = ObjectId

    def tokenize_expr(self, expr):
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

        def _finish(w):
            for pref, lookup in abbrevs:
                if w.startswith(pref):
                    ret = list(lookup)
                    ret += [self.parse_literal(w[len(pref):])
                            ] if w != pref else []
                    return ret
            else:
                if w.startswith(':') and w[1:] in self.shortcuts:
                    return self.shortcuts[w[1:]]
                return [self.parse_literal(w)] if w else []

        def _test_op(last, c):
            for cl in range(self.max_operator_len-1, 0, -1):
                if _Operator(last[-cl:] + c) in self.priorities:
                    c = _Operator(last[-cl:] + c)
                    return cl, c
            if _Operator(c) in self.priorities:
                return 0, c
            return -1, ''

        escaped = False
        commented = False

        for c in expr:
            # skip comments
            col += 1

            if c == '\n':
                line += 1
                col = 1

            if c == '\n' and commented:
                commented = False
                continue

            if not quoted and c == '/' and word.endswith('/'):
                word = word[:-1]
                commented = True
                continue

            if commented:
                continue

            # dealing escapes and quotes
            if c == '\\' and not escaped and quoted != '`':
                escaped = True
                continue
            if escaped is True:
                if c in 'ux':
                    escaped = c
                else:
                    word += {
                        'n': '\n',
                        'b': '\b',
                        't': '\t',
                        'f': '\f',
                        'r': '\r',
                    }.get(c, c)
                    escaped = False
                continue
            elif isinstance(escaped, (_str, str)):
                if escaped.startswith('u'):
                    escaped += c
                    if len(escaped) == 5:
                        word += chr(int(escaped[1:], 16))
                        escaped = False
                elif escaped.startswith('x'):
                    escaped += c
                    if len(escaped) == 3:
                        word += chr(int(escaped[1:], 16))
                        escaped = False
                continue

            if c in '`\'"':
                if quoted:
                    if quoted == c:
                        quoted = ''
                        tokens.append(_Literal(word, line, col))
                        word = ''
                        continue
                else:
                    quoted = c
                    continue
            if quoted:
                word += c
                continue

            # hereafter, not quoted
            if self.allow_spacing and SPACING_PATTERN.match(c):
                continue

            # single parentheses
            if c in '()':
                tokens += _finish(word)
                if c == '(' and ((word and word not in self.priorities and word != '(') or (not word and len(tokens) > 0 and tokens[-1] == ')')):
                    tokens.append(_Operator('__fn__', line, col))
                elif c == ')' and len(tokens) > 0 and tokens[-1] == '(':
                    tokens.append({})
                word = ''
                tokens.append(_Operator(c, line, col))
                continue

            # list
            if c in '[]':
                tokens += _finish(word)
                if c == '[':
                    if (word and word not in self.priorities and word != '[') or (not word and len(tokens) > 0 and tokens[-1] == ']'):
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
                cl, op = _test_op(tokens[-1], c)
                if op:
                    if cl:
                        tokens[-1] = tokens[-1][:-cl]
                        if tokens[-1] == '':
                            tokens = tokens[:-1]
                    tokens.append(_Operator(op, line, col))
                    continue
            elif word:
                cl, op = _test_op(word, c)
                if op:
                    if cl:
                        word = word[:-cl]
                    tokens += _finish(word)
                    word = ''
                    tokens.append(_Operator(op, line, col))
                    continue
            elif c in self.priorities:
                tokens.append(_Operator(c, line, col))
                continue

            word += c

        stack = []
        r = []
        last_t = _Operator
        for t in tokens[:-1]:
            tt = type(t)
            if t == ',' and stack and stack[-1] == '[':
                t = _Operator('__sep__', line, col, bundle=stack[-1])
            elif tt is _Operator and t in self.operators and last_t is _Operator and (not stack or stack[-1] != '['):
                t = _DefaultOperator(t, line, col)
            if t == '(':
                stack.append(t)
            elif t == '[':
                stack.append(t)
            elif t == ')' and stack and stack[-1] == '(':
                stack.pop()
            elif t == ']' and stack and stack[-1] == '[':
                stack.pop()
            r.append(t)
            last_t = tt if t not in ('(', ')') else _str

        self.logger(' '.join([repr(_) for _ in r]))
        return r

    def set_shortcut(self, name, expr):
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

    def parse_literal(self, expr):
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
            unit = {
                'H': 'hours',
                'M': 'minutes',
                'S': 'seconds',
                'd': 'days',
                'm': 'months',
                'y': 'years'
            }[expr[-1]]
            dt = datetime.datetime.utcnow(
            ) + datetime.timedelta(**{unit: offset})
            if self.force_timestamp:
                dt = dt.timestamp()
            return dt
        elif re.match(r'^(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{4})([\sT]|$)', expr):
            dt = dateutil.parser.parse(expr)
            if self.force_timestamp:
                dt = dt.timestamp()
            return dt
        elif expr.startswith('$') and ':' in expr:
            op, oa = expr.split(':', 1)
            oa = self.parse_literal(oa)
            if op == '$id' and isinstance(oa, (_str, str)) and OBJECTID_PATTERN.match(oa):
                return ObjectId(str(oa))
            return (op, oa)
        return expr

    def expand_query(self, token, op, opa):
        """Parse token, operator, and operand

        Args:
            token (Any): Token
            op (str): Operator
            opa (MongoOperand): MongoOperand

        Returns:
            Any: Result after opration
        """
        self.logger('expand', token, op, opa)

        if isinstance(token, MongoOperand):
            token = token()
        if isinstance(opa, MongoOperand):
            opa = opa()

        var_token = MongoOperand._key(token).startswith('$')
        var_opa = MongoOperand._key(opa).startswith('$')
        if (op in self.operators and (var_token or var_opa)) or (op == '=' and var_token and var_opa):
            return {
                self.operators.get(op, '$eq'): [token, opa]
            }

        if op in self.operators:
            opa = {self.operators[op]: opa}
            if self.operators[op] == '$regex':
                opa['$options'] = '-i'
                opa['$regex'] = str(opa['$regex'])

        elif op == '__fn__':
            token = f'${token}'
            op = '='

        if isinstance(token, (_str, str)):
            if token == 'id' or token.endswith('.id'):
                token = token[:-2] + '_id'
            if (token == '_id' or token.endswith('._id')) and isinstance(opa, (_str, str)) and OBJECTID_PATTERN.match(opa):
                opa = ObjectId(str(opa))
            if token == '$match':
                if not isinstance(opa, (dict, list)):
                    opa = self.expand_query(
                        self.default_field, self.default_op, opa)
                if MongoOperand._key(opa) in self.operators.values() or MongoOperand._key(opa) == '$eq':
                    opa = {'$expr': opa}
        elif isinstance(token, _list):
            token = token.literal

        flds = token.split('$')

        if len(flds) > 1:
            v = {flds[0]: {}}
            d = v[flds[0]]
            for f in flds[1:-1]:
                d['$' + f] = {}
                d = d['$' + f]
            d['$' + flds[-1]] = opa
        else:
            v = {flds[0]: opa}

        if '' in v:
            v = v['']

        return v

    def split_field_ops(self, token):
        """Split field name and operator

        Args:
            token (str): String with field name and operator

        Returns:
            Tuple[str, str]: A type of (<field name>, <operator>)
        """
        for op in sorted(self.priorities, key=lambda x: len(x), reverse=True):
            op = str(op)
            if op in token:
                qfield, opa = token.split(op, 1)
                if not qfield:
                    qfield = self.default_field
                return qfield, op, opa
        else:
            return self.default_field, self.default_op, token

    def force_operand(self, v):
        """Force input value to convert to MongoOperand

        Args:
            v (Any): Any valid value

        Returns:
            MongoOperand: Result
        """
        if isinstance(v, (_str, str)):
            return MongoOperand(self.expand_query(self.default_field, self.default_op, str(v)))
        if isinstance(v, _list):
            return MongoOperand(v.literal)
        if isinstance(v, MongoOperand):
            return v
        return MongoOperand(v)

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
        for t in tokens:
            if not isinstance(t, _Operator):
                post.append(t)
            else:
                if t not in (')', ']') and (not stack or t in ('(', '[') or stack[-1] in ('(', '[')
                                            or self.priorities[t] > self.priorities[stack[-1]]):
                    stack.append(t)
                elif t == ')':
                    while stack and stack[-1] != '(':
                        post.append(stack.pop())
                    if stack:
                        stack.pop()
                    else:
                        raise QueryExpressionError(t)
                elif t == ']':
                    while stack and stack[-1] != '[':
                        post.append(stack.pop())
                    if stack:
                        stack.pop()
                    else:
                        raise QueryExpressionError(t)
                else:
                    while True:
                        if stack and stack[-1] not in ('(', '[') and self.priorities[t] <= self.priorities[stack[-1]]:
                            post.append(stack.pop())
                        else:
                            stack.append(t)
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
                    a, b = self.force_operand(
                        opers.pop()), self.force_operand(opers.pop())
                    opers.append(b & a)
                elif token == '|':
                    a, b = self.force_operand(
                        opers.pop()), self.force_operand(opers.pop())
                    opers.append(b | a)
                elif token in ('=>', ';'):
                    a = []

                    if opers:
                        a = opers.pop()
                        if isinstance(a, MongoOperand):
                            a = a()
                        if isinstance(a, _str):
                            a = str(a)

                    if opers:
                        b = opers.pop()
                        if isinstance(b, MongoOperand):
                            b = b()
                        if isinstance(b, _str):
                            b = str(b)

                        if isinstance(b, (list, _list)):
                            v = list(b)
                        else:
                            v = [MongoOperand(b)()]

                        if isinstance(a, (list, _list)) and token == '=>':
                            v += a
                        else:
                            v.append(a)
                    else:
                        v = a
                    opers.append(MongoOperand(v))
                elif token == '__sep__':
                    b = _list([], token.bundle)
                    if len(opers) >= 2:
                        a, b = opers.pop(), opers.pop()
                        if isinstance(b, _list) and b.bundle is token.bundle:
                            b.append(MongoOperand(a)())
                        else:
                            b = _list([b, a], token.bundle)
                    opers.append(b)
                elif token == '__list__':
                    if opers:
                        b = opers.pop()
                        if isinstance(b, _list):
                            b = b.literal
                            opers.append(b)
                        elif isinstance(b, list):
                            opers.append(b)
                        elif isinstance(b, _Operator):
                            opers.append(b)
                            opers.append([])
                        elif isinstance(b, _str):
                            opers.append([str(b)])
                        else:
                            opers.append([MongoOperand(b)()])
                    else:
                        opers.append([])
                elif token == '~':
                    opers.append(~self.force_operand(opers.pop()))
                elif token == '.':
                    a, b = opers.pop(), opers.pop()
                    opers.append(self.parse_literal(f'{b}.{a}'))
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
                            v, *_ = qfield._literal.values()
                            v.update(**opa())
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
                ee = QueryExpressionError(token)
                ee.inner_exception = ex
                raise(ee)

        return opers[0] if opers else None

    def parse(self, expr):
        """Parse the expression

        Args:
            expr (str): Expression

        Returns:
            Any: Parsed result
        """
        v = self.parse_tokens(self.tokenize_expr(expr))
        if v is None or isinstance(v, (list, dict)):
            return v
        if not isinstance(v, MongoOperand):
            v = self.force_operand(v)
        return v()

    def parse_sort(self, sort_str):
        """Parse sorting expression

        Args:
            sort_str (str): Sorting expression

        Returns:
            List[Tuple[str, int]]: Sorting object
        """
        return MongoField.parse_sort(*sort_str.split(','))


class QueryExprEvaluator:
    """Evaluate Query Expression
    """

    def __init__(self, implementations: dict = None):
        """Initialize Query Expression Evaluator

        Args:
            implementations (dict, optional): Implementations of functions. Defaults to None.
        """
        self.implementations = self._default_implementations()
        if implementations:
            self.implementations.update(**implementations)

    def _operator(self, operator_name):
        operator_name = operator_name.lstrip('$')
        operator = {
            'lte': 'le',
            'gte': 'ge',
            '': 'eq'
        }.get(operator_name, operator_name)
        return f'__{operator}__'

    def _compare(self, op, *args):
        op = self._operator(op)
        if len(args) == 2:
            a, b = args
            return self._getfunc(a, op)(b)

    def _getattr(self, obj, key, default=None):
        if key.startswith('$'):
            key = key[1:]

        if key == '$ROOT':
            return obj

        if obj is None:
            return obj

        if '.' in key:
            for key_seg in key.split('.'):
                obj = _getattr(obj, key_seg, default)
            return obj

        if isinstance(obj, dict):
            return obj.get(key, default)

        if isinstance(obj, list) and RE_DIGITS.match(key):
            return obj[int(key)] if 0 <= int(key) < len(obj) else default

        return getattr(obj, key, default)

    def _test_inputs(self, obj, val, relation='eq'):
        oprname = self._operator(relation)

        if oprname == '__in__':
            return obj in val

        if oprname == '__size__':
            return len(obj) == val

        if isinstance(obj, list):
            arr_result = False
            for input_val in obj:
                arr_result = arr_result or self._getfunc(
                    input_val, oprname)(val)
                if arr_result:
                    break
        else:
            arr_result = self._getfunc(obj, oprname)(val)

        return arr_result

    def _default_implementations(self):

        def _size(obj, val):
            if isinstance(val, (dict, str)):
                return len(self.evaluate(val, obj))
            return 0

        def _first(obj, val):
            for i in self.evaluate(val, obj):
                return i

        def _last(obj, val):
            i = None
            for i in self.evaluate(val, obj):
                pass
            return i

        def _ifNull(obj, *args):
            evaluated = None
            for cond in args[:-1]:
                evaluated = self.evaluate(cond, obj)
                if evaluated is None:
                    return self.evaluate(args[-1], obj)
            return evaluated

        def _cond(obj, cond):
            if isinstance(cond, list):
                assert len(cond) in (
                    2, 3), 'length of cond array should be 2 or 3'
                if_else = cond[2] if len(cond) == 3 else None
                cond, if_then = cond[:2]
            elif isinstance(cond, dict):
                cond, if_then, if_else = cond.get(
                    'if'), cond.get('then'), cond.get('else')
                assert cond and if_then, 'must specify `if` and `then`'

            print(cond, if_then, if_else)
            if self.evaluate(cond, obj):
                return self.evaluate(if_then, obj)
            elif if_else:
                return self.evaluate(if_else, obj)

        def _abs(obj, val):
            return abs(self.evaluate(val, obj))

        def _add(obj, val):
            if isinstance(val, (str, dict)):
                val = self.evaluate(val, obj)
            assert isinstance(val, list), 'argument should be a list'
            return sum([self.evaluate(ele, obj) for ele in val])

        def _substract(obj, val):
            assert isinstance(val, list) and len(
                val) == 2, 'argument should be a list with 2 elements'
            return self.evaluate(val[0], obj) - self.evaluate(val[1], obj)

        def _mod(obj, val):
            assert isinstance(val, list) and len(
                val) == 2, 'argument should be a list with 2 elements'
            return self.evaluate(val[0], obj) % self.evaluate(val[1], obj)

        def _multiply(obj, val):
            assert isinstance(val, list), 'argument should be a list'
            result = 1
            for ele in val:
                result *= self.evaluate(ele, obj)
            return result

        def _divide(obj, val):
            assert isinstance(val, list) and len(
                val) == 2, 'argument should be a list with 2 elements'
            return self.evaluate(val[0], obj) / self.evaluate(val[1], obj)

        def _substract(obj, val):
            assert isinstance(val, list) and len(
                val) == 2, 'argument should be a list with 2 elements'
            return self.evaluate(val[0], obj) - self.evaluate(val[1], obj)

        def _avg(obj, val):
            if isinstance(val, (str, dict)):
                val = self.evaluate(val, obj)
            assert isinstance(val, list), 'argument should be a list'
            return sum([self.evaluate(ele, obj) for ele in val]) / len(val)

        def _max(obj, val):
            if isinstance(val, (str, dict)):
                val = self.evaluate(val, obj)
            assert isinstance(val, list), 'argument should be a list'
            return max([self.evaluate(ele, obj) for ele in val])

        def _min(obj, val):
            if isinstance(val, (str, dict)):
                val = self.evaluate(val, obj)
            assert isinstance(val, list), 'argument should be a list'
            return min([self.evaluate(ele, obj) for ele in val])

        def _concat(obj, val):
            result = ''
            for ele in val:
                result += self.evaluate(ele, obj)
            return result

        def _concatArrays(obj, val):
            result = []
            for ele in val:
                result += self.evaluate(ele, obj)
            return result

        def _convert(obj, inputs):
            input_val = self.evaluate(inputs.get('input'), obj)
            to_ = self.evaluate(inputs.get('to'), obj)
            if to_ in (1, 'double', 19, 'decimal'):
                return float(input_val)
            elif to_ in (2, 'string'):
                return str(input_val)
            elif to_ in (7, 'objectId'):
                return ObjectId(input_val)
            elif to_ in (8, 'bool'):
                return not not input_val
            elif to_ in (9, 'date'):
                return dateutil.parser.parse(str(input_val)) if not isinstance(input_val, datetime.datetime) else input_val
            else:
                return int(input_val)

        def _toString(obj, val):
            return _convert(obj, {'input': val, 'to': 'string'})

        def _toInt(obj, val):
            return _convert(obj, {'input': val, 'to': 'int'})

        def _toLong(obj, val):
            return _toInt(obj, val)

        def _toBool(obj, val):
            return _convert(obj, {'input': val, 'to': 'bool'})

        def _toDate(obj, val):
            return _convert(obj, {'input': val, 'to': 'date'})

        def _toDouble(obj, val):
            return _convert(obj, {'input': val, 'to': 'double'})

        def _toDecimal(obj, val):
            return _toDouble(obj, val)

        def _toObjectId(obj, val):
            return _convert(obj, {'input': val, 'to': 'objectId'})

        def _toLower(obj, val):
            val = self.evaluate(val, obj)
            assert isinstance(val, str), 'argument must resolve to string'
            return val.lower()

        def _toUpper(obj, val):
            val = self.evaluate(val, obj)
            assert isinstance(val, str), 'argument must resolve to string'
            return val.upper()

        def _dateAdd(obj, val):
            start_date = self.evaluate(val.get('startDate'), obj)
            unit = self.evaluate(val.get('unit'), obj)
            amount = self.evaluate(val.get('amount'), obj)
            timezone = self.evaluate(val.get('timezone'), obj)
            assert isinstance(
                start_date, datetime.datetime), 'startDate must resolve to a datetime.datetime object'
            assert isinstance(amount, (float, int)), 'amount must be a number'
            delta = {
                'year': datetime.timedelta(days=amount * 365),
                'quarter': datetime.timedelta(days=amount * 121),
                'week': datetime.timedelta(weeks=amount),
                'month': datetime.timedelta(days=amount * 30),
                'day': datetime.timedelta(days=amount),
                'hour': datetime.timedelta(hours=amount),
                'minute': datetime.timedelta(minutes=amount),
                'second': datetime.timedelta(seconds=amount),
                'millisecond': datetime.timedelta(milliseconds=amount),
            }.get(unit)
            assert delta, 'unit must be one of the following: year quarter week month day hour minute second millisecond'
            if timezone:
                raise NotImplemented()
            return start_date + delta

        def _dateDiff(obj, val):
            assert 'startDate' in val and 'endDate' in val, 'must specify start/end date'
            start_date, end_date = self.evaluate(
                val['startDate'], obj), self.evaluate(val['endDate'], obj)
            assert isinstance(start_date, datetime.datetime) and isinstance(end_date, datetime.datetime), \
                f'start & end date must be datetime.datetime, got {type(start_date)} & {type(end_date)}'
            unit = {
                'year': 365*86400,
                'quarter': 365*86400/4,
                'week': 7*86400,
                'month': 30*86400,
                'day': 86400,
                'hour': 3600,
                'minute': 60,
                'second': 1,
                'millisecond': 0.001
            }.get(self.evaluate(val.get('unit', 'second'), obj))
            assert unit, 'unit must be one of the following: year quarter week month day hour minute second millisecond'
            return (end_date - start_date).total_seconds() / unit

        def _year(obj, val):
            val = self.evaluate(val, obj)
            assert isinstance(val, datetime.datetime)
            return val.year

        def _month(obj, val):
            val = self.evaluate(val, obj)
            assert isinstance(val, datetime.datetime)
            return val.month

        def _day(obj, val):
            val = self.evaluate(val, obj)
            assert isinstance(val, datetime.datetime)
            return val.day

        def _floor(obj, val):
            return math.floor(self.evaluate(val, obj))

        def _ceil(obj, val):
            return math.ceil(self.evaluate(val, obj))

        def _in(obj, val):
            assert isinstance(val, list) and len(
                val) == 2, 'argument must be a list with 2 elements'
            needle, heap = map(lambda x: self.evaluate(x, obj), val)
            return needle in heap

        def _indexOfArray(obj, val):
            assert isinstance(val, list) and 4 >= len(
                val) >= 2, 'argument must be a list with 2-4 elements'
            arr, search, start, end, * \
                _ = map(lambda x: self.evaluate(x, obj), val + [-1, -1, -1])
            try:
                return arr[start:end+1].index(search) + start
            except ValueError:
                return -1

        def _isArray(obj, val):
            assert isinstance(val, list) and len(
                val) == 1, 'argument must be a single-element list'
            return isinstance(self.evaluate(val[0], obj), list)

        def _isNumber(obj, val):
            val = self.evaluate(val, obj)
            return isinstance(val, (float, int))

        def _ltrim(obj, val):
            input_, chars = self.evaluate(val.get('input'), obj), self.evaluate(
                val.get('chars', ' '), obj)
            assert isinstance(input_, str) and isinstance(
                chars, (list, tuple, str))
            return input_.lstrip(chars)

        def _rtrim(obj, val):
            input_, chars = self.evaluate(val.get('input'), obj), self.evaluate(
                val.get('chars', ' '), obj)
            assert isinstance(input_, str) and isinstance(
                chars, (list, tuple, str))
            return input_.rstrip(chars)

        def _trim(obj, val):
            input_, chars = self.evaluate(val.get('input'), obj), self.evaluate(
                val.get('chars', ' '), obj)
            assert isinstance(input_, str) and isinstance(
                chars, (list, tuple, str))
            return input_.strip(chars)

        def _map(obj, val):
            input_, as_, in_ = self.evaluate(
                val.get('input'), obj), '$' + val.get('as', 'iter'), val.get('in', {})
            result = []
            obj[as_] = None
            for ele in input_:
                obj[as_] = ele
                result.append(self.evaluate(in_, obj))
            del obj[as_]
            return result

        def _setField(obj, val):
            field, input_, value = val.get(
                'field'), val.get('input'), val.get('value')
            input_ = self.evaluate(input_, obj)
            assert isinstance(input_, dict), 'input must resolve to a dict'
            value = self.evaluate(value, input_)
            input_[field] = value
            return input_

        def _unsetField(obj, val):
            field, input_ = val.get(
                'field'), val.get('input')
            input_ = self.evaluate(input_, obj)
            assert isinstance(input_, dict), 'input must resolve to a dict'
            if field in input_:
                del input_[field]
            return input_

        def _substrCP(obj, val):
            target, start, length = self.evaluate(val.get('string'), obj), self.evaluate(
                val.get('start'), obj), self.evaluate(val.get('length'), obj)
            return target[start:][:length]

        def _strLenBytes(obj, val):
            target = self.evaluate(val, obj)
            assert isinstance(target, str), 'target must be a string'
            return len(target.encode('utf-8'))

        def _strLenCP(obj, val):
            target = self.evaluate(val, obj)
            assert isinstance(target, str), 'target must be a string'
            return len(target)

        def _strLen(obj, val):
            return _strLenCP(obj, val)

        def _substr(obj, val):
            return _substrCP(obj, val)

        def wrap(func):
            def _wrapped(_, *args):
                return func(*args)
            return _wrapped

        return {
            k[1:]: wrap(v)
            for k, v in locals().items()
            if k.startswith('_')
        }

    def _getfunc(self, obj, func_name):
        func = self._getattr(obj, func_name)
        if func:
            return func
        elif func_name.strip('_') in self.implementations:
            return lambda *args: self.implementations[func_name.strip('_')](self, obj, *args)
        else:
            return lambda *_: None

    def evaluate(self, parsed: dict, obj: object):
        """Evaluate parsed expression to its value, in the context given by obj

        Args:
            parsed (dict): Parsed Query Expression
            obj (object): Context object/dict
        """

        def _append_result(res):
            if result is None:
                return res
            return result and res

        result = None

        if isinstance(parsed, str) and parsed.startswith('$'):
            parsed = {'$': parsed}

        if not isinstance(parsed, dict):
            return parsed

        for key, val in parsed.items():
            if key.startswith('$'):
                if key == '$and':
                    temp = True
                    for element in val:
                        temp = temp and self.evaluate(
                            element, obj)
                        if not temp:
                            break
                elif key == '$or':
                    temp = False
                    for element in val:
                        temp = temp or self.evaluate(
                            element, obj)
                        if temp:
                            break
                elif key == '$not':
                    temp = not self.evaluate(val, obj)
                elif key == '$regex':
                    temp = re.search(val, obj) is not None
                elif key == '$options':
                    continue
                elif key in ('$gt', '$gte', '$eq', '$lt', '$lte', '$ne'):
                    temp = self._compare(
                        key, *[self.evaluate(ele, obj) for ele in val])
                elif key == '$expr':
                    temp = self.evaluate(val, obj)
                elif key == '$':
                    temp = self._getattr(obj, val)
                elif key[1:] in self.implementations:
                    temp = self.implementations[key[1:]](self, obj, val)
                else:
                    temp = self._test_inputs(obj, val, key[1:])

                result = _append_result(temp)

            elif not isinstance(val, dict) or not [1 for v_ in val if v_.startswith('$')]:
                result = _append_result(self._test_inputs(
                    self._getattr(obj, key), val))

            else:
                result = _append_result(self.evaluate(val, self._getattr(
                    obj, key)))

            if result is False:
                return result

        return result
