from typing import Optional

from delta.lexer.function import Function
from delta.lexer.mathFunctions import *
from .constants import NumericalConstants, SymbolicConstants

from .position import Position
from .tokens import *
from .lexicalToken import LexicalToken
from .errors import InvalidIdentifier


class Lexer:
    def __init__(self, expression: str):
        self.expression = expression
        self.tokens = []
        self.pos: Position = Position(-1)
        self.curr_char: Optional[str] = None
        self.advance()

    def advance(self):
        self.pos.advance()
        if self.pos.idx >= len(self.expression):
            self.curr_char = None
        else:
            self.curr_char = self.expression[self.pos.idx]

    def make_tokens(self):
        while self.curr_char:

            if self.curr_char in ' \n\t':
                self.advance()

            # Operators
            elif self.curr_char == '+':
                self.tokens.append(LexicalToken(TT_PLUS))
                self.advance()
            elif self.curr_char == '-':
                self.tokens.append(LexicalToken(TT_MINUS))
                self.advance()
            elif self.curr_char == '*':
                self.tokens.append(LexicalToken(TT_MULTIPLY))
                self.advance()
            elif self.curr_char == '/':
                self.tokens.append(LexicalToken(TT_DIVIDE))
                self.advance()
            elif self.curr_char == '^':
                self.tokens.append(LexicalToken(TT_EXPONENT))
                self.advance()

            # Parenthesis
            elif self.curr_char == ')':
                self.tokens.append(LexicalToken(TT_RPAREN))
                self.advance()
            elif self.curr_char == '(':
                self.tokens.append(LexicalToken(TT_LPAREN))
                self.advance()

            # Numerical Constants, Symbolic Constants, Identifiers
            elif self.curr_char.isdigit():
                self.tokens.append(self.make_digits())
            elif self.curr_char.isalpha():
                start_pos = Position.copy(self.pos)
                ident = self.make_identifiers()
                if isinstance(ident, LexicalToken):
                    self.tokens.append(ident)
                else:
                    raise InvalidIdentifier(start_pos, self.pos, ident )

            else:
                start_pos = Position.copy(self.pos)
                char = self.curr_char
                self.advance()
                raise InvalidIdentifier(start_pos, self.pos, char)

        return self.tokens

    def make_identifiers(self):
        identifier = ""
        while self.curr_char and self.curr_char.isalpha():
            identifier += self.curr_char
            self.advance()

        constant = NumericalConstants.get_constant(identifier)
        if constant:
            return LexicalToken(TT_REAL, constant)

        constant = SymbolicConstants.get_constant(identifier)
        if constant:
            return LexicalToken(TT_SYMBOL, constant)

        func = Function.get_function(identifier)
        if func:
            return LexicalToken(TT_FUNC, func)

        return identifier

    def make_digits(self):
        number = ""
        decimal = 0
        while self.curr_char and (self.curr_char.isdigit() or self.curr_char == '.'):
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
