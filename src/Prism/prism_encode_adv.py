#!/usr/bin/env python

import sys

from constant import *
from prism_compute import *
from helper import *

# Done
def encodePrimalBlockInSequence(item, sequence):
	result = [] # [ { blockIndex: , primalPos: }, ...]
	
	primalValue = 1
	primalBlockIndex = 0

	primeArrayIndex = 0
	primeArray = G_ARRAY_ADVANCE
	primeArrayLenght = len(primeArray)

	itemsetLength = len(sequence)

	# Loop on itemset list in a sequence
	for idx in xrange(0, itemsetLength):
		itemset = sequence[idx]
		# primalValue *= primeArray[primeArrayIndex] if itemset.find(item) != -1 else 1
		primalValue *= primeArray[primeArrayIndex] if string(itemset).findAdv(item) != -1 else 1
		primeArrayIndex += 1

		# Enough for a block of itemsets in a sequence or last itemset in sequence
		if primeArrayIndex == primeArrayLenght or idx == itemsetLength - 1:
			# Append if it appeard
			if primalValue > 1:
				result.append({ "blockInSeqIndex": primalBlockIndex, "primalValue": primalValue })

			# Reset value
			primalValue = 1
			primalBlockIndex += 1
			primeArrayIndex = 0

	if NO_LOGS == False:
		print "[Position Primal Encoded]:", result
	return result


# Done
def encodePrimalBlockAllSequences(item, sequences):
	primeArray = G_ARRAY_ADVANCE
	primeArrayLength = len(primeArray)

	numberOfSeq = len(sequences)
	posBlocks = []
	posOffsets = [[]] * ((numberOfSeq + 1) / primeArrayLength) # Using 2D (array of array) to cache the offset based on block of sequence
	posOffsetsIndex = 0
	lastPosOffet = 1

	for seqIndex in xrange(0, numberOfSeq):
		posOffsetsIndex = seqIndex / primeArrayLength
		seq = sequences[seqIndex]
		posBlock = encodePrimalBlockInSequence(item, seq) # [ { blockIndex: , primalPos: }, ...]
		posBlockLength = len(posBlock)

		if posBlockLength > 0: # Sequence content the thing
			posBlocks += posBlock
			posOffsets[posOffsetsIndex].append({
				"blockStartOffset": lastPosOffet,
				"numberOfBlocksInSeq": posBlockLength,
				"seqPrimeIndex": primeArray[seqIndex % primeArrayLength] # Caching the prime value for extend process purpose later
			})
			lastPosOffet += posBlockLength
		
	return (posBlocks, posOffsets)


# Done
def processEncodePrimalBlockAllSequences(items, sequences):
	itemLength = len(items)
	itemsPosBlocks = []
	itemsPosOffsets = []

	for item in items:
		(posBlocks, posOffsets) = encodePrimalBlockAllSequences(item, sequences)
		itemsPosBlocks.append(posBlocks)
		itemsPosOffsets.append(posOffsets)

	return itemsPosBlocks, itemsPosOffsets


# Done
def encodePrimalSequence(item, sequences):
	result = []

	primeValue = 1
	primeArray = G_ARRAY_ADVANCE
	primeArrayLength = len(primeArray)
	primeArrayIndex = 0

	numberOfSeq = len(sequences)

	for index in xrange(0, numberOfSeq):
		seq = sequences[index]
		filterArray = filter(lambda itemset: string(itemset).findAdv(item) != -1, seq)
		primeValue *= 1 if not filterArray else primeArray[primeArrayIndex] # if not empty
		
		primeArrayIndex += 1

		# Enough for a block of sequences or last sequence
		if primeArrayIndex == primeArrayLength or index == numberOfSeq - 1:
			result.append(primeValue)
			# Reset value
			primeValue = 1
			primeArrayIndex = 0
	
	return result


# Done
def processEncodePrimalSeqAdv(items, sequences):
	seqBlocks = []

	for item in items:
		seqBlocks.append( encodePrimalSequence(item, sequences) )

	return seqBlocks


if __name__ == "__main__":
	(itemsPosBlocks, itemsPosOffsets) = processEncodePrimalBlockAllSequences(ITEMS, SEQUENCES)
	seqBlocks = processEncodePrimalSeqAdv(ITEMS, SEQUENCES)


	# for index in xrange(0, len(ITEMS)):
	# 	print ITEMS[index], seqBlocks[index]


