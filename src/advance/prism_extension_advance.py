#!/usr/bin/env python

import sys
sys.path.insert(0, '/Users/nea/Desktop/Course/src/')

from constant import *
from prism_compute import *
from util import *

def calculatePrimalPosJoinEachSequence(primalPos, primalPosTarget):
	primalPosJoin = [] 

	for index in xrange(0, len(primalPos)):
		primalPosJoin.append( computeGCDOfPrimalsValue( primalPos[index], primalPosTarget[index] ) )

	return primalPosJoin

def itemExtensionAdv(key, targetKey, primalSeq, primalSeqTarget, primalsPos, primalsPosTarget):
	if (len(primalsPos) != len(primalsPosTarget) 
		or len(primalSeq) != len(primalSeqTarget)):
		print "[PRISM_SEQ_EXTENSION.ERROR] Invalid input params"
		return
 	
	# print "### [itemExt]: {0}{1}".format(key, targetKey)
	# print "| primalsPos\t\t{0}\n| primalsPosTarget\t{1}".format(primalsPos, primalsPosTarget)
	# print "| primalSeq\t\t{0}\n| primalSeqTarget\t{1}".format(primalSeq, primalSeqTarget)

	primalSeqExt 	= []
	primalsPosExt = []
	numberOfSeqBlock = len(primalSeq)

	minPrimalsPosLength = min( len(primalsPos), len(primalsPosTarget) )

	# Loop on number of sequence block - each block contain 8 sequences
	for blockIndex in xrange(0, numberOfSeqBlock):

		curPrimalSeq 				= primalSeq[blockIndex]
		curPrimalSeqTarget 	= primalSeqTarget[blockIndex]

		seqGCDValue = computeGCDOfPrimalsValue(curPrimalSeq, curPrimalSeqTarget)
		primalSeqExt.append(seqGCDValue)
		
		bitSeq = inverseMultiplyBitEncodingAdv(seqGCDValue)
		seqStartIndex = blockIndex * G_LENGTH_ADVANCE

		minLength = min(minPrimalsPosLength, seqStartIndex + G_LENGTH_ADVANCE)

		for seqIndex in xrange(seqStartIndex, minLength):
			curPrimalPos 				= primalsPos[seqIndex]
			curPrimalPosTarget 	= primalsPosTarget[seqIndex]

			# Is exist
			if bitSeq[seqIndex - seqStartIndex] & 0x01:
				primalPosJoin = calculatePrimalPosJoinEachSequence( curPrimalPos, curPrimalPosTarget )
				primalsPosExt.append(primalPosJoin)

			else: 
				# primalsPosExt += [1] * len(curPrimalPos)	
				print "Ignore "

	print "|-> [itemExt]: {0}{1}\t".format(key, targetKey),  primalSeqExt, " - ", primalsPosExt
	return (primalSeqExt, primalsPosExt)


def test():
	print itemExtensionAdv("a", "b", [330], [2310], [[182], [2], [3], [1], [210]], [[2310], [30], [6], [30], [330]])
	return 0

if __name__ == "__main__":
	test()






