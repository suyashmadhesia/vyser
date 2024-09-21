from .expression_syntax import ExpressionSyntax
from .iterator import Iterator
from .syntax_kind import SyntaxKind


class ParenthesizedExpressionSyntax(ExpressionSyntax):
    def __init__(self, open_parenthesis, expression, close_parenthesis):
        self._open_parenthesis = open_parenthesis
        self._expression = expression
        self._close_parenthesis = close_parenthesis

    @property
    def open_parenthesis(self):
        return self._open_parenthesis

    @property
    def expression(self):
        return self._expression

    @property
    def close_parenthesis(self):
        return self._close_parenthesis

    @property
    def kind(self):
        return SyntaxKind.ParenthesizedExpression

    @property
    def get_children(self):
        return Iterator(
            [self.open_parenthesis, self.expression, self.close_parenthesis]
        )
