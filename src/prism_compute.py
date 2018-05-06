#!/usr/bin/env python

from lookup_table import *

# BITs is counting from right to left
def computeBitValueOfPrimalValue(value):
	rankValue = computeRankOfPrimalValue(value)
	return RANK_BITS[rankValue]


def computePrimalValueOfBitValue(value):
	value = 1
	if (value & 0x80): value *= 2
	if (value & 0x40): value *= 3
	if (value & 0x20): value *= 5
	if (value & 0x10): value *= 7
	if (value & 0x08): value *= 11
	if (value & 0x04): value *= 13
	if (value & 0x02): value *= 17
	if (value & 0x01): value *= 19
	return value


def computeMaskValueOfPrimalValue(value):
	rank = computeRankOfPrimalValue(value)
	rank_mask = RANK_MASK[rank]
	result = RANK_VALUE[rank_mask]
	return result


def computeGCDOfPrimalsValue(value, target):
	valueRank = computeRankOfPrimalValue(value)
	targetRank = computeRankOfPrimalValue(target)
	rankGCD = RANK_GCD[valueRank][targetRank]
	result = RANK_VALUE[rankGCD]
	return 


def computeRankOfPrimalValue(value):
	try:
		_index = RANK_VALUE.index(value)
		return _index

	except ValueError:
		print "Not found Rank of this:", value
		return 0


def test():
	print computeMaskValueOfPrimalValue(35)
	return 

if __name__ == "__main__":
	test()