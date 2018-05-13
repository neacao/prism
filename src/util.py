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


def countingSupport(primalSeq):
    result = 0
    for element in primalSeq:
        result += COUNTING_SUPPORT_ARRAY[element]
    return result


def multiplyPrimalEncoding(array):
    return reduce((lambda x,y: x * y), array)
# multiplyBlockEncoding: [2, 3, 7] = 42



def multiplyBitEncoding(array):
    result = 1
    # Using G_LENGTH = 4 for testing purpose
    if array[0] == 1: result *= 2
    if array[1] == 1: result *= 3
    if array[2] == 1: result *= 5
    if array[3] == 1: result *= 7
    return result
# multiplyBitEncoding([1, 1, 0, 1]) = 42 


# Support up to     
def inverseMultiplyBitEncoding(number):
    ret = [0, 0, 0, 0]
    ret[0] = 1 if number % 2 == 0 else 0
    ret[1] = 1 if number % 3 == 0 else 0
    ret[2] = 1 if number % 5 == 0 else 0
    ret[3] = 1 if number % 7 == 0 else 0
    return ret
# inverseMultiplyBlockEncoding(42) = [1, 1, 0, 1]

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


# Support block-size equal 4 (up to 210) only
def maskPrimalPosition(primalPos):
    bitEncodedArray = list(map(lambda number: inverseMultiplyBitEncoding(number), primalPos))

    # TODO: Improve this
    result = []
    for index in xrange(0, len(bitEncodedArray)):
        bitEncoded = bitEncodedArray[index]
        try:
            firstPos = bitEncoded.index(1)
            result.append(G_ARRAY_MASK[firstPos])

            for restList in bitEncodedArray[index+1:]:
                result.append( G_ARRAY_MULTIPLE )
            return result

        except ValueError:
            result.append(1)
    return result


def maskPrimalEncodedBetter(number):
    return 1


def gcd(a,b):
    return a if b == 0 else gcd(b,a%b)
# --- gcd: gcd(18,9) = 9


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





