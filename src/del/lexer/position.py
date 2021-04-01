class Position:
    def __init__(self, idx):
        self.idx = idx

    def advance(self):
        self.idx += 1

    @staticmethod
    def copy(other):
        if isinstance(other, Position):
            return Position(other.idx)
        return None
