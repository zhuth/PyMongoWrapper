from .mongobase import *
from .mongofield import *
from bson import ObjectId
import datetime, time
import json
import re


F = MongoOperandFactory(MongoField)
OBJECTID_PATTERN = re.compile(r'^[0-9A-Fa-f]{24}$')
SPACING_PATTERN = re.compile(r'\s')


class _Operator(str):
    pass


class _Literal(str):
    pass


class _DefaultOperator(_Operator):
    pass


class QueryExprParser:

    def __init__(self, abbrev_prefixes={}, shortcuts={}, force_timestamp=True, allow_spacing=False, operators={
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
        '=>': 2
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

    def tokenize_expr(self, expr):
        if not expr:
            return []

        expr += '~'
        l = []
        w = ''
        quoted = False

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
                if last[-cl:] + c in self.priorities:
                    c = last[-cl:] + c
                    return cl, c
            if c in self.priorities:
                return 0, c
            return -1, ''

        escaped = False
        for c in expr:
            # dealing escapes and quotes
            if c == '\\' and not escaped:
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
            elif isinstance(escaped, str):
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

            if c == '`':
                if quoted:
                    quoted = False
                    l.append(_Literal(w))
                    w = ''
                else:
                    quoted = True
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
                    l.append(_Operator('__fn__'))
                w = ''
                l.append(_Operator(c))
                continue

            # dealing with multi-character operators
            if not w and l and isinstance(l[-1], _Operator):
                cl, op = _test_op(l[-1], c)
                if op:
                    if cl:
                        l[-1] = l[-1][:-cl]
                        if l[-1] == '': l = l[:-1]
                    l.append(_Operator(op))
                    continue
            elif w:
                cl, op = _test_op(w, c)
                if op:
                    if cl:
                        w = w[:-cl]
                    l += _w(w)
                    w = ''
                    l.append(_Operator(op))
                    continue
            elif c in self.priorities:
                l.append(_Operator(c))
                continue

            w += c
        
        r = []
        last_t = _Operator
        for t in l[:-1]:
            tt = type(t)
            if tt is _Operator and t in self.operators and last_t is _Operator:
                t = _DefaultOperator(t)
            r.append(t)
            last_t = tt

        self.logger(' '.join([type(_).__name__ + '/' + str(_) for _ in r]))
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
            return datetime.datetime.strptime(expr, '%Y-%m-%d')
        elif re.match(r'^\d{4}\-\d{1,2}\-\d{1,2} \d{1,2}\:\d{2}\:d{2}$', expr):
            return datetime.datetime.strptime(expr, '%Y-%m-%d %H:%M:%S')
        elif expr.startswith('$') and ':' in expr:
            op, oa = expr.split(':', 1)
            oa = self.expand_literals(oa)
            if op == '$id' and isinstance(oa, str) and OBJECTID_PATTERN.match(oa):
                return ObjectId(oa)
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
        elif isinstance(dt_or_span, str) and re.match(r'^\-?(\d+)([ymd])$', dt_or_span):
            offset = int(dt_or_span[:-1])
            unit = dt_or_span[-1]
            offset *= 86400
            if unit == 'm':
                offset *= 31
            elif unit == 'y':
                offset *= 365
            return int(time.time() + offset)
        return 0

    def expand_query(self, token, op, opa):

        self.logger(token, op, opa)
            
        if isinstance(opa, list) and len(opa) == 1:
            opa = opa[0]
        
        if self.force_timestamp and isinstance(opa, datetime.datetime):
            opa = opa.timestamp()

        if op in self.operators:
            opa = {self.operators[op]: opa}
            if self.operators[op] == '$regex':
                opa['$options'] = '-i'

        elif op == '__fn__':
            token = f'${token}'
            op = '='
        
        if isinstance(token, str):
            if token == 'id' or token.endswith('.id'):
                token = token[:-2] + '_id'
            if (token == '_id' or token.endswith('._id')) and isinstance(opa, str) and OBJECTID_PATTERN.match(opa):
                opa = ObjectId(opa)

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

        if len(v) == 1 and '$_json' in v:
            return json.loads(v['$_json'])

        return v

    def split_field_ops(self, token):
        for op in sorted(self.priorities, key=lambda x: len(x), reverse=True):
            if op in token:
                qfield, opa = token.split(op, 1)
                if not qfield: qfield = self.default_field
                return qfield, op, opa
        else:
            return self.default_field, self.default_op, token

    def force_operand(self, v):
        if isinstance(v, str):
            return MongoOperand(self.expand_query(self.default_field, self.default_op, v))
        elif isinstance(v, MongoOperand):
            return v
        else:
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

        self.logger(' '.join([type(_).__name__ + '/' + str(_) for _ in post]))

        opers = []
        for token in post:
            if not isinstance(token, _Operator):
                opers.append(token)
                continue
            if token in '&,':
                a, b = self.force_operand(opers.pop()), self.force_operand(opers.pop())
                opers.append(b & a)
            elif token == '|':
                a, b = self.force_operand(opers.pop()), self.force_operand(opers.pop())
                opers.append(b | a)
            elif token == '=>':
                a, b = opers.pop(), opers.pop()
                if isinstance(b, MongoOperand): b = b()
                if isinstance(b, list): v = b
                else: v = [b]
                v.append(a)
                opers.append(MongoOperand(v))
            elif token == '~':
                opers.append(~self.force_operand(opers.pop()))
            elif token == '.':
                a, b = opers.pop(), opers.pop()
                opers.append(self.expand_literals(f'{b}.{a}'))
            elif token in self.priorities:
                opa = opers.pop()
                qfield = self.default_field if isinstance(token, _DefaultOperator) else opers.pop()
                if token == '__fn__':
                    if isinstance(qfield, MongoOperand):
                        v, *_ = qfield._literal.values()
                        v.update(**opa())
                        opers.append(qfield)
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

        return opers[0] if opers else None

    def eval(self, expr):
        v = self.eval_tokens(self.tokenize_expr(expr))
        if v is None: return {}
        if isinstance(v, dict): return v
        if not isinstance(v, MongoOperand): v = self.force_operand(v)
        return v()
