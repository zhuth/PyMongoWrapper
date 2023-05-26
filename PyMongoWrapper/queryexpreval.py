"""Query Expression Evaluator"""

import random
from typing import Union, List, Dict, Callable
from functools import wraps
import re
import math
from decimal import Decimal
import datetime
import dateutil.parser
from bson import ObjectId


RE_DIGITS = re.compile(r'^[+\-]?\d+$')
UNITS = 'year quarter week month day hour minute second millisecond'.split()


class FCBreak:
    """Represent a `break` in loops"""
    pass


class FCReturn(Exception):
    """Represent a return value"""

    def __init__(self, retval, *args: object) -> None:
        self.retval = retval
        super().__init__(*args)


class FCHalt(Exception):
    """
    Represent a programmed halt.
    Unlike FCReturn, this exception should be handled by the caller, 
    not inside QueryExprEvaluator.
    """
    pass


class QueryExprEvaluator:
    """Evaluate Query Expression
    """

    def __init__(self, user_defined=None):
        """Initialize Query Expression Evaluator

        Args:
            implementations (dict, optional): Implementations of functions. Defaults to None.
        """
        self.context = {}

        self._defined = user_defined or {}
        self._impl = {}
        _default_impls(self)

    def _operator(self, operator_name):
        """Get operator name for comparison"""
        operator_name = operator_name.lstrip('$')
        operator = {
            'lte': 'le',
            'gte': 'ge',
            '': 'eq'
        }.get(operator_name, operator_name)
        return f'__{operator}__'

    def _compare(self, operator, *args):
        """Compare between arguments"""
        operator = self._operator(operator)
        if len(args) == 2:
            op_a, op_b = args
            if op_a is None:
                if operator == '__eq__':
                    return op_b is None
                return False
            return self._getfunc(op_a, operator)(op_b)

    def _getattr(self, obj, key, default=None):
        """Get attribute of an object"""
        if key.startswith('$'):
            key = key[1:]

        if key in ('$$ROOT', '$ROOT'):
            return obj

        if obj is None:
            return obj

        if '.' in key:
            for key_seg in key.split('.'):
                obj = self._getattr(obj, key_seg, default)
            return obj

        if isinstance(obj, dict):
            return obj.get(key, default)

        if isinstance(obj, list) and RE_DIGITS.match(key):
            return obj[int(key)] if 0 <= int(key) < len(obj) else default

        return getattr(obj, key, default)

    def _test_inputs(self, obj, val, relation='eq'):
        """
        Perform basic comparison between field and given value
        """
        options = None

        if relation == 'eq' and isinstance(val, dict) and tuple(val.keys())[0].startswith('$'):
            options = val.pop('$options', None)
            relation, = val.keys()
            val = val[relation]
            relation = relation[1:]

        oprname = self._operator(relation)

        if oprname == '__in__':
            return obj in val

        if oprname == '__size__':
            return len(obj) == val

        if oprname == '__regex__':
            if not isinstance(obj, list):
                obj = [obj]
            if isinstance(obj, dict):
                options = val['$options']
                val = val['$regex']
            elif options is None:
                options = 'i'

            options = [getattr(re, op.upper()) for op in options]
            flags = 0
            if options:
                flags = options[0]
                for op in options[1:]:
                    flags |= op

            for ostr in obj:
                return re.search(val, ostr, flags=flags) is not None

        if isinstance(obj, list) and not isinstance(val, list):
            arr_result = False
            for input_val in obj:
                arr_result = arr_result or self._getfunc(
                    input_val, oprname)(val)
                if arr_result:
                    break
        else:
            arr_result = self._getfunc(obj, oprname)(val)

        return arr_result

    def _getfunc(self, obj: Union[object, Dict], func_name: str) -> Callable:
        """Get function from object

        Args:
            obj (Union[object, Dict]): context
            func_name (str): function name

        Returns:
            Callable: function
        """
        func = self._getattr(obj, func_name)
        if func:
            return func
        elif func_name.strip('_') in self._impl:
            return lambda *args: self._impl[func_name.strip('_')](obj, *args)
        else:
            return lambda *_: None

    def function(self, name: str = '', mapping: Dict = None, lazy=False, context=False, bundle=None):
        """Register function

        Args:
            mapping (Dict, optional): A dict in the form of
                {arg_name: programmatic_arg_name} Defaults to None.
            lazy(bool, optional): Use `value` property to evaluate
        """

        if mapping is None:
            mapping = {}

        mapping.update({
            'input': 'input_',
            'as': 'as_',
            'from': 'from_',
            'in': 'in_',
            'to': 'to_',
        })

        class _Lazy:
            """A Lazy Evaluating Unit"""

            def __init__(this, parsed: Dict, obj: Dict):
                this.obj = obj
                this.parsed = parsed

            @property
            def value(this):
                """Get value"""
                return self.evaluate(this.parsed, this.obj)

        def _camelize(name):
            return re.sub(r'_(\w)', lambda x: x.group(1).upper(), name.strip('_'))

        def _snakize(name):
            return re.sub(r'[A-Z]', lambda x: f'_{x.group(0).lower()}', name)

        def _do(func):
            @wraps(func)
            def _wrapped(obj, param):

                def _eval(ele):
                    if lazy:
                        return _Lazy(ele, obj)
                    return self.evaluate(ele, obj)

                args, kwargs = [], {}
                if isinstance(param, (tuple, list)):
                    args = list(map(_eval, param))
                elif isinstance(param, dict):
                    if not [1 for key in param if key.startswith('$')]:
                        kwargs = {
                            mapping.get(key, _snakize(key)): _eval(val)
                            for key, val in param.items()
                        }
                    else:
                        args = [_eval(param)]
                else:
                    args = [_eval(param)]
                if context:
                    kwargs['context'] = obj
                if bundle:
                    kwargs['bundle'] = bundle

                return func(*args, **kwargs)

            func_name = name if name else _camelize(func.__name__)
            self._impl[func_name] = _wrapped
            return func

        return _do

    @property
    def implemented_functions(self):
        """
        Get names of implemented functions
        """
        return self._impl.keys()

    def execute(self, stmts: List, obj: dict):
        """
        Execute given statements and get returned value (if any)
        """
        try:
            self._execute(stmts, obj)
        except FCReturn as ret:
            return ret.retval

    def _execute(self, stmts: List, obj: dict):
        """
        Perform actual execution, will raise FCReturn exception when encountering a `return` statement
        """
        
        for stmt in stmts:
            if isinstance(stmt, dict) and len(stmt) == 1:
                (key, val), = stmt.items()
                assert key.startswith(
                    '$'), f'Unknown format as a statement: {stmt}'
                if key.startswith('$_FC'):
                    if key == '$_FCReturn':  # return
                        raise FCReturn(self.evaluate(val, obj))

                    elif key == '$_FCRepeat':
                        while self.evaluate(val['cond'], obj):
                            result = self._execute(val['pipeline'], obj)
                            if isinstance(result, FCBreak):
                                break  # exit while

                    elif key == '$_FCForEach':
                        for item in self.evaluate(val['input'], obj):
                            obj['$' + val['as']] = item
                            result = self._execute(val['pipeline'], obj)
                            if isinstance(result, FCBreak):
                                break  # exit for each
                        obj.pop('$' + val['as'], None)

                    elif key == '$_FCBreak':  # break
                        return FCBreak()

                    elif key == '$_FCHalt':  # halt, raise error
                        raise FCHalt()

                    elif key == '$_FCContinue':  # continue
                        break  # skip following statements in current pipeline

                    elif key == '$_FCConditional':  # if
                        cond = self.evaluate(val['cond'], obj)
                        if cond:
                            self._execute(val['if_true'], obj)
                        else:
                            self._execute(val['if_false'], obj)

                elif key[1:] in self._impl:
                    self._impl[key[1:]](obj, val)

                else:
                    self.evaluate(stmt, obj)
            else:
                raise FCReturn(self.evaluate(stmt, obj))

    def evaluate(self, parsed, obj: dict):
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
                if key in ('$gt', '$gte', '$eq', '$lt', '$lte', '$ne'):
                    temp = self._compare(
                        key, *[self.evaluate(ele, obj) for ele in val])
                elif key == '$expr':
                    temp = self.evaluate(val, obj)
                elif key == '$':
                    temp = self._getattr(obj, val)
                elif key[1:] in self._impl:
                    temp = self._impl[key[1:]](obj, val)
                elif key.endswith('@'):  # call user defined function when execution
                    args = self.evaluate(val, obj)
                    temp = self.execute(self._defined.get(
                        key[1:-1], []), {'arg': args, 'ctx': self.context})
                else:
                    temp = self._test_inputs(obj, val, key[1:])

                result = _append_result(temp)
            else:
                result = _append_result(self._test_inputs(
                    self._getattr(obj, key), val if isinstance(val, dict) else val))

            if result is False:
                return result

        return result


