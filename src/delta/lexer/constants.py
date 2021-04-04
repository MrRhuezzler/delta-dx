import math


class NumericalConstants:
    constants = []

    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value
        NumericalConstants.constants.append(self)

    def __repr__(self) -> str:
        return f"{self.symbol}"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.symbol == other
        if isinstance(other, NumericalConstants):
            return self.symbol == other.symbol
            
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

    def __repr__(self) -> str:
        return f"{self.symbol}"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.symbol == other
        if isinstance(other, SymbolicConstants):
            return self.symbol == other.symbol
            
        return False

    @staticmethod
    def get_constant(symbol):
        for constant in SymbolicConstants.constants:
            if constant == symbol:
                return constant
        return None


e = NumericalConstants('e', math.e)
pi = NumericalConstants('pi', math.pi)
tau = NumericalConstants('ta', math.tau)

x = SymbolicConstants('x')
y = SymbolicConstants('y')
z = SymbolicConstants('z')
w = SymbolicConstants('w')
v = SymbolicConstants('v')
u = SymbolicConstants('u')
n = SymbolicConstants('n')
