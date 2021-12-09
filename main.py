from delta import Expression
ex = Expression("log 10(x)")
print(Expression.differentiate(ex, nth_derivative=1))
