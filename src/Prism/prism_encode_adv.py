#!/usr/bin/env python3

import sys

from constant import *
from prism_compute import *
from helper import *

# --- ENCODE PRIMAL BLOCKS ---
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
# --- END ENCODE PRIMAL BLOCKS ---


# --- ENCODE SEQUENCE ---
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


def processEncodePrimalSeqAdv(items, sequences):
	seqBlocks = [encodePrimalSequence(item, sequences) for item in items]
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


