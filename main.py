from delta.expr.expression import Expression

e = Expression("ln {5 * x}")
e_d = Expression.differentiate(e)
print("f(x) = ", e)
print("f'(x) = ", e_d)