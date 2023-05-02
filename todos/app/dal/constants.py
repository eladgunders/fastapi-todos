from typing import Final


MAX_POSTGRES_INTEGER: Final[int] = (2 ** 31) - 1
"""
maximum value that can be represented by a 32-bit signed integer.
if trying to send a bigger value than that in queries (like offset or limit)
the database throws an error - OverflowError: value out of int32 range
"""
GET_MULTI_DEFAULT_SKIP: Final[int] = 0
GET_MULTI_DEFAULT_LIMIT: Final[int] = 100
