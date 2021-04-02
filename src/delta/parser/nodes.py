from delta.lexer.lexicalToken import LexicalToken


class Node:
    def __init__(self, lexical_token: LexicalToken):
        self.lexical_token = lexical_token

    def __str__(self):
        return str(self.lexical_token)

    def __repr__(self):
        return f"{self.lexical_token}"


class BinaryNode(Node):
    def __init__(self, lexical_token: LexicalToken, left_child: Node = None, right_child: Node = None):
        super().__init__(lexical_token)
        self.left_child = left_child
        self.right_child = right_child


class UnaryNode(Node):
    def __init__(self, lexical_token: LexicalToken, right_child: Node = None):
        super().__init__(lexical_token)
        self.right_child = right_child
