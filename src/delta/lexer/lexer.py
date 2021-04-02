from typing import Optional

from .position import Position
from .lexicalToken import LexicalToken
from .tokens import *


class Lexer:
    def __init__(self, expression: str):
        self.expression = expression
        self.tokens = []
        self.pos: Position = Position(-1)
        self.curr_char: Optional[str] = None
        self.advance()

    def advance(self):
        if self.pos.idx > len(self.expression):
            self.curr_char = None
        else:
            self.curr_char = self.expression[self.pos.idx]

    def make_tokens(self):
        while self.curr_char:
            if self.curr_char.isdigit():
                self.tokens.append(self.make_digits())
            if self.curr_char.isalpha():
                self.tokens.append(self.make_identifiers())

        return self.tokens

    def make_identifiers(self):
        identifier = ""
        while self.curr_char and self.curr_char.isalpha():
            identifier += self.curr_char
            self.advance()

        if len(identifier) == 1:
            return

    def make_digits(self):
        number = ""
        decimal = 0
        while self.curr_char and (self.curr_char.isdigit() or self.curr_char is '.'):
            if self.curr_char == '.':
                if decimal == 1:
                    break

                decimal += 1

            number += self.curr_char
            self.advance()

        if decimal > 0:
            return LexicalToken(TT_REAL, float(number))
        else:
            return LexicalToken(TT_INT, int(number))