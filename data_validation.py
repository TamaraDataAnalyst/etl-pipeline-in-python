from typing import get_type_hints
from functools import wraps
from inspect import getfullargspec


def data_validation(obj, **kwargs):
    hints = get_type_hints(obj)

    # iterate all type hints
    for colname, datatype in hints.items():
        if colname == 'return':
            continue

        if not isinstance(kwargs[colname],datatype):
            raise TypeError(
                'Argument %r is not of type %s' % (colname, datatype)
            )


def assert_type(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # translate *args into **kwargs
        func_args = getfullargspec(func)[0]
        kwargs.update(dict(zip(func_args, args)))

        data_validation(func, **kwargs)
        return func(**kwargs)

    return wrapper

