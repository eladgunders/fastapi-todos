from typing import Final


MAX_LIMIT_GET_MULTI: Final[int] = (2 ** 31) - 1
"""
maximum value that can be represented by a 32-bit signed integer.
it is the postgresql maximum get multi query limit == no limit.
"""
GET_MULTI_DEFAULT_SKIP: Final[int] = 0
GET_MULTI_DEFAULT_LIMIT: Final[int] = 100