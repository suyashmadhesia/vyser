from vyser.diagnostics.diagnostic_bag import DiagnosticBag

from .expression_syntax import ExpressionSyntax
from .syntax_kind import SyntaxKind


class SyntaxTree:

    def __init__(
        self,
        diagnostics: DiagnosticBag,
        root: ExpressionSyntax,
        end_of_file_token: SyntaxKind,
    ):
        self._diagnostics = diagnostics
        self._root = root
        self._end_of_file_token = end_of_file_token

    @property
    def diagnostics(self):
        return self._diagnostics

    @property
    def root(self):
        return self._root

    @property
    def end_of_file_token(self):
        return self._end_of_file_token

    @staticmethod
    def parse(parser) -> "SyntaxTree":
        return parser.parse()
