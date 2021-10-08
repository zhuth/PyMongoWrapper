from .mongobase import *
from .mongofield import *
from bson import ObjectId
import datetime, time
import json
import re


F = MongoOperandFactory(MongoField)
OBJECTID_PATTERN = re.compile(r'^[0-9A-Fa-f]{24}$')
SPACING_PATTERN = re.compile(r'\s')


class _str:
    
    def __init__(self, literal, line=0, col=0) -> None:
        self.literal = str(literal)
        if line == 0 and col == 0 and isinstance(literal, _str):
            line, col = literal.line, literal.col
        self.line, self.col = line, col
        
    def __repr__(self) -> str:
        return f'{self.literal}/{type(self).__name__}(@{self.line}:{self.col})'
    
    def __str__(self) -> str:
        return self.literal
    
    def __add__(self, another):
        if not isinstance(another, _str):
            another = _str(another, 1<<31, 1<<31)
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


class _Operator(_str):
    pass


class _Literal(_str):
    pass


class _DefaultOperator(_Operator):
    pass


class EvaluationError(Exception):

    def __init__(self, token) -> None:
        if not isinstance(token, _str):
            token = _str(token, 0, 0)
        self.token = token
        
    def __str__(self) -> str:
        return f'{type(self).__name__}: {repr(self.token)}'


