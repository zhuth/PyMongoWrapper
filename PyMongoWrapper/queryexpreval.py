"""Query Expression Evaluator"""

from typing import Union, List, Dict, Callable
from functools import wraps
import re
import math
import datetime
import dateutil.parser
from bson import ObjectId


RE_DIGITS = re.compile(r'^[+\-]?\d+$')
UNITS = 'year quarter week month day hour minute second millisecond'.split()


class QueryExprEvaluator:
    """Evaluate Query Expression
    """

    def __init__(self):
        """Initialize Query Expression Evaluator

        Args:
            implementations (dict, optional): Implementations of functions. Defaults to None.
        """
        self._impl = {}
        _default_impls(self)

    def _operator(self, operator_name):
        operator_name = operator_name.lstrip('$')
        operator = {
            'lte': 'le',
            'gte': 'ge',
            '': 'eq'
        }.get(operator_name, operator_name)
        return f'__{operator}__'

    def _compare(self, operator, *args):
        operator = self._operator(operator)
        if len(args) == 2:
            op_a, op_b = args
            return self._getfunc(op_a, operator)(op_b)

    def _getattr(self, obj, key, default=None):
        if key.startswith('$'):
            key = key[1:]

        if key == '$ROOT':
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
        if relation == 'eq' and isinstance(val, dict) and len(val) == 1 and tuple(val.keys())[0].startswith('$'):
            relation,  = val.keys()
            val = val[relation]
            relation = relation[1:]

        oprname = self._operator(relation)

        if oprname == '__in__':
            return obj in val

        if oprname == '__size__':
            return len(obj) == val

        if oprname == '__regex__':
            return re.search(val, obj, flags=re.I) is not None

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

    def function(self, mapping: Dict = None, lazy=False, context=False):
        """Register function

        Args:
            mapping (Dict, optional): A dict in the form of
                {arg_name: programmatic_arg_name} Defaults to None.
            lazy(bool, optional): Use `value` property to evaluate
        """

        if mapping is None:
            mapping = {}

        class _Lazy:

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
                return func(*args, **kwargs)

            self._impl[_camelize(func.__name__)] = _wrapped
            return func

        return _do

    @property
    def implemented_functions(self):
        """Get names of implemented functions
        """
        return self._impl.keys()

    def evaluate(self, parsed: Union[List, Dict], obj: dict):
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
                else:
                    temp = self._test_inputs(obj, val, key[1:])

                result = _append_result(temp)
            else:
                result = _append_result(self._test_inputs(
                    self._getattr(obj, key), {opr: opa for opr, opa in val.items() if opr.startswith('$') and opr != '$options'} if isinstance(val, dict) else val))

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

    def _arg_if_list(ops):
        if isinstance(ops, tuple) and len(ops) == 1 and isinstance(ops[0], list):
            ops = ops[0]
        return ops

    @inst.function()
    def size(val):
        return len(val)

    @inst.function()
    def first(val):
        for i in val:
            return i

    @inst.function()
    def last(val):
        i = None
        for i in val:
            pass
        return i

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
    def abs_(val):
        _check_type(val, (int, float))
        return abs(val)

    @inst.function()
    def add(*ops):
        ops = _arg_if_list(ops)
        _check_type(ops, (int, float))
        return sum(ops)

    @inst.function()
    def substract(opa, opb):
        _check_type((opa, opb), (int, float))
        return opa - opb

    @inst.function()
    def mod(opa, opb):
        _check_type((opa, opb), (int,))
        return opa % opb

    @inst.function()
    def multiply(*ops):
        ops = _arg_if_list(ops)
        _check_type(ops, (int, float))
        result = 1
        for ele in ops:
            result *= ele
        return result

    @inst.function()
    def divide(opa, opb):
        _check_type((opa, opb), (int, float))
        return opa/opb

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
    def concat(*ops):
        ops = _arg_if_list(ops)
        _check_type(ops, str)
        result = ''
        for ele in ops:
            result += ele
        return result

    @inst.function()
    def concat_arrays(*ops):
        ops = _arg_if_list(ops)
        _check_type(ops, list)
        result = []
        for ele in ops:
            result += ele
        return result

    @inst.function(mapping={'input': 'input_', 'to': 'to_'})
    def convert(input_, to_):
        _check_type(to_, (int, str))
        if to_ in (1, 'double', 19, 'decimal'):
            return float(input_)
        elif to_ in (2, 'string'):
            return str(input_)
        elif to_ in (7, 'objectId'):
            return ObjectId(input_)
        elif to_ in (8, 'bool'):
            return not not input_
        elif to_ in (9, 'date'):
            return dateutil.parser.parse(str(input_)) \
                if not isinstance(input_, datetime.datetime) else input_
        else:
            return int(input_)

    @inst.function()
    def to_string(val):
        return convert(val, 'string')

    @inst.function()
    def to_int(val):
        return convert(val, 'int')

    @inst.function()
    def to_long(val):
        return to_int(val)

    @inst.function()
    def to_bool(val):
        return convert(val, 'bool')

    @inst.function()
    def to_date(val):
        return convert(val, 'date')

    @inst.function()
    def to_double(val):
        return convert(val, 'double')

    @inst.function()
    def to_decimal(val):
        return to_double(val)

    @inst.function()
    def to_object_id(val):
        return convert(val, 'objectId')

    @inst.function()
    def to_lower(val):
        _check_type(val, str)
        return val.lower()

    @inst.function()
    def to_upper(val):
        _check_type(val, str)
        return val.upper()

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

    @inst.function()
    def year(val):
        _check_type(val, datetime.datetime)
        return val.year

    @inst.function()
    def month(val):
        _check_type(val, datetime.datetime)
        return val.month

    @inst.function()
    def day(val):
        _check_type(val, datetime.datetime)
        return val.day

    @inst.function()
    def floor(val):
        _check_type(val, (int, float))
        return math.floor(val)

    @inst.function()
    def ceil(val):
        _check_type(val, (int, float))
        return math.ceil(val)

    @inst.function()
    def in_(needle, heap):
        _check_type(heap, list)
        return needle in heap

    @inst.function(mapping={'input': 'input_'})
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
    def index_of_array(arr, search, start=0, end=-1):
        _check_type(arr, list)
        if end < start:
            end = len(arr)
        try:
            return arr[start:end+1].index(search) + start
        except ValueError:
            return -1

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

    @inst.function(mapping={'input': 'input_'})
    def ltrim(input_, chars=' '):
        _check_type(input_, str)
        _check_type(chars, (list, tuple, str))
        return input_.lstrip(chars)

    @inst.function(mapping={'input': 'input_'})
    def rtrim(input_, chars=' '):
        _check_type(input_, str)
        _check_type(chars, (list, tuple, str))
        return input_.rstrip(chars)

    @inst.function(mapping={'input': 'input_'})
    def trim(input_, chars=' '):
        _check_type(input_, str)
        _check_type(chars, (list, tuple, str))
        return input_.strip(chars)

    @inst.function(mapping={'input': 'input_', 'as': 'as_', 'in': 'in_'}, context=True, lazy=True)
    def map_(input_, as_, in_, context):
        as_ = as_.parsed
        _check_type(as_, str)
        as_ = '$' + as_
        result = []
        context[as_] = None
        for ele in input_.value:
            context[as_] = ele
            result.append(inst.evaluate(in_.parsed, context))
        del context[as_]
        return result

    @inst.function(mapping={'input': 'input_'}, lazy=True)
    def set_field(field, input_, value):
        _check_type(field.parsed, str)
        _check_type(input_.parsed, dict)
        value = inst.evaluate(value.value, input_.parsed)
        input_[field.parsed] = value
        return input_

    @inst.function(mapping={'input': 'input_'}, lazy=True)
    def unset_field(field, input_):
        input_ = input_.value
        _check_type(field.parsed, str)
        _check_type(input_, dict)
        if field in input_:
            del input_[field]
        return input_

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
