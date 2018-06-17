#!/usr/bin/env python

from functools import reduce
from constant import *
from lookup_table import *

def is_prime(n):
    if n == 1:
        return False
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def factorization(n):
    prime_factor_list = []
    while not n % 2:
        prime_factor_list.append(2)
        n //= 2
    while not n % 3:
        prime_factor_list.append(3)
        n //= 3
    i = 5
    while n != 1:
        if is_prime(i):
            while not n % i:
                prime_factor_list.append(i)
                n //= i
        i += 2

    return prime_factor_list
# factorization(31752) = 2^3 * 3^4 * 7^2
### END

def test():
    array = [[]] * 2
    arr1 = [1, 2, 3]
    arr2 = [4, 5, 6]

    arr1 += [8, 9]
    arr1.append([10, 2])
    print arr1

if __name__ == "__main__":
    test()





