![delta-dx](https://github.com/MrRhuezzler/delta-dx/blob/main/images/d_cover.png)
---
[![Publish to PyPI](https://github.com/MrRhuezzler/delta/actions/workflows/python-publish.yml/badge.svg)](https://github.com/MrRhuezzler/delta/actions/workflows/python-publish.yml)
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
