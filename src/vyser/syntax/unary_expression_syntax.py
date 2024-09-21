from typing import List

from .expression_syntax import ExpressionSyntax
from .iterator import Iterator
from .syntax_kind import SyntaxKind
from .syntax_node import SyntaxNode


class UnaryExpressionSyntax(ExpressionSyntax):
    def __init__(self, operator_token, operand):
        self._operatorToken = operator_token
        self._operand = operand

    @property
    def operator_token(self):
        return self._operatorToken

    @property
    def operand(self):
        return self._operand

    @property
    def kind(self):
        return SyntaxKind.UnaryExpression

    @property
    def get_children(self) -> List[SyntaxNode]:
        return Iterator([self.operator_token, self.operand])
