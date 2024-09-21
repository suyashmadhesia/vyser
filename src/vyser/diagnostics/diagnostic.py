from .text_span import TextSpan


class Diagnostic:

    def __init__(self, span: TextSpan, message: str) -> None:
        self.span = span
        self.message = message

    def __repr__(self) -> str:
        return self.message
