from .syntax_kind import SyntaxKind


class SyntaxFacts:

    @staticmethod
    def get_unary_operator_precedence(kind: SyntaxKind) -> int:
        if (
            kind == SyntaxKind.PlusToken
            or kind == SyntaxKind.MinusToken
            or kind == SyntaxKind.BangToken
        ):
            return 7
        return 0

    @staticmethod
    def get_binary_operator_precedence(kind: SyntaxKind) -> int:
        if (
            kind == SyntaxKind.StarToken
            or kind == SyntaxKind.SlashToken
            or kind == SyntaxKind.SlashSlashToken
        ):
            return 6
        if kind == SyntaxKind.PlusToken or kind == SyntaxKind.MinusToken:
            return 5
        if (
            kind == SyntaxKind.GreaterThanToken
            or kind == SyntaxKind.GreaterThanEqualToken
            or kind == SyntaxKind.LesserThanToken
            or kind == SyntaxKind.LesserThanEqualToken
        ):
            return 4
        if kind == SyntaxKind.EqualEqualToken or kind == SyntaxKind.BangEqualToken:
            return 3
        if kind == SyntaxKind.AmpersandAmpersandToken:
            return 2
        if kind == SyntaxKind.PipePipeToken:
            return 1
        return 0

    @staticmethod
    def get_keyword_kind(text):
        if text == "true":
            return SyntaxKind.TrueKeywordToken
        if text == "false":
            return SyntaxKind.FalseKeywordToken
        if text == "nil":
            return SyntaxKind.NilToken
        return SyntaxKind.BadToken

    @staticmethod
    def get_keyword_value(token):
        if (
            token.kind == SyntaxKind.TrueKeywordToken
            or token.kind == SyntaxKind.FalseKeywordToken
        ):
            return token.kind == SyntaxKind.TrueKeywordToken
        elif token.kind == SyntaxKind.NilToken:
            return None
        else:
            return token.text
