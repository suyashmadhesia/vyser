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
        self._condition_handlers = {}

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

    def add_condition_callback(self, func: Callable, condition_key):
        if not isinstance(condition_key, str):
            raise TypeError("Condition key must be a string")
        self._condition_handlers[condition_key] = func

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

    def _execute_rules(self, handler, data, result_operator):
        conditions = handler[self.CONDITIONS]
        result = [condition.evaluate(data) for condition in conditions]
        return result_operator(result)

    def execute_rule(self, data: dict):
        for handler in self._when_all_handlers:
            result = self._execute_rules(handler, data, all)
            if result:
                handler[self.HANDLER](self)

        for handler in self._when_any_handlers:
            result = self._execute_rules(handler, data, any)
            if result:
                handler[self.HANDLER](self)

    def _execute_conditions(self, conditions, data):
        result = [condition.evaluate(data) for condition in conditions]
        return all(result)

    def execute_condition(self, conditions_data: List[dict], data: dict):
        for condition_data in conditions_data:
            conditions_strs = condition_data["value"]
            condition_handler_name = condition_data["handler"]
            condition_instances = [
                Condition(condition_str)
                for condition_str in conditions_strs
                if isinstance(condition_str, str)
            ]
            condition_handler = self._condition_handlers.get(condition_handler_name)
            if not condition_handler:
                raise ValueError(f"Handler '{condition_handler_name}' not found")
            if self._execute_conditions(condition_instances, data):
                condition_handler(self)
