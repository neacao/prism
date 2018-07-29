#!/usr/bin/env python3

import sys, json
sys.path.insert(0, "../Util")

from prism_compute import *
from helper import *

# --- ENCODE PRIMAL BLOCKS ---
def encodePrimalPosBlockInSequence(item, sequence):
	result = [] # [ { posBlockIndexInSeq: , primalPos: }, ...]
	
	primeArray = G_ARRAY_ADVANCE
	primeArrayLenght = len(primeArray)
	primeArrayIndex = 0
	
	primalValue = 1
	primalBlockIndex = 0

	numberOfItemset = len(sequence)

	for idx in range(0, numberOfItemset):
		itemset = sequence[idx]

		if string(itemset).findAdv(item) != -1:
			primalValue *= primeArray[primeArrayIndex]
		primeArrayIndex += 1

		if primeArrayIndex == primeArrayLenght or idx == numberOfItemset - 1:
			if primalValue > 1:
				result.append({
					"posBlockIndexInSeq": primalBlockIndex, 
					"primalValue": primalValue 
				})

			primalValue = 1
			primalBlockIndex += 1
			primeArrayIndex = 0

	return result


def encodePrimalItemsetsForItem(item, sequences):
	primeArray = G_ARRAY_ADVANCE
	primeArrayLength = len(primeArray)

	numberOfSeq = len(sequences)
	primalPosBlockList = [] # 1D Array

	# Using 2D Array to cache the offset based on block of sequence
	maxLength = (int)((numberOfSeq + primeArrayLength - 1) / primeArrayLength)
	posOffsetsList = [[]] * maxLength
	posOffsetsIndex = 0
	lastPosOffset = 1

	for seqIndex in range(0, numberOfSeq):
		posOffsetsIndex = (int)(seqIndex / primeArrayLength)
		seq = sequences[seqIndex]
		
		primalPosBlock = encodePrimalPosBlockInSequence(item, seq) # [ { blockIndex: , primalPos: }, ...]
		numberOfBlocksInSeq = len(primalPosBlock)

		if numberOfBlocksInSeq > 0:
			primalPosBlockList += primalPosBlock
			seqPrimeIndex = primeArray[seqIndex % primeArrayLength]

			posOffsetsList[posOffsetsIndex].append({
				"blockStartOffset": lastPosOffset,
				"numberOfBlocksInSeq": numberOfBlocksInSeq,
				"seqPrimeIndex": seqPrimeIndex
			})
			lastPosOffset += numberOfBlocksInSeq
		
	return (primalPosBlockList, posOffsetsList)


def encodePrimalItemsetsAdv(items, sequences):
	primalPosBlocks = [] # 2D Array: [ [primalPosBlocksItem1], [primalPosBlockItem2] ]
	posOffsetBlocks = [] # 3D Array: [ [], [], [] ]

	for item in items:
		(primalBlock, posOffset) = encodePrimalItemsetsForItem(item, sequences)
		primalPosBlocks.append(primalBlock)
		posOffsetBlocks.append(posOffset)

	return primalPosBlocks, posOffsetBlocks
# --- END ENCODE PRIMAL BLOCKS ---


# --- ENCODE SEQUENCE ---
def encodePrimalSeqsForItem(item, sequences):
	result = [] # [  ]

	curPrimeValue = 1
	primeArray = G_ARRAY_ADVANCE
	primeArrayLength = len(primeArray)
	primeArrayIndex = 0

	numberOfSeq = len(sequences)

	# O( n * 8 * 8 ) (8 semesters * 8 course / semester)
	for index in range(0, numberOfSeq):
		seq = sequences[index]

		filterArray = list(filter(lambda itemset: string(itemset).findAdv(item) != -1, seq))
		if filterArray:
			curPrimeValue *= primeArray[primeArrayIndex]
		primeArrayIndex += 1

		# Enought for a block of sequence or in the last of sequence
		if primeArrayIndex == primeArrayLength or index == numberOfSeq - 1:
			result.append(curPrimeValue)
			curPrimeValue = 1
			primeArrayIndex = 0
	
	return result


def encodePrimalSeqsAdv(items, sequences):
	seqBlocks = [encodePrimalSeqsForItem(item, sequences) for item in items]
	return seqBlocks
# --- END ENCODE SEQUENCE ---


# Encode query input to predict
def encodeQuery(query, labelMappingPath):
	with open(labelMappingPath) as fp:
		labelMappingObj = json.load(fp)

	queryComponents = query.split("->")
	ret = ""

	for itemset in queryComponents:
		itemsetComponenets = itemset.split(".")

		for item in itemsetComponenets:
			if not item in labelMappingObj:
				print("[ERROR] Could not find <{0}> in trained data".format(item))
				return ""
			ret += "{0}.".format(labelMappingObj[item])

		ret = ret[:-1]
		ret += "->"

	return ret[:-2]




