from differentiator.expr.expression import Expression
from differentiator.parser.nodes import Node, BinaryNode, UnaryNode
from differentiator.lexer.lexicalToken import LexicalToken
from differentiator.lexer.tokens import *
from differentiator.lexer.mathFunctions import *

# f(x) = x * e ^ x * log(x)
log_x = BinaryNode(LexicalToken(TT_FUNC, LOG), Node(LexicalToken(TT_REAL, 'e')), Node(LexicalToken(TT_SYMBOL, 'x')))
e_x = BinaryNode(LexicalToken(TT_EXPONENT), Node(LexicalToken(TT_REAL, 'e')), Node(LexicalToken(TT_SYMBOL, 'x')))
e_x_log_x = BinaryNode(LexicalToken(TT_MULTIPLY), e_x, log_x)
head = BinaryNode(LexicalToken(TT_MULTIPLY), Node(LexicalToken(TT_SYMBOL, 'x')), e_x_log_x)

equation = Expression.from_nodes(head)
# folded = Expression.fold(head)
# derivative = Expression.differentiate(equation, nth_derivative=5, fold=False)
derivative_2 = Expression.differentiate(equation, nth_derivative=5, fold=True)
print("Given : ", equation)
# print("Folded Equation : ", folded)
# print("Un Folded Derivative : ", derivative)
print("Folded Derivative : ", derivative_2)
