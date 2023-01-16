import re
import dateutil.parser
import datetime
from typing import Any, List, Tuple, Union, Iterable


OBJECTID_PATTERN = re.compile(r'^[0-9A-Fa-f]{24}$')
SPACING_PATTERN = re.compile(r'\s')


class EStr:
    """String with self.line, self.col, and extra (bundle) info"""

    def __init__(self, literal, line=0, col=0, bundle=None) -> None:
        self.literal = str(literal)
        if line == 0 and col == 0 and isinstance(literal, EStr):
            self.line, self.col = literal.line, literal.col
        self.line, self.col = line, col
        self.bundle = bundle

    def __repr__(self) -> str:
        return f'{self.literal}/{type(self).__name__}(@{self.line}:{self.col})'

    def __str__(self) -> str:
        return self.literal

    def __add__(self, another):
        if not isinstance(another, EStr):
            another = EStr(another, 1 << 31, 1 << 31)
        return EStr(self.literal + another.literal,
                    min(self.line, another.line), min(self.col, another.col))

    def __getitem__(self, key):
        return EStr(self.literal[key], self.line, self.col)

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


class ELiteral(EStr):
    """Representing a literal string"""

    def __repr__(self) -> str:
        return f'{repr(self.literal)}/{type(self).__name__}(@{self.line}:{self.col})'


class EOperator(EStr):
    """Representing an operator"""


class EDefaultOperator(EOperator):
    """Representing an operator with default field name"""


class EList:
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
        if not isinstance(token, EStr):
            token = EStr(token, 0, 0)
        self.token = token

    def __str__(self) -> str:
        """Print out position info off the token

        Returns:
            str: _description_
        """
        return f'{type(self).__name__}: {repr(self.token)}'


