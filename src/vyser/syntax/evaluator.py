from typing import Dict

from vyser.diagnostics.diagnostic_bag import DiagnosticBag

from .binary_expression_syntax import BinaryExpressionSyntax
from .expression_syntax import ExpressionSyntax
from .literal_expression_syntax import LiteralExpressionSyntax
from .name_expression_syntax import NameExpressionSyntax
from .parenthesis_expression_syntax import ParenthesizedExpressionSyntax
from .syntax_kind import SyntaxKind
from .syntax_token import SyntaxToken
from .unary_expression_syntax import UnaryExpressionSyntax


class Evaluator:

    def __init__(self, root: ExpressionSyntax, data: Dict) -> None:
        self._root = root
        self._data = data
        self._diagnostics = DiagnosticBag()

    def access_value(self, instance, key):
        try:
            if isinstance(instance, list):
                key = int(key)
                return instance[key]
            elif isinstance(instance, dict):
                return instance[key]
            elif isinstance(instance, object):
                return getattr(instance, key)
            raise Exception(f"{key}")
        except Exception as e:
            return e

    def _get_identifier_value(self, identifier_token: SyntaxToken):
        identifier_name = identifier_token.text
        instance, *attrs = identifier_name.split(".")
        if not instance in self._data:
            self._diagnostics.report_undefined_name(identifier_token.span, instance)
            return None
        current_data = self._data.get(instance)
        for key in attrs:
            current_data = self.access_value(current_data, key)
            if isinstance(current_data, Exception):
                self._diagnostics.report_undefined_name(
                    identifier_token.span,
                    f"{current_data.args[0]} in {identifier_token.text}",
                )
                return None
        return current_data

    def _validate_int_binary_expression(self, left, right):
        return (
            (type(left) == int and type(right) == int)
            or type(left) == float
            and type(right) == float
        )

    def _validate_bool_binary_expression(self, left, right):
        return type(left) == bool and type(right) == bool

    def evaluate(self):
        try:
            return self._evaluate_expression(self._root)
        except Exception as e:
            print(e)

    def _evaluate_expression(self, node: ExpressionSyntax):
        if type(node) == ParenthesizedExpressionSyntax:
            return self._evaluate_expression(node.expression)

        if type(node) == LiteralExpressionSyntax:
            return node.value

        if type(node) == NameExpressionSyntax:
            return self._get_identifier_value(node.identifier_token)

        if type(node) == UnaryExpressionSyntax:
            operand = self._evaluate_expression(node.operand)
            if node.operator_token.kind == SyntaxKind.BangToken:
                return not bool(operand)
            if node.operator_token.kind == SyntaxKind.MinusToken:
                return -int(operand)
            if node.operator_token.kind == SyntaxKind.PlusToken:
                return int(operand)

        if type(node) == BinaryExpressionSyntax:
            left = self._evaluate_expression(node.left)
            right = self._evaluate_expression(node.right)

            if node.operator_token.kind == SyntaxKind.PlusToken:
                isValid = self._validate_int_binary_expression(left, right)
                if not isValid:
                    self._diagnostics.report_undefined_binary_operator(
                        node.operator_token.span, "+", type(left), type(right)
                    )
                    return
                return left + right
            if node.operator_token.kind == SyntaxKind.MinusToken:
                isValid = self._validate_int_binary_expression(left, right)
                if not isValid:
                    self._diagnostics.report_undefined_binary_operator(
                        node.operator_token.span, "-", type(left), type(right)
                    )
                    return
                return left - right
            if node.operator_token.kind == SyntaxKind.StarToken:
                isValid = self._validate_int_binary_expression(left, right)
                if not isValid:
                    self._diagnostics.report_undefined_binary_operator(
                        node.operator_token.span, "*", type(left), type(right)
                    )
                    return
                return left * right
            if node.operator_token.kind == SyntaxKind.SlashToken:
                isValid = self._validate_int_binary_expression(left, right)
                if not isValid:
                    self._diagnostics.report_undefined_binary_operator(
                        node.operator_token.span, "/", type(left), type(right)
                    )
                    return
                return left / right
            if node.operator_token.kind == SyntaxKind.SlashSlashToken:
                isValid = self._validate_int_binary_expression(left, right)
                if not isValid:
                    self._diagnostics.report_undefined_binary_operator(
                        node.operator_token.span, "//", type(left), type(right)
                    )
                    return
                return left // right
            if node.operator_token.kind == SyntaxKind.AmpersandAmpersandToken:
                isValid = self._validate_bool_binary_expression(left, right)
                if not isValid:
                    self._diagnostics.report_undefined_binary_operator(
                        node.operator_token.span, "&&", type(left), type(right)
                    )
                    return
                return left and right
            if node.operator_token.kind == SyntaxKind.PipePipeToken:
                isValid = self._validate_bool_binary_expression(left, right)
                if not isValid:
                    self._diagnostics.report_undefined_binary_operator(
                        node.operator_token.span, "||", type(left), type(right)
                    )
                    return
                return left or right
            if node.operator_token.kind == SyntaxKind.BangEqualToken:
                return left != right
            if node.operator_token.kind == SyntaxKind.EqualEqualToken:
                return left == right
            if node.operator_token.kind == SyntaxKind.GreaterThanEqualToken:
                return left >= right
            if node.operator_token.kind == SyntaxKind.GreaterThanToken:
                return left > right
            if node.operator_token.kind == SyntaxKind.LesserThanEqualToken:
                return left <= right
            if node.operator_token.kind == SyntaxKind.LesserThanToken:
                return left < right
            raise Exception(
                f"Invalid Binary operator token '{node.operator_token.text}'"
            )
        raise Exception(f"Invalid node kind '{node.kind.name}'")
