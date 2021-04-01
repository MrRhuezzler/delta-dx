from typing import Any
from .tokenType import TokenType


class LexicalToken:
    def __init__(self, token_type: TokenType, value: Any = None):
        self.token_type = token_type
        self.value = value

    def __eq__(self, other):
        if isinstance(other, LexicalToken):
            return other.token_type == self.token_type and self.value == other.value
        elif isinstance(other, TokenType):
            return self.token_type == other
        else:
            return False

    def __str__(self):
        return str(self.value) if self.value is not None else str(self.token_type)

    def __repr__(self):
        return str(self.value) if self.value is not None else str(self.token_type)
