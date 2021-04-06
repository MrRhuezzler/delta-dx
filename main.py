from delta import Expression
ex = Expression("x * e ^ x")
print(Expression.differentiate(ex, nth_derivative=1))
