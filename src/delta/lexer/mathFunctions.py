import math

from delta.lexer.constants import NumericalConstants

from .function import Function
from delta.parser.nodes import Node, BinaryNode, UnaryNode
from delta.lexer.lexicalToken import LexicalToken
from delta.lexer.tokens import *


# d(log(a, u)) / dx = (1 / (log(a) * u)) * du / dx
def log_d(node):
    a = node.left_child
    u = node.right_child
    log_a = BinaryNode(LexicalToken(TT_FUNC, LOG), Node(LexicalToken(TT_REAL, NumericalConstants.get_constant('e'))), a)
    log_a_u = BinaryNode(LexicalToken(TT_MULTIPLY), log_a, u)
    _1_log_a_u = BinaryNode(LexicalToken(TT_DIVIDE), Node(LexicalToken(TT_INT, 1)), log_a_u)
    return BinaryNode(LexicalToken(TT_MULTIPLY), _1_log_a_u)


# d(sqrt(u)) / dx = (1 / 2 * sqrt(u)) * du / dx
def sqrt_d(node):
    u = node.right_child
    sqrt_u = UnaryNode(LexicalToken(TT_FUNC, SQRT), u)
    _2_sqrt_u = BinaryNode(LexicalToken(TT_MULTIPLY), Node(LexicalToken(TT_INT, 2)), sqrt_u)
    _1_2_sqrt_u = BinaryNode(LexicalToken(TT_DIVIDE), Node(LexicalToken(TT_INT, 1)), _2_sqrt_u)
    return BinaryNode(LexicalToken(TT_MULTIPLY), _1_2_sqrt_u)


# d(sin u) / dx = cos u * du / dx
def sin_d(node):
    u = node.right_child
    cos_u = UnaryNode(LexicalToken(TT_FUNC, COS), u)
    return BinaryNode(LexicalToken(TT_MULTIPLY), cos_u)


# d(cos u) / dx = (0 - sin u) * du / dx
def cos_d(node):
    u = node.right_child
    sin_u = UnaryNode(LexicalToken(TT_FUNC, SIN), u)
    _sin_u = BinaryNode(LexicalToken(TT_MINUS), Node(LexicalToken(TT_INT, 0)), sin_u)
    return BinaryNode(LexicalToken(TT_MULTIPLY), _sin_u)


# d(tan u) / dx =  sec ^ 2 (u) * du / dx
def tan_d(node):
    u = node.right_child
    sec_u = UnaryNode(LexicalToken(TT_FUNC, SEC), u)
    sec_2_u = BinaryNode(LexicalToken(TT_EXPONENT), sec_u, Node(LexicalToken(TT_INT, 2)))
    return BinaryNode(LexicalToken(TT_MULTIPLY), sec_2_u)


# d(sec u) / dx = sec u * tan u * du / dx
def sec_d(node):
    u = node.right_child
    sec_u = UnaryNode(LexicalToken(TT_FUNC, SEC), u)
    tan_u = UnaryNode(LexicalToken(TT_FUNC, TAN), u)
    sec_u_tan_u = BinaryNode(LexicalToken(TT_MULTIPLY), sec_u, tan_u)
    return BinaryNode(LexicalToken(TT_MULTIPLY), sec_u_tan_u)


# d(cosec u) / dx = (0 - cosec u) * cot u * du / dx
def cosec_d(node):
    u = node.right_child
    cosec_u = UnaryNode(LexicalToken(TT_FUNC, COSEC), u)
    _cosec_u = BinaryNode(LexicalToken(TT_MINUS), Node(LexicalToken(TT_INT, 0)), cosec_u)
    cot_u = UnaryNode(LexicalToken(TT_FUNC, COT), u)
    _cosec_u_cot_u = BinaryNode(LexicalToken(TT_MULTIPLY), _cosec_u, cot_u)
    return BinaryNode(LexicalToken(TT_MULTIPLY), _cosec_u_cot_u)


# d(cot u) / dx = ( 0 - cosec ^ 2 (u)) * du / dx
def cot_d(node):
    u = node.right_child
    cosec_u = UnaryNode(LexicalToken(TT_FUNC, COSEC), u)
    cosec_2_u = BinaryNode(LexicalToken(TT_EXPONENT), cosec_u, Node(LexicalToken(TT_INT, 2)))
    _cosec_2_u = BinaryNode(LexicalToken(TT_MINUS), Node(LexicalToken(TT_INT, 0)), cosec_2_u)
    return BinaryNode(LexicalToken(TT_MULTIPLY), _cosec_2_u)


# d(arcsin u) / dx = (1 / sqrt(1 - u ^ 2)) * du / dx
def arcsin_d(node):
    u = node.right_child
    u_2 = BinaryNode(LexicalToken(TT_EXPONENT), u, Node(LexicalToken(TT_INT, 2)))
    _1_u_2 = BinaryNode(LexicalToken(TT_MINUS), Node(LexicalToken(TT_INT, 1)), u_2)
    sqrt_v = UnaryNode(LexicalToken(TT_FUNC, SQRT), _1_u_2)
    _1_sqrt_v = BinaryNode(LexicalToken(TT_DIVIDE), Node(LexicalToken(TT_INT, 1)), sqrt_v)
    return BinaryNode(LexicalToken(TT_MULTIPLY), _1_sqrt_v)


