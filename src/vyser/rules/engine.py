from typing import Callable, List

from .base import *
from .context import *
from .factory import *


def when_all(context: RuleContext, *args: List[Condition]):
    def decorator(func: Callable):
        context.add_rule_callback(func, *args)

        def wrapper(c: RuleContext):
            return func(c)

        return wrapper

    return decorator


def when_any(context: RuleContext, *args: List[Condition]):
    def decorator(func: Callable):
        context.add_rule_callback(func, *args)

        def wrapper(c: RuleContext):
            return func(c)

        return wrapper

    return decorator


def set_context_attrs(object, data):
    for key, val in data.items():
        setattr(object, key, val)


def remove_context_attrs(object, data):
    for key, _ in data.items():
        delattr(object, key)


def assert_rule(rule_name: str, data: dict):
    context = RuleFactory.get_rule_context(rule_name)
    set_context_attrs(context, data)
    # TODO: perform rule validations
    context.execute_rule()
    remove_context_attrs(context, data)
    print(context.__dict__)
