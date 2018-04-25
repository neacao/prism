#!/usr/bin/env python

from util import *
from constant import *


def encodeBitPosition(key, array):
	result = []
	for element in array:
		index = element.find(key)
		if index != -1:
			result.append(1)
		else:
			result.append(0)

	# Padding 0
	length = len(result)
	divisibleNumber = findNumberDivisible(length, G_LENGTH)
	for index in xrange(length, divisibleNumber):
		result.append(0)

	print "[Pos Encode Bit]:", result
	return result


def encodePrimalPosition(key, array):
	bitEncodedPos = encodeBitPosition(key, array)
	result = []
	length = len(bitEncodedPos)

	for blockIndex in xrange(0, length/G_LENGTH):
		index = blockIndex * G_LENGTH
		tmp = 1
		
		# Testing purpose, using G_LENGTH = 4
		if bitEncodedPos[index] == 1: tmp *= 2
		if bitEncodedPos[index + 1] == 1: tmp *= 3
		if bitEncodedPos[index + 2] == 1: tmp *= 5
		if bitEncodedPos[index + 3] == 1: tmp *= 7

		result.append(tmp)

	print "[Pos Encode Primal]:", result
	return result


def encodeBitSequences(key, sequences):
	result = []
	for sequence in sequences:
			foundFlag = False

			for itemset in sequence:
				index = itemset.find(item)
				if index != -1:
					foundFlag = True
					break

			if foundFlag == True:
				result.append(1)
			else:
				result.append(0)

	# Padding 0
	length = len(result)
	divisibleNumber = findNumberDivisible(length, G_LENGTH)
	for index in xrange(len(bitEncodedSequence), divisibleNumber):
		result.append(0)

	print "[Seq Encode Bit]:", result
	return result


def encodePrimalSequences(key, sequences): # Sequences is a 2D array
	bitEncodedSequences = encodeBitSequence(key, sequences)
	result = []
	length = len(bitEncodedSequences)

	for blockIndex in xrange(0, length/G_LENGTH):
		index = blockIndex * G_LENGTH
		tmp = 1
		
		# Testing purpose, using G_LENGTH = 4
		if bitEncodedSequences[index] == 1: tmp *= 2
		if bitEncodedSequences[index + 1] == 1: tmp *= 3
		if bitEncodedSequences[index + 2] == 1: tmp *= 5
		if bitEncodedSequences[index + 3] == 1: tmp *= 7
		result.append(tmp)
	
	print "[Seq Encode Primal]:", result
	return result


def processPrimalEncodingPos():
	items = ITEMS
	sequences = SEQUENCES

	fullPrimalSeqBlocks = [] * len(items)
	for item in items:
		itemPrimalBlocks = [] * len(sequences)

		for sequence in sequences:
			itemPrimalBlocks.append(encodePrimalPosition(item, sequence))

		fullPrimalBlocks.append(itemPrimalBlocks)

	for index in xrange(0, len(items)):
		print items[index], " ", fullPrimalBlocks[index]


def processPrimalEncodingSeq():
	items = ITEMS
	sequences = SEQUENCES

	fullPrimalSeqBlocks = [] * len(items)
	for item in items:
		fullPrimalSeqBlocks.append(encodePrimalSequences(item, sequences))

	for index in xrange(0, len(items)):
		print items[index], " ", fullPrimalSeqBlocks[index]

if __name__ == "__main__":
	processPrimalEncodingPos()
	processPrimalEncodingSeq()

