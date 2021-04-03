from typing import Any


class TokenType:
    def __init__(self, token_name: str, token_symbol: Any = None):
        self.token_name = token_name
        self.token_symbol = token_symbol

    def __hash__(self) -> int:
        return self.token_symbol.__hash__()

    def __eq__(self, other: "TokenType"):
        return other.token_name == self.token_name and other.token_symbol == self.token_symbol

    def __str__(self):
        return str(self.token_symbol)

    def __repr__(self):
        return str(self.token_symbol)
