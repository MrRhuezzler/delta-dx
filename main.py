from delta.expr.expression import Expression

l = Expression('log 10(cos(5 * x))')
print(Expression.differentiate(l))