class QueryExprTokenizer:
    """Query expression tokenizer"""

    operators = {
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
        '__calc__': 50,
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

    arithmetic_operators = {
        '+': '$add',
        '-': '$substract',
        '*': '$multiply',
        '/': '$divide'
    }

    arithmetic_priorities = {
        EStr('+', 0, 0): 3,
        EStr('-', 0, 0): 3,
        EStr('*', 0, 0): 4,
        EStr('/', 0, 0): 4
    }

    def __init__(self, arithmetic: bool = False,
                 allow_spacing: bool = True,
                 force_timestamp: bool = False,
                 priorities: dict = None,
                 abbrevs: dict = None,
                 default_field: str = '',
                 default_op: str = '',
                 shortcuts: dict = None,
                 logger=print) -> None:

        self.arithmetic = arithmetic

        for operator in self.operators:
            self.priorities[operator] = 20
        self.priorities = {EStr(k, 0, 0): v for k,
                           v in self.priorities.items()}

        self.max_operator_len = max(
            map(lambda x: len(x) if not x.startswith('__') else 0, self.priorities))

        self.shortcuts = {} or shortcuts
        self.default_field = '$text'
        self.default_op = '%%'

        self.abbrevs = abbrevs

        self.allow_spacing = allow_spacing
        self.force_timestamp = force_timestamp
        self.default_field = default_field
        self.default_op = default_op

        self.logger = logger

        self._col = 0
        self._line = 1

        self._word = ''
        self._tokens = []

    def finish(self):
        if not self._word:
            return

        for pref, lookup in self.abbrevs:
            if self._word.startswith(pref):
                ret = list(lookup)
                ret += [self.literal(self._word[len(pref):])
                        ] if self._word != pref else []
                self._tokens += ret
                self._word = ''
                return

        if self._word.startswith(':') and self._word[1:] in self.shortcuts:
            self._tokens += self.shortcuts[self._word[1:]]

        elif self._word == 'calc':
            self.arithmetic = True
            self._tokens += ['calc']

        else:
            self._tokens += [self.literal()] if self._word else []

        last_word = self._word
        self._word = ''
        return last_word

    def append(self, cls, token=None):
        if cls is None:
            assert token is not None
            self._tokens.append(token)
        else:
            self._tokens.append(
                cls(token or self._word, self._line, self._col))

    def peek(self, n=1):
        if len(self._tokens) >= n:
            return self._tokens[-n]

    def literal(self, expr=None):
        if expr is None:
            expr = self._word

        if re.match(r'^[\+\-]?\d+(\.\d+)?$', expr):
            return float(expr) if '.' in expr else int(expr)
        elif re.match(r'^[\+\-]?\d+\.?\d*[eE][\+\-]?\d+$', expr):
            return float(expr)
        elif expr.lower() in ['true', 'false']:
            return expr.lower() == 'true'
        elif expr.lower() in ['none', 'null']:
            return None
        elif re.match(r'^[\+\-]?(\d+)[ymdHMS]$', expr):
            offset = int(expr[:-1])
            offset *= {'y': 365, 'm': 30}.get(expr[-1], 1)
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

    def is_op(self, token):
        return token in self.operators or (self.arithmetic and token in self.arithmetic_operators)

    def is_priored(self, token):
        return token in self.priorities or (self.arithmetic and token in self.arithmetic_priorities)

    def test_op(self, last, char):
        for last_char in range(self.max_operator_len-1, 0, -1):
            if self.is_priored(EOperator(last[-last_char:] + char)):
                char = EOperator(last[-last_char:] + char)
                return last_char, char
        if self.is_priored(EOperator(char)):
            return 0, char
        return -1, ''

    def tokenize(self, expr):
        if not expr:
            return []

        expr += '\n~'
        quoted = ''
        initial_arithmetic = self.arithmetic

        brackets = []

        escaped = False
        commented = False

        for char in expr:
            # skip comments
            self._col += 1

            if char == '\n':
                self._line += 1
                self._col = 1

            if char == '\n' and commented:
                commented = False
                continue

            if not quoted and char == '/' and self._word.endswith('/'):
                self._word = self._word[:-1]
                if self._word:
                    self.finish()
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
                    self._word += {
                        'n': '\n',
                        'b': '\b',
                        't': '\t',
                        'f': '\f',
                        'r': '\r',
                    }.get(char, char)
                    escaped = False
                continue

            elif isinstance(escaped, (EStr, str)):
                if escaped.startswith('u'):
                    escaped += char
                    if len(escaped) == 5:
                        self._word += chr(int(escaped[1:], 16))
                        escaped = False
                elif escaped.startswith('x'):
                    escaped += char
                    if len(escaped) == 3:
                        self._word += chr(int(escaped[1:], 16))
                        escaped = False
                continue

            if char in '`\'"':
                if quoted:
                    if quoted == char:
                        quoted = ''
                        self.append(ELiteral)
                        self._word = ''
                        continue
                else:
                    self.finish()
                    quoted = char
                    continue
            if quoted:
                self._word += char
                continue

            # hereafter, not quoted
            if self.allow_spacing and SPACING_PATTERN.match(char):
                continue

            # single parentheses
            if char in '()':
                last_word = self.finish()
                if char == '(' and ((last_word and not self.is_priored(last_word) and last_word != '(')
                                    or (not last_word and self.peek() == ')')):
                    self.append(EOperator, '__fn__')
                elif char == ')' and len(self._tokens) > 0 and self._tokens[-1] == '(':
                    self.append(None, {})

                self.append(EOperator, char)

                if char == '(':
                    if len(self._tokens) > 2 and self._tokens[-2] == '__fn__':
                        brackets.append(self._tokens[-3])
                    else:
                        brackets.append(char)
                elif brackets:
                    print(brackets)
                    popped = brackets.pop()
                    if popped == 'calc':
                        self.arithmetic = initial_arithmetic
                else:
                    raise QueryExpressionError(
                        EStr(char, self._line, self._col))

                continue

            # list
            if char in '[]':
                last_word = self.finish()
                if char == '[':
                    if (last_word and last_word not in self.priorities and last_word != '[') \
                            or (not last_word and self.peek() == ']'):
                        self.append(EOperator, '__fn__')
                    self.append(EOperator, '(')
                    self.append(EOperator, '__list__')
                    self.append(EOperator, '[')
                else:
                    if self._tokens and self._tokens[-1] == '[':
                        self.append(None, [])
                    self.append(EOperator, ']')
                    self.append(EOperator, ')')

                self._word = ''
                continue

            # dealing with multi-character operators
            if not self._word and self._tokens and isinstance(self._tokens[-1], EOperator):
                flag, operator = self.test_op(self._tokens[-1], char)
                if operator:
                    if flag:
                        self._tokens[-1] = self._tokens[-1][:-flag]
                        if self._tokens[-1] == '':
                            self._tokens = self._tokens[:-1]
                    self.append(EOperator, operator)
                    continue
            elif self._word:
                flag, operator = self.test_op(self._word, char)
                if operator:
                    if flag:
                        self._word = self._word[:-flag]
                    self.finish()
                    self.append(EOperator, operator)
                    continue
            elif char in self.priorities:
                self.append(EOperator, char)
                continue

            self._word += char

        if brackets:
            raise QueryExpressionError(
                EStr('Missing )?', self._line, self._col))

        return self.backward()

    def backward(self):
        stack = []
        result = []
        last_t = EOperator
        for token in self._tokens[:-1]:
            token_type = type(token)
            if token == ',' and stack and stack[-1] == '[':
                token = EOperator('__sep__', self._line,
                                  self._col, bundle=stack[-1])
            elif token_type is EOperator and self.is_op(token) and last_t is EOperator \
                    and (not stack or stack[-1] != '['):
                token = EDefaultOperator(token)
            if token == '(':
                stack.append(token)
            elif token == '[':
                stack.append(token)
            elif token == ')' and stack and stack[-1] == '(':
                stack.pop()
            elif token == ']' and stack and stack[-1] == '[':
                stack.pop()
            result.append(token)
            last_t = token_type if token not in ('(', ')') else EStr

        self.logger(' '.join([repr(_) for _ in result]))
        return result
