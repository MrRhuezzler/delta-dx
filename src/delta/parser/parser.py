class Parser:
    def __init__(self, lexical_tokens: list):
        self.tokens = lexical_tokens
        self.head = None

    def make_nodes(self):
        return self.head
