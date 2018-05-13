#!/usr/bin/env python

import sys, copy
sys.path.insert(0, '/Users/nea/Desktop/Course/src/')

from constant import *
from prism_compute import *
from prism_encode_advance import *
from prism_extension_adv import *

def gcdSeqJoin(primalsSeqExt, primalSeq, primalSeqTarget):
	primalSeqJoin = computeGCDOfPrimalsValue(primalSeq, primalSeqTarget)
	return primalSeqJoin


def getLengthToLoopOnOffsetList(primalPosOffset, primalPosOffsetTarget):
	lengOfOffset = min( len(primalPosOffset), len(primalPosOffsetTarget) )
	return lengOfOffset


def calculatePrimalsPosEachSeq(primalsPosOffset, primalsPosOffsetTarget, primalsPos, primalsPosTarget, isMask = False, isTesting = False):
	# Get the primal pos block length
	numberOfPrimalsPos 			= min( primalsPosOffset["length"], primalsPosOffsetTarget["length"] )
	startOffsetIndex				= primalsPosOffset["offset"]
	startOffsetIndexTarget	= primalsPosOffsetTarget["offset"]

	primalsPosExt = []

	if isMask == True:
		maskValue = computeMaskValueOfPrimalValue( primalsPos[startOffsetIndex - 1]["primalPos"] )
		primalsPos[startOffsetIndex - 1]["primalPos"] = maskValue
		for primalPosIndex in xrange(1, numberOfPrimalsPos):
			primalsPos[primalPosIndex + startOffsetIndex - 1] = maxRankValue()


	for primalPosIndex in xrange(0, numberOfPrimalsPos):
		curPrimalPos 				= primalsPos[primalPosIndex + startOffsetIndex - 1]
		curPrimalPosTarget 	= primalsPosTarget[primalPosIndex + startOffsetIndexTarget - 1]

		curPrimalPosBlockIndex = curPrimalPos["blockIndex"]
		curPrimalPosBlockIndexTarget = curPrimalPosTarget["blockIndex"]

		if curPrimalPosBlockIndex == curPrimalPosBlockIndexTarget:

			curPrimalPosVal 			= curPrimalPos["primalPos"]
			curPrimalPosValTarget = curPrimalPosTarget["primalPos"]

			primalPosExt = computeGCDOfPrimalsValue( curPrimalPosVal, curPrimalPosValTarget )
			if primalPosExt > 1:
				primalsPosExt.append({
					"primalPos": primalPosExt,
					"blockIndex": primalPosIndex
				})

			else:
				print "===> IGNORE GCD:", curPrimalPos, curPrimalPosTarget

		else:
			print "===> IGNORE BLOCK INDEX:", curPrimalPos, curPrimalPosTarget

	return primalsPosExt


def itemExtensionAdv(key, targetKey, 
	primalsSeq, primalsSeqTarget, 
	primalsPosListOffsetList, primalsPosListOffsetListTarget,
	primalsPos, primalsPosTarget):

	if len(primalsSeq) != len(primalsSeqTarget):
		print "[PRISM_SEQ_EXTENSION.ERROR] Invalid input params: \n- {0}\n- {1}".format(primalsSeq, primalsSeqTarget)
		return
 	
	# print "### [itemExt]: {0}{1}".format(key, targetKey)
	# print "| primalsPosList\t\t{0}\n| primalsPosListTarget\t{1}".format(primalsPosList, primalsPosListTarget)
	# print "| primalSeq\t\t{0}\n| primalSeqTarget\t{1}".format(primalSeq, primalSeqTarget)

	primalsSeqExt = []
	primalsPosExt = []
	numberOfBlockSeq 	= len(primalsSeq)
	
	primalsPosOffsetListExt = [[]] * numberOfBlockSeq

	lastPrimalsPosOffsetExt = 1

	# Loop on number of sequence block - each block contain 8 sequences
	for blockSeqIndex in xrange(0, numberOfBlockSeq):
		primalsPosOffsetListExt[blockSeqIndex] = []

		curPrimalSeq 				= primalsSeq[blockSeqIndex]
		curPrimalSeqTarget 	= primalsSeqTarget[blockSeqIndex]

		# Make a join of primal sequence
		primalSeqJoin = gcdSeqJoin(primalsSeqExt, curPrimalSeq, curPrimalSeqTarget)		
		primalsSeqExt.append(primalSeqJoin)

		# Inverse the value to calculate primals position
		bitSeqJoin = inverseMultiplyBitEncodingAdv(primalSeqJoin)
		
		# Get offset block to calculate primals position for each sequence
		curPrimalPosOffsetBlock 			= primalsPosListOffsetList[blockSeqIndex]
		curPrimalPosOffsetBlockTarget = primalsPosListOffsetListTarget[blockSeqIndex]

		# Get lenfth of each offset block
		lengOfOffset = getLengthToLoopOnOffsetList( curPrimalPosOffsetBlock, curPrimalPosOffsetBlockTarget )

		# Loop on each offset block
		for primalPosOffsetIndex in xrange(0, lengOfOffset):
			if bitSeqJoin[primalPosOffsetIndex] & 0x01:

				curPrimalPosOffset 				= curPrimalPosOffsetBlock[primalPosOffsetIndex]
				curPrimalPosOffsetTarget 	= curPrimalPosOffsetBlockTarget[primalPosOffsetIndex]

				primalsPosJoin = calculatePrimalsPosEachSeq(curPrimalPosOffset, curPrimalPosOffsetTarget, primalsPos, primalsPosTarget)
				primalsPosJoinLength = len(primalsPosJoin)

				for primalPos in primalsPosJoin:
					primalsPosExt.append(primalPos)

				primalsPosOffsetListExt[blockSeqIndex].append({
					"length": primalsPosJoinLength,
					"offset": lastPrimalsPosOffsetExt
				})

				lastPrimalsPosOffsetExt += primalsPosJoinLength

	return (primalsSeqExt, primalsPosOffsetListExt, primalsPosExt)


