from delta import Expression
ex = Expression("sin(x ^ 3) + cos(x)")
print(Expression.differentiate(ex, nth_derivative=1))
