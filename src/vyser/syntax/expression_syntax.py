from .syntax_node import SyntaxNode


class ExpressionSyntax(SyntaxNode):
    pass

    def __repr__(self) -> str:
        return self.__class__.__name__
