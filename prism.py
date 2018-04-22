#!/usr/bin/env python

from util import *
from constant import *

# Give a list of itemset and encode primal position match with key
# - Array should be list of String
def encodeBitPosition(key, array):
	result = []
	for element in array:
		index = element.find(key)
		if index != -1:
			result.append(1)
		else:
			result.append(0)

	length = len(result)
	for length in xrange(length, 8):
		result.append(0)
	return result


def encodePrimalPosition(key, array):
	bitEncodedPos = encodeBitPosition(key, array)
	result = []
	length = len(bitEncodedPos)

	for blockIndex in xrange(0, length/4):
		index = blockIndex * 4
		tmp = 1
		
		if bitEncodedPos[index] == 1: tmp *= 2
		if bitEncodedPos[index + 1] == 1: tmp *= 3
		if bitEncodedPos[index + 2] == 1: tmp *= 5
		if bitEncodedPos[index + 3] == 1: tmp *= 7

		result.append(tmp)

	return result


def encodePrimalSequence(key, sequence): # Sequence is a 2D array
	return 0


def test():

	sequences = testData
	itemSet = items 

	primalBlocks = [] * len(itemSet)
	for item in itemSet:
		primalBlocksOfItem = [] * len(sequences) 
		for sequence in sequences:
			primalBlocksOfItem.append(encodePrimalPosition(item, sequence))
		primalBlocks.append(primalBlocksOfItem)

	for index in xrange(0, len(itemSet)):
		print itemSet[index], " ", primalBlocks[index]


if __name__ == "__main__":
	test()