class QueryExprParser:

    def __init__(self, abbrev_prefixes={}, shortcuts={}, functions={}, force_timestamp=True, allow_spacing=False, operators={
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
    }, verbose=False):

        self.force_timestamp = force_timestamp
        if verbose:
            self.logger = print
        else:
            self.logger = lambda *a: ''

        self.allow_spacing = allow_spacing
        
        self.shortcuts = shortcuts
        self.operators = operators
        for op in operators:
            priorities[op] = 20
        priorities = {_str(k, 0, 0): v for k, v in priorities.items()}
        self.priorities = priorities
        self.max_operator_len = max(map(lambda x: len(x) if not x.startswith('__') else 0, self.priorities))
       
        self.default_field = '$text'
        self.default_op = '%%'
        if None in abbrev_prefixes: 
            self.default_field, self.default_op, _ = self.split_field_ops(abbrev_prefixes[None])
            del abbrev_prefixes[None]
        
        self.abbrev_prefixes = {}
        for k in abbrev_prefixes:
            abbrev_prefixes[k] = self.tokenize_expr(abbrev_prefixes[k])
        self.abbrev_prefixes = abbrev_prefixes
        
        self.functions = functions
        self.functions['_json'] = lambda x: json.loads(str(x))

    def tokenize_expr(self, expr):
        
        line, col = 1, 0
        
        if not expr:
            return []

        expr += '~'
        l = []
        w = ''
        quoted = ''

        def _w(w):
            for pref, lookup in sorted(self.abbrev_prefixes.items(), key=lambda x: len(x[0]), reverse=True):
                if w.startswith(pref):
                    ret = list(lookup)
                    ret += [self.expand_literals(w[len(pref):])] if w != pref else []
                    return ret
            else:
                return [self.expand_literals(w)] if w else []

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
            
            if not quoted and c == '/' and w.endswith('/'):
                w = w[:-1]
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
                    w += {
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
                        w += chr(int(escaped[1:], 16))
                        escaped = False
                elif escaped.startswith('x'):
                    escaped += c
                    if len(escaped) == 3:
                        w += chr(int(escaped[1:], 16))
                        escaped = False
                continue

            if c in '`\'"':
                if quoted:
                    if quoted == c:
                        quoted = ''
                        l.append(_Literal(w, line, col))
                        w = ''
                        continue
                else:
                    quoted = c
                    continue
            if quoted:
                w += c
                continue

            # hereafter, not quoted
            if self.allow_spacing and SPACING_PATTERN.match(c):
                continue

            # single parentheses
            if c in '()':
                l += _w(w)
                if c == '(' and ((w and w not in self.priorities and w != '(') or (not w and len(l) > 0 and l[-1] == ')')):
                    l.append(_Operator('__fn__', line, col))
                elif c == ')' and len(l) > 0 and l[-1] == '(':
                    l.append({})
                w = ''
                l.append(_Operator(c, line, col))
                continue

            # dealing with multi-character operators
            if not w and l and isinstance(l[-1], _Operator):
                cl, op = _test_op(l[-1], c)
                if op:
                    if cl:
                        l[-1] = l[-1][:-cl]
                        if l[-1] == '': l = l[:-1]
                    l.append(_Operator(op, line, col))
                    continue
            elif w:
                cl, op = _test_op(w, c)
                if op:
                    if cl:
                        w = w[:-cl]
                    l += _w(w)
                    w = ''
                    l.append(_Operator(op, line, col))
                    continue
            elif c in self.priorities:
                l.append(_Operator(c, line, col))
                continue

            w += c
        
        r = []
        last_t = _Operator
        for t in l[:-1]:
            tt = type(t)
            if tt is _Operator and t in self.operators and last_t is _Operator:
                t = _DefaultOperator(t, line, col)
            r.append(t)
            last_t = tt

        self.logger(' '.join([repr(_) for _ in r]))
        return r

    def expand_literals(self, expr):
        if re.match(r'^[\+\-]?\d+(\.\d+)?$', expr):
            return float(expr) if '.' in expr else int(expr)
        elif expr.lower() in ['true', 'false']:
            return expr.lower() == 'true'
        elif expr.lower() in ['none', 'null']:
            return None
        elif expr == '[]':
            return []
        elif re.match(r'^\d{4}\-\d{1,2}\-\d{1,2}$', expr):
            dt = datetime.datetime.strptime(expr, '%Y-%m-%d')
            if self.force_timestamp: dt = dt.timestamp()
            return dt
        elif re.match(r'^\d{4}\-\d{1,2}\-\d{1,2} \d{1,2}\:\d{2}\:d{2}$', expr):
            dt = datetime.datetime.strptime(expr, '%Y-%m-%d %H:%M:%S')
            if self.force_timestamp: dt = dt.timestamp()
            return dt
        elif expr.startswith('$') and ':' in expr:
            op, oa = expr.split(':', 1)
            oa = self.expand_literals(oa)
            if op == '$id' and isinstance(oa, (_str, str)) and OBJECTID_PATTERN.match(oa):
                return ObjectId(str(oa))
            return (op, oa)
        return expr

    def parse_dt_span(self, dt_or_span):
        dt_or_span = self.expand_literals(str(dt_or_span))
        
        if isinstance(dt_or_span, datetime.datetime):
            return int(dt_or_span.timestamp())

        elif isinstance(dt_or_span, int):
            if abs(dt_or_span) <= 366*86400:
                return int(time.time() + dt_or_span)
            else:
                return dt_or_span
            
        elif isinstance(dt_or_span, str) and re.match(r'^[\+\-]?(\d+)([ymwd])$', dt_or_span):
            offset = int(dt_or_span[:-1])
            unit = dt_or_span[-1]
            offset *= 86400
            if unit == 'w':
                offset *= 7
            elif unit == 'm':
                offset *= 31
            elif unit == 'y':
                offset *= 365
            return int(time.time() + offset)

        return 0

    def expand_query(self, token, op, opa):

        self.logger(token, op, opa)
            
        if isinstance(opa, list) and len(opa) == 1:
            opa = opa[0]
        
        if op in self.operators:
            if token.startswith('$'):
                opa = {
                    self.operators[op]: [token, opa]
                }
                token = '$expr'
            else:
                opa = {self.operators[op]: opa}
                if self.operators[op] == '$regex':
                    opa['$options'] = '-i'

        elif op == '__fn__':
            token = f'${token}'
            op = '='
        
        if isinstance(token, (_str, str)):
            if token == 'id' or token.endswith('.id'):
                token = token[:-2] + '_id'
            if (token == '_id' or token.endswith('._id')) and isinstance(opa, (_str, str)) and OBJECTID_PATTERN.match(opa):
                opa = ObjectId(str(opa))

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
        for op in sorted(self.priorities, key=lambda x: len(x), reverse=True):
            op = str(op)
            if op in token:
                qfield, opa = token.split(op, 1)
                if not qfield: qfield = self.default_field
                return qfield, op, opa
        else:
            return self.default_field, self.default_op, token

    def force_operand(self, v):
        if isinstance(v, (_str, str)):
            return MongoOperand(self.expand_query(self.default_field, self.default_op, str(v)))
        if isinstance(v, MongoOperand):
            return v
        return MongoOperand(v)

    def eval_tokens(self, tokens):
        post = []
        stack = []
        for t in tokens:
            if not isinstance(t, _Operator):
                post.append(t)
            else:
                if t != ')' and (not stack or t == '(' or stack[-1] == '('
                                 or self.priorities[t] > self.priorities[stack[-1]]):
                    stack.append(t)
                elif t == ')':
                    while stack and stack[-1] != '(':
                        post.append(stack.pop())
                    stack.pop()
                else:
                    while True:
                        if stack and stack[-1] != '(' and self.priorities[t] <= self.priorities[stack[-1]]:
                            post.append(stack.pop())
                        else:
                            stack.append(t)
                            break
        
        while stack:
            post.append(stack.pop())

        self.logger(' '.join([repr(_) for _ in post]))

        opers = []
        for token in post:
            try:
                if not isinstance(token, _Operator):
                    opers.append(token)
                    continue
                if token == '&' or token == ',':
                    a, b = self.force_operand(opers.pop()), self.force_operand(opers.pop())
                    opers.append(b & a)
                elif token == '|':
                    a, b = self.force_operand(opers.pop()), self.force_operand(opers.pop())
                    opers.append(b | a)
                elif token in ('=>', ';'):
                    a = []
                    
                    if opers:
                        a = opers.pop()
                        if isinstance(a, MongoOperand): a = a()
                        if isinstance(a, _str): a = str(a)
                    
                    if opers:
                        b = opers.pop()
                        if isinstance(b, MongoOperand): b = b()
                        if isinstance(b, _str): b = str(b)
                        
                        if isinstance(b, (tuple, list)): v = b
                        else: v = [b]
                        
                        if isinstance(a, list):
                            v += a
                        else:
                            v.append(a)
                    else:
                        v = a
                    opers.append(MongoOperand(v))
                elif token == '~':
                    opers.append(~self.force_operand(opers.pop()))
                elif token == '.':
                    a, b = opers.pop(), opers.pop()
                    opers.append(self.expand_literals(f'{b}.{a}'))
                elif token in self.priorities:
                    opa = opers.pop()
                    if isinstance(opa, _str): opa = str(opa)
                    
                    qfield = self.default_field if isinstance(token, _DefaultOperator) else opers.pop()
                    if isinstance(qfield, _str): opa = str(qfield)
                    
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
                elif token.startswith(':'):
                    opers.append(
                        MongoOperand(self.shortcuts.get(token[1:], token)))
                else:
                    opers.append(token)
            except Exception as ex:
                raise EvaluationError(token)

        return opers[0] if opers else None

    def eval(self, expr):
        v = self.eval_tokens(self.tokenize_expr(expr))
        if v is None: return {}
        if isinstance(v, dict): return v
        if not isinstance(v, MongoOperand): v = self.force_operand(v)
        return v()
