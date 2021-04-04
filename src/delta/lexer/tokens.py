from .tokenType import TokenType

# Variables, Numerals
TT_INT = TokenType('INT')
TT_REAL = TokenType('REAL')

# Special Variables
TT_SYMBOL = TokenType('SYMBOL')

# Special Mathematical Functions
TT_FUNC = TokenType('FUNCTION')

# Mathematical Operators
TT_PLUS = TokenType('PLUS', '+')
TT_MINUS = TokenType('MINUS', '-')
TT_DIVIDE = TokenType('DIVIDE', '/')
TT_MULTIPLY = TokenType('MULTIPLY', '*')
TT_EXPONENT = TokenType('EXPONENT', '^')

# Mathematical Expression Operators
TT_LPAREN = TokenType('LPAREN', '(')
TT_RPAREN = TokenType('RPAREN', ')')