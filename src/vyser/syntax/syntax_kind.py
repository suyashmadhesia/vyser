from enum import Enum


class SyntaxKind(Enum):
    EndOfFileToken = 0
    NumberToken = 1
    WhiteSpaceToken = 2
    PlusToken = 3
    MinusToken = 4
    StarToken = 5
    SlashToken = 6
    BadToken = 7
    BinaryExpression = 8
    LiteralExpression = 9
    ParenthesizedExpression = 10
    OpenParenthesisToken = 11
    CloseParenthesisToken = 12
    UnaryExpression = 13
    AmpersandAmpersandToken = 14
    PipePipeToken = 15
    BangToken = 16
    EqualEqualToken = 17
    BangEqualToken = 18
    TrueKeywordToken = 19
    FalseKeywordToken = 20
    IdentifierToken = 21
    StringToken = 22
    GreaterThanToken = 23
    LesserThanToken = 24
    GreaterThanEqualToken = 25
    LesserThanEqualToken = 26
    NilToken = 27
    NameExpression = 28
    SlashSlashToken = 29
