from delta.lexer.lexer import Lexer
from delta.parser.parser import Parser

# f(x) = x ^ n
# head = BinaryNode(LexicalToken(TT_EXPONENT), Node(LexicalToken(TT_SYMBOL, 'x')), Node(LexicalToken(TT_SYMBOL, 'n')))

# f(x) = x * e ^ x * log(x)
# log_x = BinaryNode(LexicalToken(TT_FUNC, LOG), Node(LexicalToken(TT_REAL, 'e')), Node(LexicalToken(TT_SYMBOL, 'x')))
# e_x = BinaryNode(LexicalToken(TT_EXPONENT), Node(LexicalToken(TT_REAL, 'e')), Node(LexicalToken(TT_SYMBOL, 'x')))
# e_x_log_x = BinaryNode(LexicalToken(TT_MULTIPLY), e_x, log_x)
# head = BinaryNode(LexicalToken(TT_MULTIPLY), Node(LexicalToken(TT_SYMBOL, 'x')), e_x_log_x)

la = Lexer("(x * e ^ x) * (ln {5} + sin{7 * y})")
lb = Lexer("(x * e ^ x) * (log 5 {5} + sin{7 * y}) * cos{9 * u}")
pa = Parser(la.make_tokens())
pb = Parser(lb.make_tokens())
print(pa.make_nodes())
print(pb.make_nodes())
