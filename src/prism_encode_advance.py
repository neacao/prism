#!/usr/bin/env python

from constant import *
from util import *

def encodeBitPositionAdv(key, array):
	result = []
	for element in array:
		index = element.find(key)
		if index != -1:
			result.append(1)
		else:
			result.append(0)

	# Padding 0
	length = len(result)
	divisibleNumber = findNumberDivisible(length, G_LENGTH_ADVANCE)
	for index in xrange(length, divisibleNumber):
		result.append(0)

	if NO_LOGS == False:
		print "[Pos Encode Bit]:", result
	return result


def encodePrimalPositionAdv(key, array):
	bitEncodedPos = encodeBitPositionAdv(key, array)
	result = []
	length = len(bitEncodedPos)

	for blockIndex in xrange(0, length/G_LENGTH_ADVANCE):
		index = blockIndex * G_LENGTH_ADVANCE
		tmp = 1
		
		# Testing purpose, using G_LENGTH_ADVANCE = 8
		if bitEncodedPos[index] == 1: tmp *= 2
		if bitEncodedPos[index + 1] == 1: tmp *= 3
		if bitEncodedPos[index + 2] == 1: tmp *= 5
		if bitEncodedPos[index + 3] == 1: tmp *= 7
		if bitEncodedPos[index + 4] == 1: tmp *= 11
		if bitEncodedPos[index + 5] == 1: tmp *= 13
		if bitEncodedPos[index + 6] == 1: tmp *= 17
		if bitEncodedPos[index + 7] == 1: tmp *= 19

		result.append(tmp)

	if NO_LOGS == False:
		print "[Pos Encode Primal]:", result
	return result
