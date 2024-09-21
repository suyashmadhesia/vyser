from typing import List

from vyser.syntax.syntax_kind import SyntaxKind

from .diagnostic import Diagnostic
from .text_span import TextSpan


class DiagnosticBag:

    def __init__(self) -> None:
        self._diagnostics: List[Diagnostic] = []

    def _report(self, span: TextSpan, message: str):
        diagnostic = Diagnostic(span, message)
        self._diagnostics.append(diagnostic)

    def report_bad_character(self, position: int, character: str):
        message = f"ERROR: bad character input at <{position}> <{character}>."
        self._report(TextSpan(position, 1), message)

    def extend(self, diagnostics: "DiagnosticBag"):
        self._diagnostics.append(diagnostics._diagnostics)

    def report_invalid_number(self, span: TextSpan, text: str, type_: str):
        message = f"The number '{text}' is not a valid <{type_}>."
        self._report(span, message)

    def report_unexpected_token(
        self, span: TextSpan, actual_kind: SyntaxKind, expected_kind: SyntaxKind
    ):
        message = f"ERROR: Unexpected token <{actual_kind.name}>, expected <{expected_kind.name}>."
        self._report(span, message)

    def report_undefined_unary_operator(
        self, span: TextSpan, operator_text: str, operand_type: str
    ):
        message = (
            f"Unary operator '{operator_text}' is not defined for type {operand_type}."
        )
        self._report(span, message)

    def report_undefined_binary_operator(
        self, span: TextSpan, operator_text: str, left_type: str, right_type: str
    ):
        message = f"Binary operator '{operator_text}' is not defined for types {left_type} and {right_type}."
        self._report(span, message)

    def report_undefined_name(self, span: TextSpan, name: str):
        message = f"Variable name '{name}' doesn't exist."
        self._report(span, message)

    def extend(self, diagnostics: "DiagnosticBag"):
        self._diagnostics.extend(diagnostics._diagnostics)

    def __iter__(self):
        return iter(self._diagnostics)

    @property
    def diagnostics(self):
        return self._diagnostics

    def any(self):
        return len(self._diagnostics) != 0
