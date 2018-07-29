#!/usr/bin/env python3

import sys, copy
sys.path.insert(0, "./")

import prism_compute as Computer
import prism_encode_adv as Encoder
from helper import * 

'''
	Calculate primal position block s in this sequence
	Params:
		key 							: string - the key will be extended
		targetKey 				: string - the key will be added below 'key'
		posOffset 				: object ("numberOfBlocksInSeq", "blockStartOffset") of key
		posOffsetTarget 	: object ("numberOfBlocksInSeq", "blockStartOffset") of target key
		posBlocks 				: 1D array - all primal position value of this key
		posBlocksTarget 	: 1D array - all primal position value of target key
		isSeqExt 					: boolean - determine compute for itemset (false) or sequence (true) extension
		DEBUG 						: print log purposed
'''
def computePosBlocksInSequence(key, targetKey,
 posOffset, posOffsetTarget, 
 posBlocks, posBlocksTarget, 
 isSeqExt = False, DEBUG = False):

	# Get the primal pos block length
	minNumberOfPosBlocks 		= min( posOffset["numberOfBlocksInSeq"], posOffsetTarget["numberOfBlocksInSeq"] )
	posBlockIndex 					= posOffset["blockStartOffset"]
	posBlockIndexTarget 		= posOffsetTarget["blockStartOffset"]

	posBlocksExt = []

	if isSeqExt == True:
		startIndex = posBlockIndex - 1 # Real index
		maskValue = Computer.computeMaskValueOfPrimalValue( posBlocks[startIndex]["primalValue"] )

		# Loop on position block to get first value greater than 1
		while startIndex < minNumberOfPosBlocks and maskValue == 1:
			startIndex += 1
			maskValue = Computer.computeMaskValueOfPrimalValue( posBlocks[startIndex]["primalValue"] )

		# Quick return if this block is all empty
		if startIndex == minNumberOfPosBlocks and maskValue == 1:
			return []

		posBlocks[startIndex]["primalValue"] = maskValue
		startIndex += 1

		for index in range(startIndex, minNumberOfPosBlocks):
			posBlocks[index]["primalValue"] = maxRankValue()


	for blockIndex in range(0, minNumberOfPosBlocks):
		realIndex 			= blockIndex + posBlockIndex - 1
		realIndexTarget = blockIndex + posBlockIndexTarget - 1

		posBlock 				= posBlocks[realIndex]
		posBlockTarget 	= posBlocksTarget[realIndexTarget]

		posBlockIndex 			= posBlock["posBlockIndexInSeq"]
		posBlockIndexTarget	= posBlockTarget["posBlockIndexInSeq"]

		if posBlockIndex == posBlockIndexTarget:
			posBlockVal 			= posBlock["primalValue"]
			posBlockValTarget = posBlockTarget["primalValue"]

			posBlockJoin = Computer.computeGCDOfPrimalsValue( posBlockVal, posBlockValTarget )

			if posBlockJoin > 1:
				posBlocksExt.append({
					"primalValue": posBlockJoin,
					"posBlockIndexInSeq": blockIndex
				})

	return posBlocksExt


