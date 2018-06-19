#!/usr/bin/env python

import sys, copy

from prism_compute import *
from prism_encode_advance import *

'''
	Brief: calculate posistion block each sequence
	Return: a list of pos block joining
'''
def calculatePrimalsPosEachSeq(posOffset, posOffsetTarget, posBlocks, posBlocksTarget, isSeqExt = False):
	# Get the primal pos block length
	minNumberOfPosBlocks 		= min( posOffset["length"], posOffsetTarget["length"] )
	posBlockIndex 					= posOffset["offset"]
	posBlockIndexTarget 		= posOffsetTarget["offset"]

	posBlocksExt = []

	if isSeqExt == True:
		maskValue = computeMaskValueOfPrimalValue( posBlocks[posBlockIndex - 1]["primalPos"] )
		posBlocks[posBlockIndex - 1]["primalPos"] = maskValue

		for index in xrange(1, minNumberOfPosBlocks):
			realIndex = primalPosIndex + posBlockIndex - 1
			posBlocks[realIndex]["primalPos"] = maxRankValue()


	for blockIndex in xrange(0, minNumberOfPosBlocks):
		realIndex 			= blockIndex + posBlockIndex - 1
		realIndexTarget = blockIndex + posBlockIndexTarget - 1

		posBlock 				= posBlocks[realIndex]
		posBlockTarget 	= posBlocksTarget[realIndexTarget]

		posBlockIndex 			= posBlock["blockIndex"]
		posBlockIndexTarget	= posBlockTarget["blockIndex"]

		if posBlockIndex == posBlockIndexTarget:
			posBlockVal 			= posBlock["primalPos"]
			posBlockValTarget = posBlockTarget["primalPos"]

			posBlockJoin = computeGCDOfPrimalsValue( posBlockVal, posBlockValTarget )

			if posBlockJoin > 1:
				posBlocksExt.append({
					"primalPos": posBlockJoin,
					"blockIndex": blockIndex
				})
		# 	else:
		# 		print "===> IGNORE GCD:", posBlock, posBlockTarget
		# else:
		# 	print "===> IGNORE BLOCK INDEX:", posBlock, posBlockTarget

	return posBlocksExt


# Calculate extension of each sequence block
def calculateExtensionAdv(key, targetKey, 
	seqBlock, seqBlockTarget, 
	posOffsets, posOffsetsTarget, 
	posBlocks, posBlocksTarget, 
	lastOffset, isSeqExt = False):
	seqBlockExt 	= computeGCDOfPrimalsValue( seqBlock, seqBlockTarget )
	posOffsetsExt = []
	posBlocksExt	= []

	lazyPosOffsetIndex 				= 0
	lazyPosOffsetIndexTarget 	= 0

	posOffsetsLength 				= len(posOffsets)
	posOffsetsLengthTarget 	= len(posOffsetsTarget)
	maxNumberOffsetBlocks 	= max( posOffsetsLength, posOffsetsLengthTarget )

	# Loop on offsets to caculate position blocks
	while lazyPosOffsetIndex < posOffsetsLength and lazyPosOffsetIndexTarget < posOffsetsLengthTarget:

		if lazyPosOffsetIndex == len(posOffsets):
			print "Checking:", posOffsets, posOffsetsTarget

		encode 				= posOffsets[lazyPosOffsetIndex]["encode"]
		encodeTarget 	= posOffsetsTarget[lazyPosOffsetIndexTarget]["encode"]

		# Move the pointer to the right
		while seqBlockExt % encode != 0 and lazyPosOffsetIndex < posOffsetsLength - 1:
			lazyPosOffsetIndex += 1
			encode = posOffsets[lazyPosOffsetIndex]["encode"]

		if lazyPosOffsetIndex == posOffsetsLength:
			return (seqBlockExt, posOffsetsExt, posBlocksExt, lastOffset)

		while seqBlockExt % encodeTarget != 0 and lazyPosOffsetIndexTarget < posOffsetsLengthTarget - 1:
			lazyPosOffsetIndexTarget += 1
			encodeTarget = posOffsetsTarget[lazyPosOffsetIndexTarget]["encode"]

		if lazyPosOffsetIndexTarget == posOffsetsLengthTarget:
			return (seqBlockExt, posOffsetsExt, posBlocksExt, lastOffset)

		posBlock 				= posOffsets[lazyPosOffsetIndex]
		posBlockTarget 	= posOffsetsTarget[lazyPosOffsetIndexTarget]

		# Make a copy to avoid data be reassigned in calculate... function
		_posBlocks = copy.deepcopy(posBlocks)

		posBlocksJoin 			= calculatePrimalsPosEachSeq(posBlock, posBlockTarget, _posBlocks, posBlocksTarget, isSeqExt)
		posBlocksJoinLength = len(posBlocksJoin)

		# No empty block
		if posBlocksJoinLength > 0:
			posBlocksExt += posBlocksJoin
			
			posOffsetsExt.append({
				"offset": lastOffset,
				"length": posBlocksJoinLength,
				"encode": encode
			})
			lastOffset += posBlocksJoinLength
		# Remove empty block in sequence from seqBlockExt
		else:
			seqBlockExt /= encode

		lazyPosOffsetIndex 				+= 1
		lazyPosOffsetIndexTarget 	+= 1

	return (seqBlockExt, posOffsetsExt, posBlocksExt, lastOffset)


# Calcualte seq extension of all sequence blocks
def processExtensionAdv(key, targetKey, seqBlocks, seqBlocksTarget, posOffsetsList, posOffsetsListTarget, posBlocks, posBlocksTarget, isSeqExt):
	seqBlocksExt = []
	posOffsetsListExt = [[]] * len(seqBlocks)
	posBlocksExt = []

	numberOfSeqBlocks = len(seqBlocks)
	lastOffset = 1

	# Loop on sequence block
	for seqIndex in xrange(0, numberOfSeqBlocks):
		posOffsets 				= posOffsetsList[seqIndex]
		posOffsetsTarget 	= posOffsetsListTarget[seqIndex]

		(seqBlockExt, posOffsetsExt, _posBlocksExt, _lastOffset) = calculateExtensionAdv(
			key, targetKey,
			seqBlocks[seqIndex]	, seqBlocksTarget[seqIndex],
			posOffsetsList[seqIndex], posOffsetsListTarget[seqIndex],
			posBlocks, posBlocksTarget, lastOffset,
			isSeqExt
		)

		_lastOffset = lastOffset
		seqBlocksExt.append(seqBlockExt)
		posOffsetsListExt[seqIndex] += posOffsetsExt
		posBlocksExt += _posBlocksExt

	return (seqBlocksExt, posOffsetsListExt, posBlocksExt)



def test():
	(posOffsetsList, posBlocksList) = processEncodePrimalPosAdv(ITEMS, SEQUENCES)
	seqBlocksList = processEncodePrimalSeqAdv(ITEMS, SEQUENCES)

	(seqBlockExt, posOffsetsExt, posBlocksExt) = processExtensionAdv(
		"a", "b",
		seqBlocksList[0], seqBlocksList[1],
		posOffsetsList[0], posOffsetsList[1],
		posBlocksList[0], posBlocksList[1],
		True
	)

	print "Result:", seqBlockExt
	print posOffsetsExt
	print posBlocksExt

	return 1


if __name__ == "__main__":
	test()




