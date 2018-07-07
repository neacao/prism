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
		[ { "blockInSeqIndex": ,"primalValue" }, ... ]
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

		posBlockIndex 			= posBlock["blockInSeqIndex"]
		posBlockIndexTarget	= posBlockTarget["blockInSeqIndex"]

		if posBlockIndex == posBlockIndexTarget:
			posBlockVal 			= posBlock["primalValue"]
			posBlockValTarget = posBlockTarget["primalValue"]

			posBlockJoin = computeGCDOfPrimalsValue( posBlockVal, posBlockValTarget )

			# if DEBUG:
			# print("GCD of {0} {1} is {2} in blockIndex {3} {4} at index {5} {6}".format(posBlockVal, posBlockValTarget,
			#  posBlockJoin, posBlockIndex, posBlockIndexTarget, realIndex, realIndexTarget))
			print("-- blockJoin: {0} & {1} = {2}".format(posBlockVal, posBlockValTarget, posBlockJoin))

			if posBlockJoin > 1:
				posBlocksExt.append({
					"primalValue": posBlockJoin,
					"blockInSeqIndex": blockIndex
				})
		# 	else:
		# 		#print "===> IGNORE GCD:", posBlock, posBlockTarget
		# else:
		# 	#print "===> IGNORE BLOCK INDEX:", posBlock, posBlockTarget
	return posBlocksExt


# Calculate extension of each sequence block
def computeSingleBlockOfSequence(key, targetKey, 
	seqBlock, seqBlockTarget, 
	posOffsets, posOffsetsTarget, 
	posBlocks, posBlocksTarget, 
	lastOffset, isSeqExt, DEBUG=False):

	seqBlockExt 	= computeGCDOfPrimalsValue( seqBlock, seqBlockTarget )
	# if DEBUG:
	print("== seqBlock: {0} & {1} = {2}".format(seqBlock, seqBlockTarget, seqBlockExt))
	# print("=== posBlocks {0}\n=== posBlocksTarget {1}".format(posBlocks, posBlocksTarget))
		
	
	if seqBlockExt == 1:
		return 1, [], [], lastOffset

	# #print "key {0} target {1} - checking seqJoin {2}".format(key, targetKey, seqBlockExt)
	# #print "seqBlock: {0} - targetBlock: {1}".format(seqBlock, seqBlockTarget) 

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
			print("Checking:" + posOffsets + " " + posOffsetsTarget)

		encode 				= posOffsets[lazyPosOffsetIndex]["seqPrimeIndex"]
		encodeTarget 	= posOffsetsTarget[lazyPosOffsetIndexTarget]["seqPrimeIndex"]

		# Move the pointer to the right if not correct primal block
		while seqBlockExt % encode != 0 and lazyPosOffsetIndex < posOffsetsLength - 1:
			lazyPosOffsetIndex += 1
			encode = posOffsets[lazyPosOffsetIndex]["seqPrimeIndex"]

		if lazyPosOffsetIndex == posOffsetsLength:
			return (seqBlockExt, posOffsetsExt, posBlocksExt, lastOffset)

		# Move the pointer to the right if not correct primal block
		while seqBlockExt % encodeTarget != 0 and lazyPosOffsetIndexTarget < posOffsetsLengthTarget - 1:
			lazyPosOffsetIndexTarget += 1
			encodeTarget = posOffsetsTarget[lazyPosOffsetIndexTarget]["seqPrimeIndex"]

		if lazyPosOffsetIndexTarget == posOffsetsLengthTarget:
			return (seqBlockExt, posOffsetsExt, posBlocksExt, lastOffset)

		posOffset = posOffsets[lazyPosOffsetIndex]
		posOffsetTarget = posOffsetsTarget[lazyPosOffsetIndexTarget]

		# Make a copy to avoid data be reassigned in calculate... function
		_posBlocks = copy.deepcopy(posBlocks)

		posBlocksJoin = computePosBlocksInSequence(
			key, targetKey, 
			posOffset, posOffsetTarget, _posBlocks, posBlocksTarget, 
			isSeqExt, DEBUG)
		posBlocksJoinLength = len(posBlocksJoin)

		if DEBUG:
			print("posBlocksJoin: {0}".format(posBlocksJoin))

		# No empty block
		if posBlocksJoinLength > 0:
			posBlocksExt += posBlocksJoin
			
			posOffsetsExt.append({
				"blockStartOffset": lastOffset,
				"numberOfBlocksInSeq": posBlocksJoinLength,
				"seqPrimeIndex": encode
			})
			lastOffset += posBlocksJoinLength

		# Remove empty block in sequence if joined before
		elif (encode == encodeTarget and seqBlockExt % encode == 0):
			seqBlockExt /= encode

		lazyPosOffsetIndex 				+= 1
		lazyPosOffsetIndexTarget 	+= 1

	# Avoid empty join block
	if not posBlocksExt:
		return (1, [], [], lastOffset)
	else:
		return (seqBlockExt, posOffsetsExt, posBlocksExt, lastOffset)


'''
		Calculate seq extension of all sequence blocks
'''
def extend(key, targetKey, seqBlocks, seqBlocksTarget,
 posOffsetsList, posOffsetsListTarget, posBlocks, posBlocksTarget, 
 isSeqExt, DEBUG=False):

	seqBlocksExt = []
	posOffsetsListExt = [[]] * len(seqBlocks)
	posBlocksExt = []

	numberOfSeqBlocks = len(seqBlocks)
	lastOffset = 1

	# Loop on sequence block
	for seqIndex in range(0, numberOfSeqBlocks):
		posOffsets 				= posOffsetsList[seqIndex]
		posOffsetsTarget 	= posOffsetsListTarget[seqIndex]

		(seqBlockExt, posOffsetsExt, _posBlocksExt, _lastOffset) = computeSingleBlockOfSequence(
			key, targetKey,
			seqBlocks[seqIndex]	, seqBlocksTarget[seqIndex],
			posOffsetsList[seqIndex], posOffsetsListTarget[seqIndex],
			posBlocks, posBlocksTarget, lastOffset,
			isSeqExt, DEBUG
		)

		if DEBUG:
			print("== SeqExt: {0}".format(seqBlockExt))

		_lastOffset = lastOffset
		seqBlocksExt.append(seqBlockExt)
		posOffsetsListExt[seqIndex] += posOffsetsExt
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




