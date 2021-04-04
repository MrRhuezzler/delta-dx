from typing import Callable


class Function:
    functions = []

    def __init__(self, function_name: str, derivative_func: Callable, fold_func: Callable = lambda x: x, isbinary: int = 0):
        self.function_name = function_name
        self.derivative_func = derivative_func
        self.fold_func = fold_func
        self.isbinary = isbinary
        Function.functions.append(self)

    def derivative(self, node):
        return self.derivative_func(node)

    def fold(self, node):
        return self.fold_func(node)

    def __repr__(self):
        return f"{self.function_name}"

    @staticmethod
    def get_function(function_name: str):
        for function in Function.functions:
            if function.function_name == function_name:
                return function

        return None
