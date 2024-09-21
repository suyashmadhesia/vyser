from vyser.syntax.evaluator import Evaluator
from vyser.syntax.parser import Parser
from vyser.syntax.syntax_tree import SyntaxTree


class Condition:

    def __init__(self, condition: str):
        self._condition = condition
        self._parser = Parser(self._condition)
        self._expression_tree = SyntaxTree.parse(self._parser)
        self._diagnostics = self._expression_tree._diagnostics
        if self._diagnostics.any():
            self.show_diagnostics(self._diagnostics)

    def show_diagnostics(self, diagnostics):
        for diagnostic in diagnostics:
            print(diagnostic)
            print("\n Please fix error above")

    def evaluate(self, data: dict):
        if not self._diagnostics.any():
            evaluator = Evaluator(self._expression_tree._root, data)
            result = evaluator.evaluate()
            if evaluator._diagnostics.any():
                self.show_diagnostics(evaluator._diagnostics)
            else:
                return result
        else:
            self.show_diagnostics(self._diagnostics)
