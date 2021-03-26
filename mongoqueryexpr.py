from .mongobase import *
from .mongofield import *
from bson import ObjectId
import json
import re
F = MongoOperandFactory(MongoField)


class QueryExprParser:
    def __init__(self, default_field, default_query_field, abbrev_prefixes, shortcuts, priorities={
        '~': 10,
        '&': 9,
        '|': 8
    }):
        self.default_field = default_field
        self.default_query_field = default_query_field
        self.abbrev_prefixes = abbrev_prefixes
        self.shortcuts = shortcuts
        self.priorities = priorities

    def tokenize_expr(self, expr):
        l = []
        w = ''
        i = 0
        len_expr = len(expr)
        quoted = False
        while i < len_expr:
            c = expr[i]
            if c == '`':
                quoted = not quoted
            elif not quoted and (c in ',()' or c in self.priorities):
                if w:
                    l.append(w)
                w = ''
                if c == ',':
                    c = '&'
                l.append(c)
            else:
                w += c
            i += 1
        if w:
            l.append(w)
        return l

    def expand_literals(self, expr):
        if re.match(r'^[\+\-]?\d+(\.\d+)?$', expr):
            return float(expr) if '.' in expr else int(expr)
        elif expr.lower() in ['true', 'false']:
            return expr.lower() == 'true'
        elif expr.lower() in ['none', 'null']:
            return None
        elif (expr.startswith("{") and expr.endswith("}")) or (expr.startswith('[') and expr.endswith(']')):
            return json.loads(expr)
        elif expr.startswith('$'):
            op, oa = expr.split(':', 1)
            oa = self.expand_literals(oa)
            if op == '$id':
                return ObjectId(oa)
            return (op, oa)
        return expr

    def expand_query(self, token, op, opa):
        if isinstance(opa, list):
            opa = opa[0]
        opa = self.expand_literals(opa)
        if token.endswith('_at'):
            opa = self.parse_dt_span(opa)
        if op == '>':
            opa = {'$gt': opa}
        elif op == '<':
            opa = {'$lt': opa}
        elif op == '>=':
            opa = {'$gte': opa}
        elif op == '<=':
            opa = {'$lte': opa}
        elif op == '%':
            opa = {'$regex': opa}
        elif op == '!=':
            opa = {'$ne': opa}

        for pref, lookuped in self.abbrev_prefixes.items():
            if token.startswith(pref):
                token = lookuped + token[1:]
                break

        if token == 'id' or token.endswith('.id'):
            token = token[:-2] + '_id'
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

        return v

    def stacking_tokens(self, tokens):
        post = []
        stack = []
        for t in tokens:
            if t not in '()' and t not in self.priorities:
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
        return post

    def eval_tokens(self, tokens):
        tokens = self.stacking_tokens(tokens)
        opers = []
        i = 0
        len_tokens = len(tokens)
        while i < len_tokens:
            token = tokens[i]
            if token == '&':
                opers.append(opers.pop() & opers.pop())
            elif token == '|':
                opers.append(opers.pop() | opers.pop())
            elif token == '~':
                opers.append(~opers.pop())
            elif token.startswith('?'):
                for op in sorted(['>', '>=', '<', '<=', '=', '!=', '%'], key=lambda x: len(x), reverse=True):
                    if op in token:
                        qfield, opa = token.split(op, 1)
                        opers.append(MongoOperand(
                            self.expand_query(qfield[1:], op, opa)))
                        break
                else:
                    opers.append(MongoOperand(
                        {self.default_query_field: {'$regex': token[1:], "$options": "-i"}}))
            else:
                if self.default_field == '$text':
                    f_search = F['$text'].search
                    f_eq = f_search
                else:
                    f_search = F[self.default_field].regex
                    f_eq = F[self.default_field].eq
                if '%' in token:
                    v = f_search(token.replace('%', '.*'))
                elif token.startswith(':'):
                    v = self.shortcuts.get(token[1:], f_eq(token))
                else:
                    v = f_eq(token)
                opers.append(v)
            i += 1
        return opers[0] if opers else None

    def match_query(self, expr):
        v = self.eval_tokens(self.tokenize_expr(expr))
        return v() if v else None
