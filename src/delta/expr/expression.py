import sys

from delta.parser.nodes import Node, BinaryNode, UnaryNode
from delta.parser.parser import Parser
from delta.lexer.lexer import Lexer
from delta.lexer.tokens import *
from delta.lexer.mathFunctions import *
from delta.lexer.constants import NumericalConstants
from delta.lexer.lexicalToken import LexicalToken


class Expression:
    def __init__(self, expression: str):
        self.__lexer = Lexer(expression)
        self.__parser = Parser(self.__lexer.make_tokens())
        self.head_node = self.__parser.make_nodes()
        self.expression = expression

    @classmethod
    def from_nodes(cls, head_node):
        expression = Expression.to_string(head_node)
        expr = cls(expression)
        expr.head_node = head_node
        return expr

    @staticmethod
    def __inorder_traversal(node, string):
        if node:
            if not(node.lexical_token == TT_INT or node.lexical_token == TT_SYMBOL):
                string.append('(')

            if isinstance(node, BinaryNode) and not(node.lexical_token == TT_FUNC):
                Expression.__inorder_traversal(node.left_child, string)

            string.append(str(node))

            if isinstance(node, BinaryNode) and node.lexical_token == TT_FUNC:
                Expression.__inorder_traversal(node.left_child, string)

            if isinstance(node, UnaryNode) or isinstance(node, BinaryNode):
                if node.lexical_token == TT_FUNC:
                    string.append('(')
                
                Expression.__inorder_traversal(node.right_child, string)

                if node.lexical_token == TT_FUNC:
                    string.append(')')

            if not (node.lexical_token == TT_INT or node.lexical_token == TT_SYMBOL):
                string.append(')')

    @staticmethod
    def to_string(node):
        string = []
        Expression.__inorder_traversal(node, string)
        return ' '.join(string)

    def __repr__(self):
        return Expression.to_string(self.head_node)

    @staticmethod
    def __fold_node(node):
        lex = node.lexical_token
        if lex == TT_EXPONENT:
            a = node.left_child
            b = node.right_child
            if a.lexical_token == LexicalToken(TT_INT, 1) or b.lexical_token == LexicalToken(TT_INT, 0):
                return Node(LexicalToken(TT_INT, 1))
            elif b.lexical_token == LexicalToken(TT_INT, 1):
                return a
            elif a.lexical_token == LexicalToken(TT_INT, 0):
                return Node(LexicalToken(TT_INT, 0))

        elif lex == TT_MULTIPLY:
            a = node.left_child
            b = node.right_child
            if a.lexical_token == LexicalToken(TT_INT, 1):
                return b
            elif b.lexical_token == LexicalToken(TT_INT, 1):
                return a
            elif a.lexical_token == LexicalToken(TT_INT, 0) or b.lexical_token == LexicalToken(TT_INT, 0):
                return Node(LexicalToken(TT_INT, 0))

        elif lex == TT_PLUS:
            a = node.left_child
            b = node.right_child
            if a.lexical_token == LexicalToken(TT_INT, 0):
                return b
            elif b.lexical_token == LexicalToken(TT_INT, 0):
                return a

        elif lex == TT_MINUS:
            a = node.left_child
            b = node.right_child
            if b.lexical_token == LexicalToken(TT_INT, 0):
                return a

        elif lex == TT_DIVIDE:
            a = node.left_child
            b = node.right_child
            if b.lexical_token == LexicalToken(TT_INT, 1):
                return a

        elif lex == TT_FUNC:
            return node.lexical_token.value.fold(node)

        return node

    @staticmethod
    def __fold(node, prev_node, left):
        if node:

            if isinstance(node, BinaryNode):
                Expression.__fold(node.left_child, node, 1)

            if prev_node and node:
                if left:
                    prev_node.left_child = Expression.__fold_node(node)
                else:
                    prev_node.right_child = Expression.__fold_node(node)

            if isinstance(node, UnaryNode) or isinstance(node, BinaryNode):
                Expression.__fold(node.right_child, node, 0)

            if isinstance(node, UnaryNode) or isinstance(node, BinaryNode):
                prev_node = node

        return node

    @staticmethod
    def fold(node):
        prev_node = node
        for _ in range(5):
            node = Expression.__fold(prev_node, None, 0)
            node = Expression.__fold_node(node)
            prev_node = node
        return prev_node

    @staticmethod
    def __differentiate(node, wrt):

        lex = node.lexical_token

        # d(u + v) / dx = du / dx + dv / dx
        if lex == TT_PLUS:
            u = node.left_child
            v = node.right_child
            du = Expression.__differentiate(u, wrt)
            dv = Expression.__differentiate(v, wrt)
            return BinaryNode(LexicalToken(TT_PLUS), du, dv)

        # d(u - v) / dx = du / dx - dv / dx
        elif lex == TT_MINUS:
            u = node.left_child
            v = node.right_child
            du = Expression.__differentiate(u, wrt)
            dv = Expression.__differentiate(v, wrt)
            return BinaryNode(LexicalToken(TT_MINUS), du, dv)

        # d(uv) / dx = v * du / dx + u * dv / dx
        elif lex == TT_MULTIPLY:
            u = node.left_child
            v = node.right_child

            if u.lexical_token == TT_INT:
                return BinaryNode(LexicalToken(TT_MULTIPLY), u, Expression.__differentiate(v, wrt))

            if v.lexical_token == TT_INT:
                return BinaryNode(LexicalToken(TT_MULTIPLY), v, Expression.__differentiate(u, wrt))

            v_du = BinaryNode(LexicalToken(TT_MULTIPLY), v, Expression.__differentiate(u, wrt))
            u_dv = BinaryNode(LexicalToken(TT_MULTIPLY), u, Expression.__differentiate(v, wrt))
            return BinaryNode(LexicalToken(TT_PLUS), v_du, u_dv)

        # d(u / v) / dx = v * du - u * dv / v ^ 2
        elif lex == TT_DIVIDE:
            u = node.left_child
            v = node.right_child
            v_du = BinaryNode(LexicalToken(TT_MULTIPLY), v, Expression.__differentiate(u, wrt))
            u_dv = BinaryNode(LexicalToken(TT_MULTIPLY), u, Expression.__differentiate(v, wrt))
            numerator = BinaryNode(LexicalToken(TT_MINUS), v_du, u_dv)
            denominator = BinaryNode(LexicalToken(TT_EXPONENT), v, Node(LexicalToken(TT_INT, 2)))
            return BinaryNode(LexicalToken(TT_DIVIDE), numerator, denominator)

        # d(u ^ c) / dx =  c * u ^ (c - 1) * du / dx
        elif lex == TT_EXPONENT:
            u = node.left_child
            c = node.right_child

            # d(a ^ u) / dx = a ^ u * log(a) * du / dx
            if u.lexical_token == TT_INT or u.lexical_token == TT_REAL:
                a_u = BinaryNode(LexicalToken(TT_EXPONENT), u, c)
                log_a = BinaryNode(LexicalToken(TT_FUNC, LOG), Node(LexicalToken(TT_REAL, NumericalConstants.get_constant('e'))), u)
                a_u_log_a = BinaryNode(LexicalToken(TT_MULTIPLY), a_u, log_a)
                du = Expression.__differentiate(c, wrt)
                return BinaryNode(LexicalToken(TT_MULTIPLY), a_u_log_a, du)

            # d(u ^ c) / dx =  c * u ^ (c - 1) * du / dx
            elif c.lexical_token == TT_INT or c.lexical_token == TT_REAL or c.lexical_token == TT_SYMBOL:
                if c.lexical_token == wrt:
                    return node

                if c.lexical_token == TT_SYMBOL:
                    u_c_1 = BinaryNode(LexicalToken(TT_EXPONENT), u, Node(LexicalToken(TT_INT, str(c.lexical_token.value) + "-1")))
                else:
                    u_c_1 = BinaryNode(LexicalToken(TT_EXPONENT), u, Node(LexicalToken(TT_INT, c.lexical_token.value - 1)))

                c_u_c_1 = BinaryNode(LexicalToken(TT_MULTIPLY), c, u_c_1)
                du = Expression.__differentiate(u, wrt)
                return BinaryNode(LexicalToken(TT_MULTIPLY), c_u_c_1, du)

            else:
                sys.exit(0)

        elif lex == TT_FUNC:
            du = Expression.__differentiate(node.right_child, wrt)
            res = lex.value.derivative(node)
            res.right_child = du
            return res

        # d(c) / dx = 0
        elif lex in [TT_INT, TT_REAL]:
            return Node(LexicalToken(TT_INT, 0))

        # d(v) / dx = 1 (v : variable)
        elif lex == TT_SYMBOL:
            # d(x) / dx = 1
            if lex == wrt:
                return Node(LexicalToken(TT_INT, 1))

            # d(v) / dx = 0 (v : variable other than x)
            else:
                return Node(LexicalToken(TT_INT, 0))

    @staticmethod
    def differentiate(expression: "Expression", wrt: LexicalToken = LexicalToken(TT_SYMBOL, 'x'),
                      nth_derivative: int = 1, fold: bool = True):
        head = expression.head_node
        for _ in range(nth_derivative):
            head = Expression.__differentiate(head, wrt)
            if fold:
                head = Expression.fold(head)

        return Expression.from_nodes(head)
