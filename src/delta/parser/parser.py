from typing import List, Text
from delta.lexer.mathFunctions import LOG

from delta.lexer.tokens import *
from delta.lexer.lexicalToken import LexicalToken
from .errors import InvalidExpression
from .nodes import BinaryNode, UnaryNode, Node

class Parser:

    precedence = {
            TT_PLUS : 1,
            TT_MINUS : 1,
            TT_MULTIPLY : 2,
            TT_DIVIDE : 3,
            TT_EXPONENT : 4,
            TT_FUNC : 5,
        }
    
    binary_nodes = [TT_PLUS, TT_MINUS, TT_DIVIDE, TT_MULTIPLY, TT_EXPONENT]
    unary_nodes = [TT_FUNC]
    nodes = [TT_REAL, TT_INT, TT_SYMBOL]

    def __init__(self, lexical_tokens: list):
        self.tokens = lexical_tokens
        self.head = None

    @staticmethod
    def __balanceOfBrackets(tokens):
        stack = []
        brackets_mapping = {TT_RCURLY : TT_LCURLY, TT_RPAREN : TT_LPAREN}
        for i in range(len(tokens)):
            if tokens[i] in [TT_LPAREN, TT_LCURLY]:
                stack.append((tokens[i], i))
            elif tokens[i] in [TT_RCURLY, TT_RPAREN]:
                if stack and stack[-1][0] == brackets_mapping[tokens[i].token_type]:
                    stack.pop()
                else:
                    return False, (tokens[i], i)

        return (True, (None, None)) if not(stack) else (False, stack[-1])

    @staticmethod
    def __postfix(tokens: List[LexicalToken]):
        postfix_expr = []
        stack = []
        brackets_mapping = {TT_RCURLY : TT_LCURLY, TT_RPAREN : TT_LPAREN}
        for token in tokens:
            if token in [TT_SYMBOL, TT_INT, TT_REAL, TT_COMMA]:
                postfix_expr.append(token)
            elif token in [TT_LPAREN, TT_LCURLY]:
                stack.append(token)
            elif token in [TT_RPAREN, TT_RCURLY]:
                while stack and stack[-1] != brackets_mapping[token.token_type]:
                    postfix_expr.append(stack.pop())

                if stack:
                    stack.pop()

            elif token in [TT_PLUS, TT_MINUS, TT_MULTIPLY, TT_DIVIDE, TT_EXPONENT, TT_FUNC]:
                while stack and Parser.precedence.get(token.token_type, 0) <= Parser.precedence.get(stack[-1].token_type, 0):
                    postfix_expr.append(stack.pop())
                stack.append(token)

        while stack:
            postfix_expr.append(stack.pop())

        return postfix_expr

    @staticmethod
    def __prefix(tokens: List[LexicalToken]):
        balanced, error = Parser.__balanceOfBrackets(tokens)
        if balanced:
            tokens = tokens[::-1]
            for i in range(len(tokens)):
                if tokens[i] == TT_LPAREN:
                    tokens[i] = LexicalToken(TT_RPAREN)
                elif tokens[i] == TT_RPAREN:
                    tokens[i] = LexicalToken(TT_LPAREN)
                
                if tokens[i] == TT_RCURLY:
                    tokens[i] = LexicalToken(TT_LCURLY)
                elif tokens[i] == TT_LCURLY:
                    tokens[i] = LexicalToken(TT_RCURLY)
            return Parser.__postfix(tokens)[::-1]
        raise Exception(InvalidExpression(f"Check for balance of brackets : {error}"))

    @staticmethod
    def __make_nodes(tokens):
        elem = tokens.pop(0)
        if elem in Parser.nodes:
            return Node(elem)
        else:
            if elem in Parser.binary_nodes or elem == LexicalToken(TT_FUNC, LOG):
                left = Parser.__make_nodes(tokens)

            if elem in Parser.unary_nodes or elem in Parser.binary_nodes:
                right = Parser.__make_nodes(tokens)

        if elem in Parser.binary_nodes or elem == LexicalToken(TT_FUNC, LOG):
            return BinaryNode(elem, left, right)

        if elem in Parser.unary_nodes:
            return UnaryNode(elem, right)

    def make_nodes(self):
        prefix_expr = Parser.__prefix(self.tokens)
        self.head = Parser.__make_nodes(prefix_expr)
        return self.head
