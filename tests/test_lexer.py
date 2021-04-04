import pytest
from delta.lexer.function import Function
from delta.lexer.lexer import Lexer
from delta.lexer.lexicalToken import LexicalToken
from delta.lexer.tokens import *
from delta.lexer.constants import SymbolicConstants, NumericalConstants

from delta.lexer.errors import Error, InvalidIdentifier

class TestLexer:
    def test_lexer_operators(self):
        l = Lexer("+-*/^")
        assert l.make_tokens() == [LexicalToken(TT_PLUS), LexicalToken(TT_MINUS), LexicalToken(TT_MULTIPLY), LexicalToken(TT_DIVIDE), LexicalToken(TT_EXPONENT)]

    def test_lexer_constants(self):
        numerical_constants = " ".join(map(str, NumericalConstants.constants))
        symbolic_constants = " ".join(map(str, SymbolicConstants.constants))
        tokens = []
        for i in NumericalConstants.constants:
            tokens.append(LexicalToken(TT_REAL, i))
        
        for i in SymbolicConstants.constants:
            tokens.append(LexicalToken(TT_SYMBOL, i))

        l = Lexer(numerical_constants + " " + symbolic_constants)
        assert l.make_tokens() == tokens
    
    def test_lexer_functions(self):
        functions = " ".join(map(str, Function.functions))
        tokens = []
        for i in Function.functions:
            tokens.append(LexicalToken(TT_FUNC, i))
        
        l = Lexer(functions)
        assert l.make_tokens() == tokens

    def test_lexer_custom_one(self):
        l = Lexer("x * e ^ x * log e(x)")
        assert l.make_tokens() == [LexicalToken(TT_SYMBOL, SymbolicConstants.get_constant('x')),
                                    LexicalToken(TT_MULTIPLY), 
                                    LexicalToken(TT_REAL, NumericalConstants.get_constant('e')),
                                    LexicalToken(TT_EXPONENT),
                                    LexicalToken(TT_SYMBOL, SymbolicConstants.get_constant('x')),
                                    LexicalToken(TT_MULTIPLY),
                                    LexicalToken(TT_FUNC, Function.get_function('log')),
                                    LexicalToken(TT_REAL, NumericalConstants.get_constant('e')),
                                    LexicalToken(TT_LPAREN),
                                    LexicalToken(TT_SYMBOL, SymbolicConstants.get_constant('x')),
                                    LexicalToken(TT_RPAREN)]
    
    def test_exception(self):
        with pytest.raises(InvalidIdentifier):
            l = Lexer("x * e ^ x + l")
            l.make_tokens()