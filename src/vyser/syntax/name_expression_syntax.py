from .expression_syntax import ExpressionSyntax
from .iterator import Iterator
from .syntax_kind import SyntaxKind
from .syntax_token import SyntaxToken


class NameExpressionSyntax(ExpressionSyntax):

    def __init__(self, identifier_token: SyntaxToken) -> None:
        self._identifier_token = identifier_token

    @property
    def kind(self):
        return SyntaxKind.NameExpression

    @property
    def identifier_token(self):
        return self._identifier_token

    @property
    def get_children(self):
        return Iterator([self.identifier_token])
