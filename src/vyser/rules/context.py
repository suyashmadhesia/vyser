from typing import Callable, List

from .base import Condition
from .factory import RuleFactory

# This is the base class for all the execution in the pipeline


class RuleContext:

    CONDITIONS = "condtions"
    HANDLER = "handler"

    def __init__(self, rule_name: str) -> None:
        self._rule_name = rule_name
        self._when_all_handlers = []
        self._when_any_handlers = []

    def __enter__(self):
        RuleFactory.register_rule_context(self)
        return self

    def __exit__(self, *args, **kwargs):
        return True

    def add_when_all_rule_callback(self, func: Callable, args):
        conditions: List[Condition] = []
        for arg in args:
            if not isinstance(arg, str):
                raise TypeError("Argument must be a string conditions")
            condition = Condition(arg)
            conditions.append(condition)
        self._when_all_handlers.append(
            {self.CONDITIONS: conditions, self.HANDLER: func}
        )

    def add_when_any_rule_callback(self, func: Callable, args):
        conditions: List[Condition] = []
        for arg in args:
            if not isinstance(arg, str):
                raise TypeError("Argument must be a string conditions")
            condition = Condition(arg)
            conditions.append(condition)
        self._when_any_handlers.append(
            {self.CONDITIONS: conditions, self.HANDLER: func}
        )

    def _execute_conditions(self, handler, data, result_operator):
        conditions = handler[self.CONDITIONS]
        result = [condition.evaluate(data) for condition in conditions]
        return result_operator(result)

    def execute_rule(self, data: dict):
        for handler in self._when_all_handlers:
            result = self._execute_conditions(handler, data, all)
            if result:
                handler[self.HANDLER](self)

        for handler in self._when_any_handlers:
            result = self._execute_conditions(handler, data, any)
            if result:
                handler[self.HANDLER](self)
    