'''
	Calculate single sequence block
	Params:
		key 								: string - the key will be extended
		targetKey 					: string - the key will be added below 'key'
		seqBlock 						: int - primal value of sequence block of key
		seqBlockTarget 			: int - prinal value of sequence block of target key
		posOffsets 					: 1D array - all primal value index in posBlocks of key
		posOffsetsTarget 		: 1D array - all primal value index in posBlocksTarget of targetKey
		posBlocks 					: 1D array - all primal value of key
		posBlocksTarget 		: 1D array - all primal value of target key
		lastPosBlockOffset 	: int - the last index of primal position joined
		isSeqExt 						: boolean - extend by itemset (false) or sequence (true)
		DEBUG 							: boolean - print value purposed
'''
def computeSingleSeqBlock(key, targetKey, 
	seqBlock, seqBlockTarget, 
	posOffsets, posOffsetsTarget, 
	posBlocks, posBlocksTarget, 
	lastPosBlockOffset, isSeqExt, DEBUG = False):

	seqBlockExt = Computer.computeGCDOfPrimalsValue( seqBlock, seqBlockTarget )

	if seqBlockExt == 1:
		return 1, [], [], lastPosBlockOffset

	posOffsetsExt = []
	posBlocksExt	= []

	lazyPosOffsetIndex 				= 0
	lazyPosOffsetIndexTarget 	= 0

	posOffsetsLength 				= len(posOffsets)
	posOffsetsLengthTarget 	= len(posOffsetsTarget)

	while lazyPosOffsetIndex < posOffsetsLength and lazyPosOffsetIndexTarget < posOffsetsLengthTarget:
		encode 				= posOffsets[lazyPosOffsetIndex]["seqPrimeIndex"]
		encodeTarget 	= posOffsetsTarget[lazyPosOffsetIndexTarget]["seqPrimeIndex"]

		# Move the pointer to the right if not correct primal block
		while seqBlockExt % encode != 0 and lazyPosOffsetIndex < posOffsetsLength - 1:
			lazyPosOffsetIndex += 1
			encode = posOffsets[lazyPosOffsetIndex]["seqPrimeIndex"]

		while seqBlockExt % encodeTarget != 0 and lazyPosOffsetIndexTarget < posOffsetsLengthTarget - 1:
			lazyPosOffsetIndexTarget += 1
			encodeTarget = posOffsetsTarget[lazyPosOffsetIndexTarget]["seqPrimeIndex"]
		# --- End move pointer to right

		posOffset = posOffsets[lazyPosOffsetIndex]
		posOffsetTarget = posOffsetsTarget[lazyPosOffsetIndexTarget]

		# Make a copy to avoid data be reassigned in calculate... function
		_posBlocks = copy.deepcopy(posBlocks)

		_posBlocksExt = computePosBlocksInSequence(
			key, targetKey, 
			posOffset, posOffsetTarget, _posBlocks, posBlocksTarget, 
			isSeqExt, DEBUG)

		posBlocksJoinLength = len(_posBlocksExt)

		# No empty block
		if posBlocksJoinLength > 0:
			posBlocksExt += _posBlocksExt
			
			posOffsetsExt.append({
				"blockStartOffset": lastPosBlockOffset,
				"numberOfBlocksInSeq": posBlocksJoinLength,
				"seqPrimeIndex": encode
			})
			lastPosBlockOffset += posBlocksJoinLength

		# Remove empty block in sequence if joined before
		elif (encode == encodeTarget and seqBlockExt % encode == 0):
			seqBlockExt = (int)(seqBlockExt / encode)

		lazyPosOffsetIndex 				+= 1
		lazyPosOffsetIndexTarget 	+= 1

	# Avoid empty join block
	if not posBlocksExt:
		return (1, [], [], lastPosBlockOffset)
	else:
		return (seqBlockExt, posOffsetsExt, posBlocksExt, lastPosBlockOffset)


'''
	Calculate seq extension of all sequence blocks
	Params:
		key 									: the key will be extended
		targetKey 						: the key will be added below 'key'
		seqBlocks 						: 1D array - all sequence blocks of key
		seqBlocksTarget 			: 1D array - all sequence block of target key
		posOffsetsList 				: 2D array - all primal value index of key
		posOffsetsListTarget 	: 2D array - all primal value index of target key
		posBlocks 						: 1D array - all primal value of all keys
		posBlocksTarget 			: 1D array - all primal value of all target keys
		isSeqExt 							: extend by itemset (false) or sequence (true)
		DEBUG 								: print value purposed
'''
def extend(key, targetKey,
 seqBlocks, seqBlocksTarget,
 posOffsetsList, posOffsetsListTarget, 
 posBlocks, posBlocksTarget, 
 isSeqExt, DEBUG = False):

	seqBlocksExt 			= []
	posOffsetsListExt = [[]] * len(seqBlocks)
	posBlocksExt 			= []

	numberOfSeqBlocks 	= len(seqBlocks)
	lastPosBlockOffset 	= 1

	# Loop on sequence block
	for seqIndex in range(0, numberOfSeqBlocks):
		posOffsets 				= posOffsetsList[seqIndex]
		posOffsetsTarget 	= posOffsetsListTarget[seqIndex]
		seqBlock 					= seqBlocks[seqIndex]
		seqBlockTarget 		= seqBlocksTarget[seqIndex]

		(_seqBlockExt, _posOffsetsExt, _posBlocksExt, _lastPosBlockOffset) = computeSingleSeqBlock(
			key, targetKey,
			seqBlock, seqBlockTarget,
			posOffsets, posOffsetsTarget,
			posBlocks, posBlocksTarget, lastPosBlockOffset,
			isSeqExt, DEBUG
		)

		lastPosBlockOffset = _lastPosBlockOffset
		seqBlocksExt.append(_seqBlockExt)
		posOffsetsListExt[seqIndex] += _posOffsetsExt
		posBlocksExt += _posBlocksExt
	return (seqBlocksExt, posOffsetsListExt, posBlocksExt)



# TESTING PURPOSE
def test():
	return
	

if __name__ == "__main__":
	test()




