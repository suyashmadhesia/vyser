from typing import List

from vyser.diagnostics.diagnostic_bag import DiagnosticBag

from .binary_expression_syntax import BinaryExpressionSyntax
from .expression_syntax import ExpressionSyntax
from .lexer import Lexer
from .literal_expression_syntax import LiteralExpressionSyntax
from .name_expression_syntax import NameExpressionSyntax
from .parenthesis_expression_syntax import ParenthesizedExpressionSyntax
from .syntax_facts import SyntaxFacts
from .syntax_kind import SyntaxKind
from .syntax_token import SyntaxToken
from .syntax_tree import SyntaxTree
from .unary_expression_syntax import UnaryExpressionSyntax


class Parser:

    def __init__(self, text: str) -> None:
        self._position = 0
        self._tokens: List[SyntaxToken] = []
        self._diagnostics: DiagnosticBag = DiagnosticBag()
        lexer = Lexer(text)
        while True:
            token = lexer.lex()
            if token.kind not in {SyntaxKind.WhiteSpaceToken, SyntaxKind.BadToken}:
                self._tokens.append(token)
            if token.kind == SyntaxKind.EndOfFileToken:
                break
        self._diagnostics.extend(lexer.diagnostics)

    def peek(self, offset=0):
        index: int = self._position + offset
        if index >= len(self._tokens):
            return self._tokens[-1]
        return self._tokens[index]

    @property
    def current(self):
        return self.peek()

    def next_token(self) -> SyntaxToken:
        current = self.current
        self._position += 1
        return current

    def match_token(self, kind: SyntaxKind) -> SyntaxToken:
        if self.current.kind == kind:
            return self.next_token()
        self._diagnostics.report_unexpected_token(
            self.current.span, self.current.kind, kind
        )
        return SyntaxToken(kind, self.current.position, "", None)

    def parse(self) -> SyntaxTree:
        expression = self.parse_expression()
        end_of_file_token = self.match_token(SyntaxKind.EndOfFileToken)
        return SyntaxTree(self._diagnostics, expression, end_of_file_token)

    def parse_expression(self, parent_precedence=0) -> ExpressionSyntax:
        left = None
        unary_operator_precedence = SyntaxFacts.get_unary_operator_precedence(
            self.current.kind
        )
        if (
            unary_operator_precedence != 0
            and unary_operator_precedence >= parent_precedence
        ):
            operator_token = self.next_token()
            operand = self.parse_expression(unary_operator_precedence)
            left = UnaryExpressionSyntax(operator_token, operand)
        else:
            left = self.parse_primary_expression()

        while True:
            precedence = SyntaxFacts.get_binary_operator_precedence(self.current.kind)
            if precedence == 0 or precedence <= parent_precedence:
                break
            operator_token = self.next_token()
            right = self.parse_expression(precedence)
            left = BinaryExpressionSyntax(left, operator_token, right)
        return left

    def parse_primary_expression(self) -> ExpressionSyntax:
        if self.current.kind == SyntaxKind.OpenParenthesisToken:
            left = self.next_token()
            expression = self.parse_expression()
            right = self.match_token(SyntaxKind.CloseParenthesisToken)
            return ParenthesizedExpressionSyntax(left, expression, right)
        elif (
            self.current.kind == SyntaxKind.TrueKeywordToken
            or self.current.kind == SyntaxKind.FalseKeywordToken
            or self.current.kind == SyntaxKind.StringToken
            or self.current.kind == SyntaxKind.NilToken
        ):
            keyword = self.next_token()
            value = SyntaxFacts.get_keyword_value(keyword)
            return LiteralExpressionSyntax(keyword, value)

        elif self.current.kind == SyntaxKind.IdentifierToken:
            idetifier = self.next_token()
            return NameExpressionSyntax(idetifier)
        else:
            number_token = self.match_token(SyntaxKind.NumberToken)
            return LiteralExpressionSyntax(number_token, number_token.value)
