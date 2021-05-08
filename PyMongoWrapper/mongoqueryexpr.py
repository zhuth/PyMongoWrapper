from .mongobase import *
from .mongofield import *
from bson import ObjectId
import datetime, time
import json
import re


F = MongoOperandFactory(MongoField)
OBJECTID_PATTERN = re.compile(r'^[0-9A-Fa-f]{24}$')
SPACING_PATTERN = re.compile(r'\s')


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

        self.allow_spacing = allow_spacing

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
                    return lookup + [self.expand_literals(w[len(pref):])]
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

        for c in expr:
            # dealing quotes
            if c == '`':
                quoted = not quoted
                if not quoted:
                    l.append(w)
                    w = ''
                continue
            if quoted:
                w += c
                continue
            if self.allow_spacing and SPACING_PATTERN.match(c):
                continue

            # hereafter, not quoted

            # single parentheses
            if c in '()':
                l += _w(w)
                if c == '(' and w and w not in self.priorities and w != '(':
                    l.append('__fn__')
                w = ''
                l.append(c)
                continue

            # dealing with multi-character operators
            if not w and l:
                cl, op = _test_op(l[-1], c)
                if op:
                    if cl:
                        l[-1] = l[-1][:-cl]
                        if l[-1] == '': l = l[:-1]
                    l.append(op)
                    continue
            elif w:
                cl, op = _test_op(w, c)
                if op:
                    if cl:
                        w = w[:-cl]
                    l += _w(w)
                    w = ''
                    l.append(op)
                    continue
            elif c in self.priorities:
                l.append(c)
                continue

            w += c
        
        self.logger(l[:-1])
        return l[:-1]

    def expand_literals(self, expr):
        if re.match(r'^[\+\-]?\d+(\.\d+)?$', expr):
            return float(expr) if '.' in expr else int(expr)
        elif expr.lower() in ['true', 'false']:
            return expr.lower() == 'true'
        elif expr.lower() in ['none', 'null']:
            return None
        elif re.match(r'^\d{4}\-\d{1,2}\-\d{1,2}$', expr):
            return datetime.datetime.strptime(expr, '%Y-%m-%d')
        elif re.match(r'^\d{4}\-\d{1,2}\-\d{1,2} \d{1,2}\:\d{2}\:d{2}$', expr):
            return datetime.datetime.strptime(expr, '%Y-%m-%d %H:%M:%S')
        elif expr.startswith('$') and ':' in expr:
            op, oa = expr.split(':', 1)
            oa = self.expand_literals(oa)
            if op == '$id' and isinstance(opa, str) and OBJECTID_PATTERN.match(opa):
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
        last_token = ''
        for t in tokens:
            if not isinstance(t, str) or (t not in '()' and t not in self.priorities):
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
            last_token = t
        
        while stack:
            post.append(stack.pop())

        self.logger(post)

        opers = []
        for token in post:
            if not isinstance(token, str):
                opers.append(token)
                continue
            if token == '&' or token == ',':
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
                qfield = opers.pop()
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
