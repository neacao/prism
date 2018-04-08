#!/usr/bin/env python

from functools import reduce

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


# @timeit
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

def supp(n):
    return len(prime_factor(n))

# Multiplication block encoding
def v(array):
    return reduce((lambda x,y: x * y), array)

# 14 = 1001 - 30 = 1110
def inverse_v(n):
    ret = [0, 0, 0, 0]
    ret[0] = 1 if n % 2 == 0 else 0
    ret[1] = 1 if n % 3 == 0 else 0
    ret[2] = 1 if n % 5 == 0 else 0
    ret[3] = 1 if n % 7 == 0 else 0
    return ret


def gcd(a,b):
    if(b==0):
        return a
    else:
        return gcd(b,a%b)