def _default_impls(inst: QueryExprEvaluator):

    def _check_type(objs, types):
        if not isinstance(objs, (tuple, list)):
            objs = (objs,)
        if not isinstance(types, tuple):
            types = (types,)
        for obj in objs:
            if not isinstance(obj, types):
                types_str = '/'.join([_.__name__ for _ in types])
                raise TypeError(
                    f'must be {types_str}, got {type(obj).__name__}: {obj}')

    def _check_unit(unit):
        if unit not in UNITS:
            raise ValueError('unit must be one of the following: ' + UNITS)

    def _convert_date(val):
        if isinstance(val, datetime.datetime):
            return val

        if isinstance(val, ObjectId):
            return val.generation_time

        if isinstance(val, (int, float)):
            if val > 1e10:
                val /= 1000
            return datetime.datetime.fromtimestamp(val)

        try:
            return dateutil.parser.parse(str(val))
        except ValueError:
            return None

    def _arg_if_list(ops):
        if isinstance(ops, tuple) and len(ops) == 1 and isinstance(ops[0], list):
            ops = ops[0]
        return ops

    # ARRAY OPERATIONS

    @inst.function()
    def size(input_):
        return len(input_)

    @inst.function()
    def first(input_):
        for i in input_:
            return i

    @inst.function()
    def first_n(input_, n):
        return input_[:n]

    @inst.function()
    def last(input_):
        i = None
        for i in input_:
            pass
        return i

    @inst.function()
    def last_n(input_, n):
        return input_[-n:]

    @inst.function()
    def index_of_array(arr, search, start=0, end=-1):
        _check_type(arr, list)
        if end < start:
            end = len(arr)
        try:
            return arr[start:end+1].index(search) + start
        except ValueError:
            return -1

    @inst.function(context=True, lazy=True)
    def map_(input_, in_, context, as_='this'):
        as_ = getattr(as_, 'parsed', as_)
        _check_type(as_, str)
        as_ = '$' + as_
        result = []
        context[as_] = None
        for ele in input_.value:
            context[as_] = ele
            result.append(inst.evaluate(in_.parsed, context))
        del context[as_]
        return result

    @inst.function(context=True, lazy=True)
    def filter_(input_, cond, context, as_='this'):
        as_ = getattr(as_, 'parsed', as_)
        _check_type(as_, str)
        as_ = '$' + as_
        result = []
        context[as_] = None
        for ele in input_.value:
            context[as_] = ele
            if inst.evaluate(cond.parsed, context):
                result.append(ele)
        return result

    @inst.function(context=True, lazy=True)
    def reduce_(input_, in_, context, initial_value, as_='this'):
        as_ = getattr(as_, 'parsed', as_)
        _check_type(as_, str)
        as_ = '$' + as_
        result = []
        context[as_] = None
        context['$value'] = initial_value.parsed
        for ele in input_.value:
            context[as_] = ele
            context['$value'] = inst.evaluate(in_.parsed, context)

        result = context['$value']
        del context[as_]
        del context['$value']
        return result

    @inst.function()
    def reverse_array(input_):
        return reversed(input_)

    @inst.function(lazy=True)
    def sort_array(input_, sort_by, reverse=False):
        sort_by = getattr(sort_by, 'parsed', sort_by)
        sort_by = list(sort_by.items())

        class _sorting:

            def __init__(self, val):
                self.value = [(val[field] if field else val, ordering)
                              for field, ordering in sort_by]

            def __lt__(self, another):
                for (a, ordering), (b, _) in zip(self.value, another.value):
                    if a != b:
                        return a < b if ordering > 0 else a > b
                return False

        input_ = sorted(input_.value, key=_sorting, reverse=reverse)
        return input_

    @inst.function(lazy=True)
    def top_n(input_, n, sort_by, output):
        input_ = sort_array(input_, sort_by, reverse=True)[:n.value]
        return [inst.evaluate(output.parsed, inp) for inp in input_]

    @inst.function(lazy=True)
    def top(input_, sort_by, output):
        return top_n(input_, 1, sort_by, output)[0]

    @inst.function(lazy=True)
    def min_n(input_, n, sort_by={'': 1}):
        return sort_array(input_, sort_by)[:n.value]

    @inst.function(lazy=True)
    def max_n(input_, n, sort_by={'': 1}):
        return sort_array(input_, sort_by, reverse=True)[:n.value]

    @inst.function()
    def set_union(*ops):
        ops = _arg_if_list(ops)
        result = set()
        for op in ops:
            result.update(op)
        return result

    @inst.function()
    def set_is_subset(opa: set, opb: set):
        opa, opb = set(opa), set(opb)
        return opb.issubset(opa)

    @inst.function()
    def set_is_superset(opa: set, opb: set):
        opa, opb = set(opa), set(opb)
        return opb.issuperset(opa)

    @inst.function()
    def set_intersection(*ops):
        ops = _arg_if_list(ops)
        assert len(ops) > 0
        op0 = set(ops[0])
        return op0.intersection(*ops[1:])

    @inst.function()
    def set_equals(*ops):
        ops = _arg_if_list(ops)
        assert len(ops) > 0
        op0 = set(ops[0])
        for op in ops[1:]:
            if set(op) != op0:
                return False
        return True

    @inst.function()
    def set_difference(opa, opb):
        opa, opb = set(opa), set(opb)
        return opa.difference(opb)

    # CONDITIONAL

    @inst.function(lazy=True)
    def if_null(*args):
        evaluated = None
        for cond in args[:-1]:
            evaluated = cond.value
            if evaluated is None:
                return args[-1].value
        return evaluated

    @inst.function(mapping={'if': 'cond', 'then': 'if_then', 'else': 'if_else'}, lazy=True)
    def cond(cond, if_then, if_else=None):
        if cond.value:
            return if_then.value
        elif if_else is not None:
            return if_else.value

    @inst.function()
    def concat_arrays(*ops: List[List]):
        ops = _arg_if_list(ops)
        _check_type(ops, list)
        result = []
        for ele in ops:
            result += ele
        return result

    @inst.function()
    def zip_(inputs, use_longest_length=False, defaults=[]):
        if use_longest_length:
            length = max(map(len, inputs))
            for inp, default in zip(inputs, defaults):
                if len(inp) < length:
                    for _ in range(length - len(inp)):
                        inp.append(default)
        return list(zip(inputs))

    # MATH

    for math_name in dir(math):
        if '_' in math_name:
            continue

        @inst.function(name=math_name, bundle=math_name)
        def _math(number, bundle):
            _check_type(number, (int, float))
            return getattr(math, bundle)(number)

    @inst.function()
    def add(*ops):
        ops = _arg_if_list(ops)
        _check_type(ops, (int, float))
        return sum(ops)

    @inst.function()
    def subtract(opa, opb):
        _check_type((opa, opb), (int, float))
        return opa - opb

    @inst.function()
    def mod(opa, opb):
        _check_type((opa, opb), (int,))
        return opa % opb

    @inst.function()
    def multiply(*ops: Union[int, float]):
        ops = _arg_if_list(ops)
        _check_type(ops, (int, float))
        result = 1
        for ele in ops:
            result *= ele
        return result

    @inst.function()
    def divide(opa: Union[int, float], opb: Union[int, float]):
        _check_type((opa, opb), (int, float))
        return opa/opb

    @inst.function()
    def rand():
        return random.random()

    @inst.function()
    def sample_rate(rate):
        return random.random() < rate

    @inst.function()
    def range(start, end, step=1):
        assert step != 0
        return list(range(start, end, step))

    @inst.function()
    def avg(*ops):
        ops = _arg_if_list(ops)
        _check_type(ops, (int, float))
        return sum(ops) / len(ops)

    @inst.function()
    def max_(*ops):
        ops = _arg_if_list(ops)
        return max(ops)

    @inst.function()
    def min_(*ops):
        ops = _arg_if_list(ops)
        return min(ops)

    @inst.function()
    def trunc_(number, place=0):
        _check_type(number, (int, float))
        _check_type(place, int)
        return math.trunc(number * (10 ** place)) / (10 ** place)

    @inst.function()
    def radians_to_degrees(number):
        _check_type(number, (int, float))
        return number * 180 / math.pi

    # TYPES & CONVERSIONS

    @inst.function(name='NumberLong')
    def number_long(val):
        return int(val)

    @inst.function()
    def type_(val):
        type_str = {
            'float': 'double',
            'str': 'string',
            'list': 'array',
            'bytes': 'binData',
            'NoneType': 'Null',
            'bool': 'bool',
            'datetime': 'date',
            'date': 'date',
        }.get(type(val).__name__, '')

        if not type_str:
            if isinstance(val, int):
                if abs(val) < (1 << 32):
                    return 'int'
                else:
                    return 'long'

            if isinstance(val, dict) and (
                (len(val) in (1, 2) and '$regex' in val) and
                ('$options' in val or len(val) == 1)
            ):
                return 'regex'
            return 'object'

    @inst.function()
    def is_array(val):
        _check_type(val, list)
        if len(val) != 1:
            raise ValueError('argument must have and only have one element')
        val, = val
        return isinstance(val, list)

    @inst.function()
    def is_number(val):
        return isinstance(val, (float, int))

    @inst.function()
    def convert(input_: Union[int, str], to_: Union[int, str]):
        _check_type(to_, (int, str))
        if to_ in (1, 'double'):
            return float(input_)
        elif to_ in (19, 'decimal'):
            return Decimal(input_)
        elif to_ in (2, 'string'):
            return str(input_)
        elif to_ in (7, 'objectId'):
            return ObjectId(input_)
        elif to_ in (8, 'bool'):
            return not not input_
        elif to_ in (9, 'date'):
            return _convert_date(input_)
        else:
            return int(input_)

    for type_name in ('string', 'int', 'long', 'bool', 'date', 'double', 'decimal', 'objectId'):
        @inst.function(name=f'to{type_name.capitalize()}', bundle=type_name)
        def _to_type(val, bundle):
            return convert(val, bundle)

    # DATE FUNCTIONS

    @inst.function()
    def date_add(start_date, unit, amount, timezone):
        _check_type(start_date, datetime.datetime)
        _check_type(amount, (float, int))
        _check_unit(unit)
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
        if timezone:
            raise NotImplementedError()
        return start_date + delta

    @inst.function()
    def date_diff(start_date, end_date, unit):
        _check_type((start_date, end_date), datetime.datetime)
        _check_unit(unit)
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
        }.get(unit)
        return (end_date - start_date).total_seconds() / unit

    for date_part in ('year', 'month', 'day', 'hour', 'minute', 'second'):
        @inst.function(name=date_part, bundle=date_part)
        def _date_part(date, bundle):
            date = _convert_date(date)
            return getattr(date, bundle)

    @inst.function()
    def week(date: datetime.datetime):
        date = _convert_date(date)
        return date.isocalendar().week

    @inst.function()
    def iso_week(date):
        return week(date)

    @inst.function()
    def iso_week_year(date):
        return week(date)

    @inst.function()
    def day_of_week(date: datetime.datetime):
        date = _convert_date(date)
        return date.weekday

    @inst.function()
    def day_of_year(date: datetime.datetime):
        date = _convert_date(date)
        return date.timetuple().tm_yday

    @inst.function
    def millisecond(date):
        date = _convert_date(date)
        return date.microsecond / 1000

    @inst.function()
    def in_(needle, heap):
        _check_type(heap, list)
        return needle in heap

    # STRING OPERATION

    @inst.function()
    def to_lower(val):
        _check_type(val, str)
        return val.lower()

    @inst.function()
    def to_upper(val):
        _check_type(val, str)
        return val.upper()

    @inst.function()
    def concat(*ops: List[str]):
        ops = _arg_if_list(ops)
        _check_type(ops, str)
        result = ''
        for ele in ops:
            result += ele
        return result

    @inst.function()
    def regex_match(input_, regex, options):
        _check_type(input_, str)
        _check_type(regex, str)
        flags = 0
        if 'i' in options:
            flags |= re.I
        if 's' in options:
            flags |= re.S
        if 'm' in options:
            flags |= re.M
        return re.search(regex, input_, flags=flags) is not None

    @inst.function()
    def index_of_CP(string: str, substring, start=0, end=-1):
        return string.index(substring, start, end)

    @inst.function()
    def index_of_bytes(string: str, substring, start=0, end=-1):
        return string.encode('utf-8').index(substring.encode('utf-8'), start, end)

    @inst.function()
    def substr_CP(string, start, length=0):
        if length == 0:
            length = len(string) - start
        return string[start:][:length]

    @inst.function()
    def str_len_bytes(val):
        _check_type(val, str)
        return len(val.encode('utf-8'))

    @inst.function()
    def str_len_CP(val):
        _check_type(val, str)
        return len(val)

    @inst.function()
    def str_len(val):
        return str_len_CP(val)

    @inst.function()
    def substr(*args, **kwargs):
        return substr_CP(*args, **kwargs)

    @inst.function()
    def replace_one(input_, find, replacement):
        return re.sub(find, replacement, str(input_), count=1)

    @inst.function()
    def replace_all(input_, find, replacement):
        return re.sub(find, replacement, str(input_))

    @inst.function()
    def to_upper(val):
        return str(val).upper()

    @inst.function()
    def to_lower(val):
        return str(val).lower()

    @inst.function()
    def split(string, delimiter):
        _check_type(string, str)
        _check_type(delimiter, str)
        return string.split(delimiter)

    for strip_oper in ('l', 'r', ''):
        @inst.function(name=f'{strip_oper}trim', bundle=strip_oper)
        def _strip(input_, chars=' ', bundle=''):
            _check_type(input_, str)
            _check_type(chars, (list, tuple, str))
            return getattr(input_, f'{bundle}strip')(chars)

    # OBJECT FIELD OPERATION

    @inst.function(context=True)
    def add_fields(context, **kwargs):
        for key, val in kwargs.items():
            target = context
            while '.' in key:
                par, key = key.split('.', 1)
                if par not in target:
                    target[par] = {}
                target = target[par]
            target[key] = val
        return context

    @inst.function(lazy=True)
    def set_field(field, input_, value):
        _check_type(field.parsed, str)
        _check_type(input_.parsed, dict)
        value = inst.evaluate(value.value, input_.parsed)
        input_[field.parsed] = value
        return input_

    @inst.function(lazy=True)
    def unset_field(field, input_):
        input_ = input_.value
        _check_type(field.parsed, str)
        _check_type(input_, dict)
        if field in input_:
            del input_[field]
        return input_

    @inst.function()
    def object_to_array(obj):
        _check_type(obj, dict)
        return [
            {'k': k, 'v': v}
            for k, v in obj.items()
        ]

    # LOGIC

    @inst.function(lazy=True)
    def and_(*conds):
        for cond in conds:
            if not cond.value:
                return False
        return True

    @inst.function(lazy=True)
    def or_(*conds):
        for cond in conds:
            if cond.value:
                return True
        return False

    @inst.function()
    def not_(val):
        return not val

    for comp_name in ('le', 'lte', 'gt', 'gte', 'eq', 'ne'):
        @inst.function(name=comp_name, bundle=comp_name)
        def _comp(opa, opb, bundle):
            cmp = '__%s__' % {'lte': 'le', 'gte': 'ge'}.get(bundle)
            return getattr(opa, cmp)(opb)
