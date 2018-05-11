#!/usr/bin/env python

import sys
sys.path.insert(0, '/Users/nea/Desktop/Course/src/')

from constant import *
from prism_compute import *

def encodeBitPositionAdv(item, sequence):
	result = []

	for itemset in sequence:
		val = 1 if itemset.find(item) != -1 else 0
		result.append(val)

	# Zero padding
	length = len(result)
	divisibleNumber = findNumberDivisible(length, G_LENGTH_ADVANCE)
	result += [0] * (divisibleNumber - length)

	if NO_LOGS == False:
		print "[Pos Encode Bit]:", result
	return result


def encodePrimalPositionAdv(item, sequence):
	bitPosEncoded = encodeBitPositionAdv(item, sequence)

	length = len(bitPosEncoded)
	result = []

	for blockIndex in xrange(0, length / G_LENGTH_ADVANCE):
		index = blockIndex * G_LENGTH_ADVANCE
		val = 1

		# if bitPosEncoded[index] == 1: val *= 2
		# if bitPosEncoded[index + 1] == 1: val *= 3
		# if bitPosEncoded[index + 2] == 1: val *= 5
		# if bitPosEncoded[index + 3] == 1: val *= 7
		# if bitPosEncoded[index + 4] == 1: val *= 11
		# if bitPosEncoded[index + 5] == 1: val *= 13
		# if bitPosEncoded[index + 6] == 1: val *= 17
		# if bitPosEncoded[index + 7] == 1: val *= 19

		for primeIndex in xrange(0, G_LENGTH_ADVANCE):
			if bitPosEncoded[primeIndex + index] == 1:
				val *= G_ARRAY_ADVANCE[primeIndex]

		# Return empty array if 
		if val > 1:
			result.append({
				"blockIndex": blockIndex,
				"primalPos": val
			})
			
	if NO_LOGS == False:
		print "[Pos Encode Primal]:", result
	return result


def processEncodePrimalPosAdv(items, sequences):
	primalsPosAllItems = []
	posOffsetsAllItems = []
	numberOfSeq = len(sequences)

	for item in items:
		primalPosOffset = []
		lastPrimalBlockOffset = 1 # Couting current primal block offset	

		itemPrimalsPosBlock = [[]] * ((numberOfSeq + G_LENGTH_ADVANCE - 1) / G_LENGTH_ADVANCE)
		itemPrimalsPosBlockIndex = 0
		itemPrimalsPosBlock[itemPrimalsPosBlockIndex] = []

		for seqIndex in xrange(0, numberOfSeq):
			primalPos = encodePrimalPositionAdv(item, sequences[seqIndex])
			length = len(primalPos)

			if length > 0:
				primalPosOffset.append( lastPrimalBlockOffset )
				lastPrimalBlockOffset += length
				itemPrimalsPosBlock[itemPrimalsPosBlockIndex] += primalPos
			
			if seqIndex != 0 and ((seqIndex + 1) % G_LENGTH_ADVANCE == 0):
				itemPrimalsPosBlockIndex += 1
				itemPrimalsPosBlock[itemPrimalsPosBlockIndex] = []

		primalsPosAllItems.append(itemPrimalsPosBlock)
		posOffsetsAllItems.append(primalPosOffset)

	return (posOffsetsAllItems, primalsPosAllItems)


def encodeBitSeqAdv(item, sequences):
	result = []

	for sequence in sequences:
		filterArray = filter(lambda itemset: itemset.find(item) != -1, sequence)
		val = 0 if not filterArray else 1
		result.append(val)

	length = len(result)
	divisibleNumber = findNumberDivisible(length, G_LENGTH_ADVANCE)
	result += [0] * (divisibleNumber - length)

	if NO_LOGS == False:
		print "[Seq Encode Bit]:", result
	return result


def encodePrimalSeq(item, sequences):
	bitSeqEncoded = encodeBitSeqAdv(item, sequences)

	result = []
	length = len(bitSeqEncoded)

	for blockIndex in xrange(0, length/G_LENGTH_ADVANCE):
		index = blockIndex * G_LENGTH_ADVANCE
		val = 1

		# if bitSeqEncoded[index] == 1: val *= 2
		# if bitSeqEncoded[index + 1] == 1: val *= 3
		# if bitSeqEncoded[index + 2] == 1: val *= 5
		# if bitSeqEncoded[index + 3] == 1: val *= 7
		# if bitSeqEncoded[index + 4] == 1: val *= 11
		# if bitSeqEncoded[index + 5] == 1: val *= 13
		# if bitSeqEncoded[index + 6] == 1: val *= 17
		# if bitSeqEncoded[index + 7] == 1: val *= 19

		for primeIndex in xrange(0, G_LENGTH_ADVANCE):
			if bitSeqEncoded[primeIndex + index] == 1:
				val *= G_ARRAY_ADVANCE[primeIndex]

		if val > 1:
			result.append(val)


	if NO_LOGS == False:
		print "[Seq Encode Primal]:", result
	return result


def processEncodePrimalSeqAdv(items, sequences):
	primalsSeq = []

	for item in items:
		itemPrimalSeq = encodePrimalSeq(item, sequences)
		primalsSeq.append(itemPrimalSeq)

	return primalsSeq

if __name__ == "__main__":
	(posOffsetsAllItems, primalPosAllItems) = processEncodePrimalPosAdv(ITEMS, SEQUENCES)
	primalSeqAllItems = processEncodePrimalSeqAdv(ITEMS, SEQUENCES)

	for index in xrange(0, len(ITEMS)):
		print ITEMS[index], primalSeqAllItems[index], posOffsetsAllItems[index], primalPosAllItems[index]






