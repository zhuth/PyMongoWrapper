"""Parse query expressions"""

from .mongobase import *
from .mongofield import *
from bson import ObjectId
import datetime
import time
import json
import re
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
    pass


class _DefaultOperator(_Operator):
    """Representing an operator with default field name"""
    pass


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


class EvaluationError(Exception):
    """Evaluation error
    """

    def __init__(self, token) -> None:
        if not isinstance(token, _str):
            token = _str(token, 0, 0)
        self.token = token

    def __str__(self) -> str:
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
        """Evaluate token, operator, and operand

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

        if (op in self.operators or op == '=') and MongoOperand._key(token).startswith('$') and MongoOperand._key(opa).startswith('$'):
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

    def eval_tokens(self, tokens):
        """Evaluate query expression tokens

        Args:
            tokens (list): List of tokens

        Raises:
            EvaluationError: Evaluation error

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
                        raise EvaluationError(t)
                elif t == ']':
                    while stack and stack[-1] != '[':
                        post.append(stack.pop())
                    if stack:
                        stack.pop()
                    else:
                        raise EvaluationError(t)
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
                ee = EvaluationError(token)
                ee.inner_exception = ex
                raise(ee)

        return opers[0] if opers else None

    def eval(self, expr):
        """Evaluate the result of the expression

        Args:
            expr (str): Expression

        Returns:
            Any: Evaluated result
        """
        v = self.eval_tokens(self.tokenize_expr(expr))
        if v is None or isinstance(v, (list, dict)):
            return v
        if not isinstance(v, MongoOperand):
            v = self.force_operand(v)
        return v()

    def eval_sort(self, sort_str):
        """Evaluate sorting expression

        Args:
            sort_str (str): Sorting expression

        Returns:
            List[Tuple[str, int]]: Sorting object
        """
        return MongoField.parse_sort(*sort_str.split(','))
