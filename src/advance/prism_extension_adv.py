#!/usr/bin/env python

import sys, copy
sys.path.insert(0, '/Users/nea/Desktop/Course/src/')

from prism_compute import *
from prism_encode_advance import *

'''
	Brief: calculate posistion block each sequence
	Return: a list of pos block joining
'''
def calculatePrimalsPosEachSeq2(posOffset, posOffsetTarget, posBlocks, posBlocksTarget, isMask = False, isTesting = False):
	# Get the primal pos block length
	minNumberOfPosBlocks 		= min( posOffset["length"], posOffsetTarget["length"] )
	posBlockIndex 					= posOffset["offset"]
	posBlockIndexTarget 		= posOffsetTarget["offset"]

	posBlocksExt = []

	if isMask == True:
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

			else:
				print "===> IGNORE GCD:", posBlock, posBlockTarget

		else:
			print "===> IGNORE BLOCK INDEX:", posBlock, posBlockTarget

	return posBlocksExt


# Calculate extension of each sequence block
def seqExtensionAdv2(key, targetKey, seqBlock, seqBlockTarget, posOffsets, posOffsetsTarget, posBlocks, posBlocksTarget, lastOffset):
	seqBlockExt 	= computeGCDOfPrimalsValue( seqBlock, seqBlockTarget )
	posOffsetsExt = []
	posBlocksExt	= []

	lazyPosOffsetIndex 				= 0
	lazyPosOffsetIndexTarget 	= 0

	maxNumberOffsetBlocks = max( len(posOffsets), len(posOffsetsTarget) )

	# Loop on offsets to caculate position blocks
	while lazyPosOffsetIndex < maxNumberOffsetBlocks and lazyPosOffsetIndexTarget < maxNumberOffsetBlocks:

		encode 				= posOffsets[lazyPosOffsetIndex]["encode"]
		encodeTarget 	= posOffsetsTarget[lazyPosOffsetIndexTarget]["encode"]

		# Move the pointer to the right
		while(seqBlockExt % encode != 0):
			lazyPosOffsetIndex += 1
			encode = posOffsets[lazyPosOffsetIndex]["encode"]

		while(seqBlockExt % encodeTarget != 0):
			lazyPosOffsetIndexTarget += 1
			encodeTarget = posOffsetsTarget[lazyPosOffsetIndexTarget]["encode"]

		posBlock 				= posOffsets[lazyPosOffsetIndex]
		posBlockTarget 	= posOffsetsTarget[lazyPosOffsetIndexTarget]

		# Make a copy to avoid data be reassigned in calculate... function
		_posBlocks = copy.deepcopy(posBlocks)

		posBlocksJoin 			= calculatePrimalsPosEachSeq2(posBlock, posBlockTarget, _posBlocks, posBlocksTarget, True)
		posBlocksJoinLength = len(posBlocksJoin)

		# No empty block
		if posBlocksJoinLength > 0:
			for posBlock in posBlocksJoin:
				posBlocksExt.append(posBlock)
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


def test():
	(posOffsetsList, posBlocksList) = processEncodePrimalPosAdv(ITEMS, SEQUENCES)
	seqBlocksList = processEncodePrimalSeqAdv(ITEMS, SEQUENCES)

	print posOffsetsList[0][0]

	(seqBlockExt, posOffsetsExt, posBlocksExt, lastOffset) = seqExtensionAdv2(
		"a", "b",
		seqBlocksList[0][0], seqBlocksList[1][0],
		posOffsetsList[0][0], posOffsetsList[1][0],
		posBlocksList[0], posBlocksList[1],
		1,
	)

	print "Result:", seqBlockExt
	print posOffsetsExt
	print posBlocksExt

	return 1


if __name__ == "__main__":
	test()




