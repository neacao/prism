#!/usr/bin/env python

import sys, copy
sys.path.insert(0, "./")

import prism_encode_adv as Encoder
from helper import *
from prism_compute import *

'''
	- Brief: calculate posistion block each sequence
	- posOffset & posOffsetTarget: posOffset of each sequence
		{ "blockStartOffset": ,"numberOfBlocksInSeq": , "seqPrimeIndex": encode }
	- posBlocks & posBlocksTarget: list of position blocks encoded for all sequences
		[ { "posBlockIndexInSeq": ,"primalValue" }, ... ]
	- Return: a list of pos block joining
'''
def computePosBlocksInSequence(key, targetKey,
 posOffset, posOffsetTarget, posBlocks, posBlocksTarget, 
 isSeqExt = False, DEBUG=False):

	# Get the primal pos block length
	minNumberOfPosBlocks 		= min( posOffset["numberOfBlocksInSeq"], posOffsetTarget["numberOfBlocksInSeq"] )
	posBlockIndex 					= posOffset["blockStartOffset"]
	posBlockIndexTarget 		= posOffsetTarget["blockStartOffset"]

	posBlocksExt = []

	if isSeqExt == True:
		maskValue = computeMaskValueOfPrimalValue( posBlocks[posBlockIndex - 1]["primalValue"] )
		posBlocks[posBlockIndex - 1]["primalValue"] = maskValue

		for index in range(1, minNumberOfPosBlocks):
			realIndex = index + posBlockIndex - 1
			posBlocks[realIndex]["primalValue"] = maxRankValue()


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

			posBlockJoin = computeGCDOfPrimalsValue( posBlockVal, posBlockValTarget )

			# if DEBUG:
			# print("GCD of {0} {1} is {2} in blockIndex {3} {4} at index {5} {6}".format(posBlockVal, posBlockValTarget,
			#  posBlockJoin, posBlockIndex, posBlockIndexTarget, realIndex, realIndexTarget))
			# print("-- blockJoin: {0} & {1} = {2}".format(posBlockVal, posBlockValTarget, posBlockJoin))

			if posBlockJoin > 1:
				posBlocksExt.append({
					"primalValue": posBlockJoin,
					"posBlockIndexInSeq": blockIndex
				})
		# 	else:
		# 		#print "===> IGNORE GCD:", posBlock, posBlockTarget
		# else:
		# 	#print "===> IGNORE BLOCK INDEX:", posBlock, posBlockTarget
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
	lastPosBlockOffset, isSeqExt, DEBUG=False):

	seqBlockExt = computeGCDOfPrimalsValue( seqBlock, seqBlockTarget )
	bitValue = computeBitValueOfPrimalValue(seqBlockExt)
	print("Primal {0} \n=> Bit value {1}".format(seqBlockExt, bitValue))

	if seqBlockExt == 1:
		return 1, [], [], lastPosBlockOffset

	posOffsetsExt = []
	posBlocksExt	= []

	lazyPosOffsetIndex 				= 0
	lazyPosOffsetIndexTarget 	= 0

	posOffsetsLength 				= len(posOffsets)
	posOffsetsLengthTarget 	= len(posOffsetsTarget)
	# maxNumberOffsetBlocks 	= max( posOffsetsLength, posOffsetsLengthTarget )

	# Loop on offsets to caculate position blocks
	while lazyPosOffsetIndex < posOffsetsLength and lazyPosOffsetIndexTarget < posOffsetsLengthTarget:
		encode 				= posOffsets[lazyPosOffsetIndex]["seqPrimeIndex"]
		encodeTarget 	= posOffsetsTarget[lazyPosOffsetIndexTarget]["seqPrimeIndex"]

		# Move the pointer to the right if not correct primal block
		while seqBlockExt % encode != 0 and lazyPosOffsetIndex < posOffsetsLength - 1:
			lazyPosOffsetIndex += 1
			encode = posOffsets[lazyPosOffsetIndex]["seqPrimeIndex"]

		if lazyPosOffsetIndex == posOffsetsLength:
			return (seqBlockExt, posOffsetsExt, posBlocksExt, lastPosBlockOffset)
		# -- End move pointer of key

		# Move the pointer to the right if not correct primal block
		while seqBlockExt % encodeTarget != 0 and lazyPosOffsetIndexTarget < posOffsetsLengthTarget - 1:
			lazyPosOffsetIndexTarget += 1
			encodeTarget = posOffsetsTarget[lazyPosOffsetIndexTarget]["seqPrimeIndex"]

		if lazyPosOffsetIndexTarget == posOffsetsLengthTarget:
			return (seqBlockExt, posOffsetsExt, posBlocksExt, lastPosBlockOffset)
		# -- End move pointer of target key

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
			seqBlockExt /= encode

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
 isSeqExt, DEBUG=False):

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



def test():
	(posBlocksList, posOffsetsList) = Encoder.processEncodePrimalBlockAllSequences(ITEMS, SEQUENCES)
	seqBlocksList = Encoder.processEncodePrimalSeqAdv(ITEMS, SEQUENCES)

	(seqBlockExt, posOffsetsExt, posBlocksExt) = extend(
		"G", "D1",
		seqBlocksList[1], seqBlocksList[0],
		posOffsetsList[1], posOffsetsList[0],
		posBlocksList[1], posBlocksList[0],
		False
	)

	#print "Result:", seqBlockExt
	#print posBlocksExt
	#print posOffsetsExt
	return
	

if __name__ == "__main__":
	test()