def seqExtensionAdv(key, targetKey,
	primalsSeq, primalsSeqTarget, 
	primalsPosListOffsetList, primalsPosListOffsetListTarget,
	primalsPos, primalsPosTarget):

	if len(primalsSeq) != len(primalsSeqTarget):
		print "[PRISM_SEQ_EXTENSION.ERROR] Invalid input params: \n- {0}\n- {1}".format(primalsSeq, primalsSeqTarget)
		return
 	
	# print "### [itemExt]: {0}{1}".format(key, targetKey)
	# print "| primalsPosList\t\t{0}\n| primalsPosListTarget\t{1}".format(primalsPosList, primalsPosListTarget)
	# print "| primalSeq\t\t{0}\n| primalSeqTarget\t{1}".format(primalSeq, primalSeqTarget)

	primalsSeqExt = []
	primalsPosExt = []
	numberOfBlockSeq 	= len(primalsSeq)
	
	primalsPosOffsetListExt = [[]] * numberOfBlockSeq

	lastPrimalsPosOffsetExt = 1

	# Loop on number of sequence block - each block contain 8 sequences
	for blockSeqIndex in xrange(0, numberOfBlockSeq):
		primalsPosOffsetListExt[blockSeqIndex] = []

		curPrimalSeq 				= primalsSeq[blockSeqIndex]
		curPrimalSeqTarget 	= primalsSeqTarget[blockSeqIndex]

		# Make a join of primal sequence
		primalSeqJoin = gcdSeqJoin(primalsSeqExt, curPrimalSeq, curPrimalSeqTarget)		
		primalsSeqExt.append(primalSeqJoin)

		# Inverse the value to calculate primals position
		bitSeqJoin = inverseMultiplyBitEncodingAdv(primalSeqJoin)
		
		# Get offset block to calculate primals position for each sequence
		curPrimalPosOffsetBlock 			= primalsPosListOffsetList[blockSeqIndex]
		curPrimalPosOffsetBlockTarget = primalsPosListOffsetListTarget[blockSeqIndex]

		# Lazy increase offset index to ignore sequence empty blocks
		curPrimalPosOffsetIndex = 0
		curPrimalPosOffsetIndexTarget = 0

		# Loop on each offset block
		for bitSeqIndex in xrange(0, G_LENGTH_ADVANCE):
			if bitSeqJoin[bitSeqIndex] & 0x01:

				curPrimalPosOffset 				= curPrimalPosOffsetBlock[curPrimalPosOffsetIndex]
				curPrimalPosOffsetTarget 	= curPrimalPosOffsetBlockTarget[curPrimalPosOffsetIndexTarget]

				_primalsPos = copy.deepcopy(primalsPos)

				isTesting = True if bitSeqIndex == 1 else False

				primalsPosJoin = calculatePrimalsPosEachSeq2(curPrimalPosOffset, curPrimalPosOffsetTarget, _primalsPos, primalsPosTarget, True, isTesting)
				primalsPosJoinLength = len(primalsPosJoin)

				if primalsPosJoinLength > 0:
					for primalPos in primalsPosJoin:
						primalsPosExt.append(primalPos)

					primalsPosOffsetListExt[blockSeqIndex].append({
						"length": primalsPosJoinLength,
						"offset": lastPrimalsPosOffsetExt
					})

					lastPrimalsPosOffsetExt += primalsPosJoinLength

				else:
					primalsSeqExt[-1] /= G_ARRAY_ADVANCE[bitSeqIndex]

				curPrimalPosOffsetIndex += 1
				curPrimalPosOffsetIndexTarget += 1
				

	return (primalsSeqExt, primalsPosOffsetListExt, primalsPosExt)


def test():
	(posOffsetsAllItems, primalPosAllItems) = processEncodePrimalPosAdv(ITEMS, SEQUENCES)
	primalSeqAllItems = processEncodePrimalSeqAdv(ITEMS, SEQUENCES)

	(primalsSeqExt, primalsPosOffsetListExt, primalsPosExt) = seqExtensionAdv(
		"a", "b", 
		primalSeqAllItems[0], primalSeqAllItems[1],
		posOffsetsAllItems[0], posOffsetsAllItems[1],
		primalPosAllItems[0], primalPosAllItems[1]
	)

	print primalsSeqExt
	print primalsPosOffsetListExt
	print primalsPosExt



'''
	for index in xrange(0, len(ITEMS)):
		print ITEMS[index], primalSeqAllItems[index], posOffsetsAllItems[index]
		for element in primalPosAllItems[index]:
			print element

	a [30, 2] [[{'length': 2, 'offset': 1}, {'length': 1, 'offset': 3}, {'length': 1, 'offset': 4}], [{'length': 1, 'offset': 5}]]
	{'primalPos': 14, 'blockIndex': 0}
	{'primalPos': 3, 'blockIndex': 1}
	{'primalPos': 2, 'blockIndex': 0}
	{'primalPos': 3, 'blockIndex': 0}
	{'primalPos': 210, 'blockIndex': 0}
	...

	1. Why we need length inside offset
'''
	

if __name__ == "__main__":
	test()






