#!/usr/bin/env python3

import sys

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
			# Append if not empty block
			if primalValue > 1:
				result.append({
					"posBlockIndexInSeq": primalBlockIndex, 
					"primalValue": primalValue 
				})

			# Reset for next loop
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


def test():
	arr = [
		['A.O', 'B.C.D.E.O1', 'F.G.H', 'I.J.K.M.N', 'O.P1.T', 'K1.L.P.Q.R.S.U', 'V.W.X.Y', 'B1.C1.D1.E1.G1.J1'],
		['A', 'A.B.C.D', 'E.F.G', 'H.I.J.K', 'L', 'M.N.O.P', 'Q.R', 'S.T.U.V.W'],
		['A', 'A.B.C', 'E.F', 'H.I.J', 'M.N.O.P.S', 'L.Q.R.X.Y', 'D.Z', 'A1.U.V.W'],
		['A.L', 'A.B.C.D', 'L', 'D.H.I.J.X', 'B1.N.O.P', 'Q.R.Y', 'F.Z', 'E.V.W'],
		['C1.L', 'B', 'E', 'D.H.I.J.X', 'F.M.N.P.Z', 'Q.R.Y', 'A.A1.O.S.U.V.W'],
		['A.L', 'A.B.C.C1.D', 'E.F.G', 'H.I.J.K', 'L', 'B1.M.N.O.P', 'Q.R', 'A1.U.V.W'],
		['A', 'B', 'D1', 'H.I.J', 'L', 'B1.P', 'Q.R', 'A.Z', 'E.F.N.U.V'],
		['C1.D.E.G.L', 'J', 'B1.P', 'Q'],
		['A.J1.L', 'B.C.K1.Z', 'D.F.J.L1.N'],
		['A.D.J1.L', 'B.C.K1.Z', 'E.J.L1.N'],
		['A.D.J1.L', 'B.C.K1.Z', 'E.F.J.N'],
		['A.D.J1.L', 'B.C.K1.Z'],
		['A.D.J1.L', 'B.C.K1.Z', 'E.F.J.L1.N.P'],
		['A.D.J1.L', 'B.C.K1.Z', 'E.F.J.L1.N'],
		['J1.L', 'B.C', 'J.L1.N']
	]
	ret = encodePrimalSequence('G', arr)
	print(ret)	


if __name__ == "__main__":

	test()

	# for index in range(0, len(ITEMS)):
	# 	#print ITEMS[index], seqBlocks[index]


