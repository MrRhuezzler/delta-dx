class NumericalConstants:
    constants = []

    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value
        NumericalConstants.constants.append(self)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.symbol == other
        return False

    @staticmethod
    def get_constant(symbol):
        for constant in NumericalConstants.constants:
            if constant == symbol:
                return constant
        return None


class SymbolicConstants:
    constants = []

    def __init__(self, symbol):
        self.symbol = symbol
        SymbolicConstants.constants.append(self)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.symbol == other
        return False

    @staticmethod
    def get_constant(symbol):
        for constant in SymbolicConstants.constants:
            if constant == symbol:
                return constant
        return None
