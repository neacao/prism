#!/usr/bin/env python

from lookup_table import *
from constant import *

# BITs is counting from right to left
# computeBitValueOfPrimalValue(30) = 224 = 11100000
def computeBitValueOfPrimalValue(value):
	rankValue = computeRankOfPrimalValue(value)
	return RANK_BITS[rankValue]


# computePrimalValueOfBitValue(224) = 30
def computePrimalValueOfBitValue(value):
	result = 1
	if (value & 0x80): result *= 2
	if (value & 0x40): result *= 3
	if (value & 0x20): result *= 5
	if (value & 0x10): result *= 7
	if (value & 0x08): result *= 11
	if (value & 0x04): result *= 13
	if (value & 0x02): result *= 17
	if (value & 0x01): result *= 19
	return result


# computeSupportOfPrimalValue(30) = 3
def computeSupportOfPrimalValue(value):
	rankValue = computeRankOfPrimalValue(value)
	result = RANK_SUPPORT[rankValue]
	return result


def computeSupportOfPrimalValueArray(array):
	result = 0
	for element in array:
			if element > 1:
				result += computeSupportOfPrimalValue(element)
	return result


# computeMaskValueOfPrimalValue(30) = 4849845
def computeMaskValueOfPrimalValue(value):
	rank = computeRankOfPrimalValue(value)
	raskMask = RANK_MASK[rank]
	result = RANK_VALUE[raskMask]
	return result


# computeGCDOfPrimalsValue(30, 6) = 6
def computeGCDOfPrimalsValue(value, target):
	valueRank = computeRankOfPrimalValue(value)
	targetRank = computeRankOfPrimalValue(target)
	rankGCD = RANK_GCD[valueRank][targetRank]
	result = RANK_VALUE[rankGCD]
	return result

# computeRankOfPrimalValue(30) = 7
def computeRankOfPrimalValue(value):
	try:
		_index = RANK_VALUE.index(value)
		return _index

	except ValueError:
		print("==> Not found Rank of this: {0}".format(value))
		return 0


def findNumberDivisible(currentNumber, target):
  for number in range(currentNumber, currentNumber + target):
      if number % target == 0:
        return number if number >= G_LENGTH_ADVANCE else G_LENGTH_ADVANCE
  return 0
# findNumberDivisible(7, 5) -> 10


def inverseMultiplyBitEncodingAdv(number):
    ret = [0] * G_LENGTH_ADVANCE
    for index in range(0, G_LENGTH_ADVANCE):
    	ret[index] = 1 if number % G_ARRAY_ADVANCE[index] == 0 else 0
    return ret


def maxRankValue():
	return RANK_VALUE[-1]

def test():
	# #print computeBitValueOfPrimalValue(30) # Must equal 224
	# #print computePrimalValueOfBitValue(224) # Must equal 30
	# #print computeGCDOfPrimalsValue(30, 6) # Must equal 6
	# #print computeSupportOfPrimalValue(30) # Must equal 3 
	# #print computeMaskValueOfPrimalValue(30) # Must equal 4849845
	return 1

if __name__ == "__main__":
	test()