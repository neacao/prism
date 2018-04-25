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
# --- Factorization: 31752 = 2^3 * 3^4 * 7^2

# Prerequiste: Calculate only sequence primal encoded
def supp(number):
    return len(set(factorization(number)))
# --- Min support: 2^3 * 3^4 * 7^2 = 3


def multiplyBlockEncoding(array):
    return reduce((lambda x,y: x * y), array)
# --- multiplyBlockEncoding: [2, 3, 7] = 42

def maskBitEncoded(array):
    flag = False
    for i in xrange(0, len(array), 1):
        if flag == True:
            array[i] = 1
        elif array[i] == 1:
            flag = True
            array[i] = 0

    return array
# --- maskBlockEncoding: [0, 1, 0, 0] = [0, 0, 1, 1]


def maskPrimalEncoded(number):
    
    return 1

def inverseMultiplyBlockEncoding(n):
    ret = [0, 0, 0, 0]
    ret[0] = 1 if n % 2 == 0 else 0
    ret[1] = 1 if n % 3 == 0 else 0
    ret[2] = 1 if n % 5 == 0 else 0
    ret[3] = 1 if n % 7 == 0 else 0
    return ret
# --- inverseMultiplyBlockEncoding: 42 = [1, 1, 0, 1]


def gcd(a,b):
    if(b==0):
        return a
    else:
        return gcd(b,a%b)
# --- gcd: gcd(18,9) = 9


def findNumberDivisible(currentNumber, target):
    for number in xrange(currentNumber, currentNumber + target):
        if number % target == 0:
            return number
    return 0
# findNumberDivisible(7, 5) -> 10









