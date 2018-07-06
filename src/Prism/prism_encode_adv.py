#!/usr/bin/env python3

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
	for idx in range(0, itemsetLength):
		itemset = sequence[idx]

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

	# if NO_LOGS == False:
		#print "[Position Primal Encoded]:", result
	return result


# Done
def encodePrimalBlockAllSequences(item, sequences):
	primeArray = G_ARRAY_ADVANCE
	primeArrayLength = len(primeArray)

	numberOfSeq = len(sequences)
	posBlocks = []
	# Using 2D (array of array) to cache the offset based on block of sequence
	posOffsets = [[]] * (int)((numberOfSeq + primeArrayLength - 1) / primeArrayLength) 
	posOffsetsIndex = 0
	lastPosOffet = 1

	# #print "Leng init {0} for total seq {1}".format(len(posOffsets), numberOfSeq)

	for seqIndex in range(0, numberOfSeq):
		posOffsetsIndex = (int)(seqIndex / primeArrayLength)
		# #print "Cur pos offset index: ", posOffsetsIndex

		seq = sequences[seqIndex]
		posBlock = encodePrimalBlockInSequence(item, seq) # [ { blockIndex: , primalPos: }, ...]
		posBlockLength = len(posBlock)

		if posBlockLength > 0: # Sequence content the thing
			posBlocks += posBlock
			# Caching the prime value for extend process purpose later
			seqPrimeIndex = primeArray[seqIndex % primeArrayLength]

			posOffsets[posOffsetsIndex].append({
				"blockStartOffset": lastPosOffet,
				"numberOfBlocksInSeq": posBlockLength,
				"seqPrimeIndex": seqPrimeIndex 
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

	for index in range(0, numberOfSeq):
		seq = sequences[index]

		# Is exist in this sequence
		filterArray = list(filter(lambda itemset: string(itemset).findAdv(item) != -1, seq))
		primeValue *= 1 if not filterArray else primeArray[primeArrayIndex]
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


	# for index in range(0, len(ITEMS)):
	# 	#print ITEMS[index], seqBlocks[index]


