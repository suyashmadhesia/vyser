from typing import Callable, List

from rules.base import Condition
from rules.factory import RuleFactory

# This is the base class for all the execution in the pipeline


class RuleContext:

    CONDITIONS = "condtions"
    HANDLER = "handler"

    def __init__(self, rule_name: str) -> None:
        self._rule_name = rule_name
        self._id = 0
        self._handlers = {}

    def __enter__(self):
        RuleFactory.register_rule_context(self)
        return self

    def __exit__(self, *args, **kwargs):
        return True

    def add_rule_callback(self, func: Callable, *args: List[Condition]):
        self._handlers[self._id] = {self.CONDITIONS: args, self.HANDLER: func}
        self._id += 1

    def execute_rule(self):
        for k, value in self._handlers.items():
            value[self.HANDLER](self)
