from vyser.diagnostics.text_span import TextSpan

from .iterator import Iterator


class SyntaxNode:
    def __init__(self) -> None:
        pass


class SyntaxToken(SyntaxNode):
    def __init__(self, kind, position, text, value=None) -> None:
        self._kind = kind
        self._position = position
        self._text = text
        self._value = value

    @property
    def kind(self):
        return self._kind

    @property
    def position(self):
        return self._position

    @property
    def text(self):
        return self._text

    @property
    def value(self):
        return self._value

    @property
    def span(self):
        return TextSpan(self._position, len(self._text))

    @property
    def get_children(self):
        return Iterator([])

    def __repr__(self) -> str:
        return f"{self.kind.name} {self.text}"
