from .expression_syntax import ExpressionSyntax
from .iterator import Iterator
from .syntax_kind import SyntaxKind
from .syntax_token import SyntaxToken


class LiteralExpressionSyntax(ExpressionSyntax):

    def __init__(self, literal_token: SyntaxToken, value=None):
        self._literal_token = literal_token
        self._value = value

    @property
    def kind(self):
        return SyntaxKind.LiteralExpression

    @property
    def literal_token(self):
        return self._literal_token

    @property
    def value(self):
        return self._value

    @property
    def get_children(self):
        return Iterator([self.literal_token])