# d(arccos u) / dx = (0 - (1 / sqrt(1 - u ^ 2))) * du / dx
def arccos_d(node):
    u = node.right_child
    u_2 = BinaryNode(LexicalToken(TT_EXPONENT), u, Node(LexicalToken(TT_INT, 2)))
    _1_u_2 = BinaryNode(LexicalToken(TT_MINUS), Node(LexicalToken(TT_INT, 1)), u_2)
    sqrt_v = UnaryNode(LexicalToken(TT_FUNC, SQRT), _1_u_2)
    _1_sqrt_v = BinaryNode(LexicalToken(TT_DIVIDE), Node(LexicalToken(TT_INT, 1)), sqrt_v)
    __1_sqrt_v = BinaryNode(LexicalToken(TT_MINUS), Node(LexicalToken(TT_INT, 0)), _1_sqrt_v)
    return BinaryNode(LexicalToken(TT_MULTIPLY), __1_sqrt_v)


# d(arctan u) / dx = (1 / (1 + u ^ 2)) * du / dx
def arctan_d(node):
    u = node.right_child
    u_2 = BinaryNode(LexicalToken(TT_EXPONENT), u, Node(LexicalToken(TT_INT, 2)))
    _1_u_2 = BinaryNode(LexicalToken(TT_PLUS), Node(LexicalToken(TT_INT, 1)), u_2)
    _1_v = BinaryNode(LexicalToken(TT_DIVIDE), Node(LexicalToken(TT_INT, 1)), _1_u_2)
    return BinaryNode(LexicalToken(TT_MULTIPLY), _1_v)


# d(arcsec u) / dx = (1 / u * sqrt(u ^ 2 - 1)) * du / dx
def arcsec_d(node):
    u = node.right_child
    u_2 = BinaryNode(LexicalToken(TT_EXPONENT), u, Node(LexicalToken(TT_INT, 2)))
    u_2_1 = BinaryNode(LexicalToken(TT_MINUS), u_2, Node(LexicalToken(TT_INT, 1)))
    u_u_2_1 = BinaryNode(LexicalToken(TT_MULTIPLY), u, u_2_1)
    _1_v = BinaryNode(LexicalToken(TT_DIVIDE), Node(LexicalToken(TT_INT, 1)), u_u_2_1)
    return BinaryNode(LexicalToken(TT_MULTIPLY), _1_v)


# d(arccosec u) / dx = (0 - (1 / u * sqrt(u ^ 2 - 1))) * du / dx
def arccosec_d(node):
    u = node.right_child
    u_2 = BinaryNode(LexicalToken(TT_EXPONENT), u, Node(LexicalToken(TT_INT, 2)))
    u_2_1 = BinaryNode(LexicalToken(TT_MINUS), u_2, Node(LexicalToken(TT_INT, 1)))
    u_u_2_1 = BinaryNode(LexicalToken(TT_MULTIPLY), u, u_2_1)
    _1_v = BinaryNode(LexicalToken(TT_DIVIDE), Node(LexicalToken(TT_INT, 1)), u_u_2_1)
    __1_v = BinaryNode(LexicalToken(TT_MINUS), Node(LexicalToken(TT_INT, 0)), _1_v)
    return BinaryNode(LexicalToken(TT_MULTIPLY), __1_v)


# d(arccot u) / dx = (0 - (1 / (1 + u ^ 2))) * du / dx
def arccot_d(node):
    u = node.right_child
    u_2 = BinaryNode(LexicalToken(TT_EXPONENT), Node(LexicalToken(TT_INT, 2)), u)
    _1_u_2 = BinaryNode(LexicalToken(TT_PLUS), Node(LexicalToken(TT_INT, 1)), u_2)
    _1_v = BinaryNode(LexicalToken(TT_DIVIDE), Node(LexicalToken(TT_INT, 1)), _1_u_2)
    __1_v = BinaryNode(LexicalToken(TT_MINUS), Node(LexicalToken(TT_INT, 0)), _1_v)
    return BinaryNode(LexicalToken(TT_MULTIPLY), __1_v)


def log_f(node):
    a = node.left_child
    b = node.right_child
    if a.lexical_token == b.lexical_token:
        return Node(LexicalToken(TT_INT, 1))

    return node


def sqrt_f(node):
    a = node.right_child
    if a.lexical_token == TT_INT or a.lexical_token == TT_REAL:
        val = a.lexical_token.value
        if a.lexical_token == LexicalToken(TT_REAL, 'e'):
            val = math.e
        return Node(LexicalToken(TT_REAL, pow(val, 0.5)))

    return node


LOG = Function('log', log_d, log_f, 1)

SQRT = Function('sqrt', sqrt_d, sqrt_f)

COS = Function('cos', cos_d)
SIN = Function('sin', sin_d)
TAN = Function('tan', tan_d)
SEC = Function('sec', sec_d)
COSEC = Function('cosec', cosec_d)
COT = Function('cot', cot_d)

ARCSIN = Function('arcsin', arcsin_d)
ARCCOS = Function('arccos', arccos_d)
ARCTAN = Function('arctan', arctan_d)
ARCSEC = Function('arcsec', arcsec_d)
ARCCOSEC = Function('arccosec', arccosec_d)
ARCCOT = Function('arccot', arccot_d)
