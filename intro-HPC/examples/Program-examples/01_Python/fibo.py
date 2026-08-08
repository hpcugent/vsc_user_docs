#! /usr/bin/env python

"""
Fibonacci numbers module.
The Fibonacci sequence starts with
 0, 1, 1, 2, 3, 5, 8, 13, 21.
"""

import sys


def fib(n):
    """Write Fibonacci series up to n"""
    a, b = 0, 1
    while b < n:
        print(f"{b} ", end="")
        a, b = b, a + b


#         print(f"{a} {b}\n")


def fib2(n):
    """Return Fibonacci series up to n as an array"""
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a + b
    return result


if __name__ == "__main__":
    fib(int(sys.argv[1]))
