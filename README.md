![delta-dx](https://github.com/MrRhuezzler/delta-dx/blob/main/images/d_cover.png)
---
[![PYPI Version](https://img.shields.io/pypi/v/delta-dx.svg)](https://pypi.org/project/delta-dx/)
[![Publish to PYPI](https://github.com/MrRhuezzler/delta/actions/workflows/python-publish.yml/badge.svg)](https://github.com/MrRhuezzler/delta/actions/workflows/python-publish.yml)
[![Run Python Tests](https://github.com/MrRhuezzler/delta/actions/workflows/pytest_actions.yml/badge.svg)](https://github.com/MrRhuezzler/delta/actions/workflows/pytest_actions.yml)  

Author           : [MrRhuezzler](https://github.com/MrRhuezzler)  
Project Language : Python  
Project Year     : 2021  

## How to Install
This currently avaiable on [PYPI](https://pypi.org/project/delta-dx/), from where it can be installed  using the following command.  
(Note : pip and python must be added to the PATH for this command to work)
```
pip install delta-dx
```
## Usage

```python
from delta import Expression
expression = Expression("x * e ^ x")
print(Expression.differentiate(expression, nth_derivative=1))
```

## Approach

This Project uses all the basic rules of Mathematical Differentiation and converts them into a computer algorithm, which provides the power to differentiate various equations. One main advantage of this project is that it can differentiate between variables ( x, y, z, w, u, v ) and numbers (5, 0.56, e, pi, tau ).

Thinking of devising an algorithm to handle such a task is the goal, luckily Dynamic Programming can be used to devise such an algorithm. Let's take an example to explain.

```
Example:

d(sin(2x)) / dx = cos(2x) * 2
```

In the equation sin(2x), first we differentiate based on the rule d(sin(u)) / dx =cos(u) and then followed by differentiating u = 2x based on the rule d(cv) / dx = c dv/dx we get 2. 

From the above example, we can see that the process of differentiating sin(2x)is being broken down to first differentiating the outer sin(u) function and differentiating the inner 2x function and then combining both results to get the answer to the given problem.

The Next major problem is that, how is an equation being represented in the computer algorithm. To Tackle this problem, we have to see the various ways that an expression can be expressed. They are infix, prefix, postfix notations.
```
Example:

(a+b) * (c + d) - Infix
*+ab+cd         - Prefix
ab+cd+*         - Postfix
```
Given the input expression, it can be converted to the prefix notation, with can be easily converted into a prefix expression tree, which can be used as an input to the algorithm and also devise the algorithm in such a way that it outputs a prefix expression tree, which makes it complete cycle (Enabling the algorithm to find multiorder derivatives).
```
Example:

log 10(cos(5 * x))

Expression Tree :

        log
      /     \
    10        cos
                \ 
                 *
                /  \ 
              5     x

```
By traversing the tree layer by layer and calling the algorithm, to solve for each layer, the problem of differentiating becomes a lot simpler. Let's take an example of differentiating a mathematical expression.

```
Example:

sin(2*x)

Expression Tree

    sin
      |
      *
    /   \
  2       x
```
```
-> differentiate(sin) // Calling the algorithm to solve
-> if input == sin // If the given head node of the tree represents sin function
->    cos = cos // Creating a node representing cos function
->    cos.child = input.child // Assigning the input for cos function
->     multiply = * // Creating a multiplication node
->    multiply.left = cos
->    multiply.right = differentiate(input.child) // Recursively calling the algorithm to solve for 2*x
->      return multiply // returning the result
-> if input == * // If the input is a multiplication operation
->     // Statements to handle this case and return the result.
-> done
```
Now we are done with the differentiating algorithm.

The Next steps may be to simplify the output of the differentiating algorithm, so that it looks neat and simple, rather than having more additional terms in the final output expression. Such an expression folding algorithm is also implemented to fold into smaller expressions. And with some basic mathematics an algorithm was devised. It is not the most optimal solution for the problem. I learnt many things in making this package.

## Resources
- [The D* Symbolic Differentiation Algorithm](https://www.microsoft.com/en-us/research/publication/the-d-symbolic-differentiation-algorithm/) | Author : [Brian Guenter](https://www.microsoft.com/en-us/research/people/bguenter/) | Year : 2007
- [A Webpage of the University of Texas at Austin](https://www.cs.utexas.edu/users/novak/asg-symdif.html) (Primary Inspiration for developing this package)
- [A Webpage of MIT Press](https://mitpress.mit.edu/sites/default/files/sicp/full-text/sicp/book/node39.html) (Served as a quick reference material)
