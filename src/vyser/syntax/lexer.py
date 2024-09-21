from typing import List

from vyser.diagnostics.diagnostic_bag import DiagnosticBag
from vyser.diagnostics.text_span import TextSpan

from .syntax_facts import *
from .syntax_kind import *
from .syntax_token import *


class Lexer:
    def __init__(self, text):
        self._text: str = text
        self._position: int = 0
        self._diagnostics = DiagnosticBag()

    @property
    def diagnostics(self):
        return self._diagnostics

    def _peek(self, offset: int = 0):
        index: int = self._position + offset
        if index >= len(self._text):
            return "\0"
        return self._text[index]

    @property
    def current(self):
        return self._peek(0)

    def _next(self):
        self._position += 1

    @property
    def _lookahead(self):
        return self._peek(1)

    @property
    def _end(self):
        return self._position >= len(self._text)

    def lex(self):
        # if position of the line exceeds its length
        if self._position >= len(self._text):
            return SyntaxToken(SyntaxKind.EndOfFileToken, self._position, "\0")

        # Covers all whitespaces
        if self.current.isspace() or not len(self.current):
            start: int = self._position
            while self.current.isspace() or not len(self.current):
                self._next()
            text: str = self._text[start : self._position]
            return SyntaxToken(SyntaxKind.WhiteSpaceToken, start, text)

        # covers number or float literals
        if self.current.isdigit():
            start: int = self._position
            flt = 0
            while self.current.isdigit():
                self._next()
            if self._peek() == "." and self._lookahead.isdigit():
                flt = 1
                self._next()
                while self._peek().isdigit():
                    self._next()
            length: int = self._position - start
            text = self._text[start : self._position]
            try:
                value = float(text) if flt else int(text)
            except:
                self._diagnostics.report_invalid_number(
                    TextSpan(start, length), self._text, int
                )
            return SyntaxToken(SyntaxKind.NumberToken, start, text, value)

        # # covers all the constant numbers or strings
        # if self.current.isalpha():
        #     start: int = self._position
        #     while self.current.isalpha():
        #         self._next()
        #     text: str = self._text[start: self._position]
        #     kind = SyntaxFacts.get_keyword_kind(text)
        #     return SyntaxToken(kind, start, text)

        # creates an identifier token
        if self.current == "$":
            self._next()
            start: int = self._position
            while (
                self.current.isalpha()
                or self.current == "."
                or self.current == "_"
                or self.current.isdigit()
            ):  # it is also considering the digits for array indices
                self._next()
            text: str = self._text[start : self._position]
            return SyntaxToken(SyntaxKind.IdentifierToken, start, text)

        # all other cases handled here
        if self.current == "+":
            self._next()
            return SyntaxToken(SyntaxKind.PlusToken, self._position, "+")
        if self.current == "-":
            self._next()
            return SyntaxToken(SyntaxKind.MinusToken, self._position, "-")
        if self.current == "*":
            self._next()
            return SyntaxToken(SyntaxKind.StarToken, self._position, "*")
        if self.current == "/":
            if self._lookahead == "/":
                self._next()
                self._next()
                return SyntaxToken(SyntaxKind.SlashSlashToken, self._position, "//")
            self._next()
            return SyntaxToken(SyntaxKind.SlashToken, self._position, "/")
        if self.current == "(":
            self._next()
            return SyntaxToken(SyntaxKind.OpenParenthesisToken, self._position, "(")
        if self.current == ")":
            self._next()
            return SyntaxToken(SyntaxKind.CloseParenthesisToken, self._position, ")")
        if self.current == "&":
            if self._lookahead == "&":
                self._next()
                self._next()
                return SyntaxToken(
                    SyntaxKind.AmpersandAmpersandToken, self._position, "&&"
                )
        if self.current == "|":
            if self._lookahead == "|":
                self._next()
                self._next()
                return SyntaxToken(SyntaxKind.PipePipeToken, self._position, "||")
        if self.current == "=":
            if self._lookahead == "=":
                self._next()
                self._next()
                return SyntaxToken(SyntaxKind.EqualEqualToken, self._position, "==")
        if self.current == "!":
            if self._lookahead == "=":
                self._next()
                self._next()
                return SyntaxToken(SyntaxKind.BangEqualToken, self._position, "!=")
            self._next()
            return SyntaxToken(SyntaxKind.BangToken, self._position, "!")
        if self.current == "<":
            if self._lookahead == "=":
                self._next()
                self._next()
                return SyntaxToken(
                    SyntaxKind.LesserThanEqualToken, self._position, "<="
                )
            self._next()
            return SyntaxToken(SyntaxKind.LesserThanToken, self._position, "<")
        if self.current == ">":
            if self._lookahead == "=":
                self._next()
                self._next()
                return SyntaxToken(
                    SyntaxKind.GreaterThanEqualToken, self._position, ">="
                )
            self._next()
            return SyntaxToken(SyntaxKind.GreaterThanToken, self._position, ">")
        if self.current == "'":
            self._next()
            start = self._position
            while self._peek() != "'" and not self._end:
                self._next()
            text: str = self._text[start : self._position]
            self._next()
            return SyntaxToken(SyntaxKind.StringToken, self._position, text)

        self._diagnostics.report_bad_character(self._position, self.current)
        self._next()
        return SyntaxToken(
            SyntaxKind.BadToken,
            self._position,
            self._text[self._position - 1 : self._position + 1],
        )
