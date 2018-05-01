#!/usr/bin/env python

from util import *
from constant import *

def calculatePrimalPos(primalPos, primalPosTarget):
	result = []
	for posIndex in xrange(0, len(primalPos)):
		gcdValue = gcd( primalPos[posIndex], primalPosTarget[posIndex] )
		result.append(gcdValue)

	return result 


def itemExtension(key, targetKey, primalSeq, primalSeqTarget, primalsPos, primalsPosTarget):
	if (len(primalsPos) != len(primalsPosTarget) or 
		len(primalSeq) != len(primalSeqTarget)):
		print "[PRISM_SEQ_EXTENSION.ERROR] Invalid input params"
		print primalsPos
		print primalsPosTarget
		print primalSeq
		print primalSeqTarget
		return
 	
 	print "### [itemExt]: {0}{1}".format(key, targetKey)
	print "| primalsPos\t\t{0}\n| primalsPosTarget\t{1}".format(primalsPos, primalsPosTarget)
	print "| primalSeq\t\t{0}\n| primalSeqTarget\t{1}".format(primalSeq, primalSeqTarget)

	primalsPosJoin = []
	primalSeqJoin = []
	lengthPrimalSeq = len(primalSeq)

	for blockIndex in xrange(0, lengthPrimalSeq):
		gcdValue = gcd( primalSeq[blockIndex], primalSeqTarget[blockIndex] )
		primalSeqJoin.append(gcdValue)

		inverseBitSeq = inverseMultiplyBitEncoding(gcdValue)

		seqStartIndex = blockIndex * G_LENGTH
		for seqIndex in xrange(seqStartIndex, seqStartIndex + G_LENGTH):
			curPrimalPos = primalsPos[seqIndex]
			targetPrimakPos = primalsPosTarget[seqIndex]

			if inverseBitSeq[seqIndex - seqStartIndex] == 1: # key & targetKey appear simultaneously
				primalPosJoin = calculatePrimalPos( curPrimalPos, targetPrimakPos )
				primalsPosJoin.append(primalPosJoin)

			else:
				primalsPosJoin.append( [1] * len(curPrimalPos) ) # Add padding


	print "|-> [itemExt]: {0}{1}\t".format(key, targetKey),  primalSeqJoin, " - ", primalsPosJoin
	return (primalSeqJoin, primalsPosJoin)


def seqExtension(key, targetKey, primalSeq, primalSeqTarget, primalsPos, primalsPosTarget):
	if (len(primalsPos) != len(primalsPosTarget) or 
		len(primalSeq) != len(primalSeqTarget)):
		print "[PRISM_SEQ_EXTENSION.ERROR] Invalid input params"
		return
 	
	print "### [seqExt]: {0}->{1}".format(key, targetKey)
	print "| {0}:\t{1} - {2}".format(key, primalSeq, primalsPos)
	print "| {0}:\t{1} - {2}".format(targetKey, primalSeqTarget, primalsPosTarget)

	primalsPosJoin = []
	primalSeqJoin = []
	lengthPrimalSeq = len(primalSeq)

	for blockIndex in xrange(0, lengthPrimalSeq):
		gcdValue = gcd( primalSeq[blockIndex], primalSeqTarget[blockIndex] )
		# print "  Priaml Seq Join:\t{0} at block {1}".format(gcdValue, index)

		inverseBitSeq = inverseMultiplyBitEncoding(gcdValue)

		seqStartIndex = blockIndex * G_LENGTH
		for seqIndex in xrange(seqStartIndex, seqStartIndex + G_LENGTH):
			maskPrimalPos = maskPrimalPosition(primalsPos[seqIndex])
			primalPosJoin = calculatePrimalPos( maskPrimalPos, primalsPosTarget[seqIndex] )

			# print "gcd( {0}, {1} ) = {2}".format(maskPrimalPos, primalsPosTarget[seqIndex], primalPosJoin)

			# TODO: Improve [ remove empty block ] - keep cur version to test
			if inverseBitSeq[seqIndex - seqStartIndex] == 1: # key appear front of targetKey
				if isEmptyPrimalPos(primalPosJoin) == True:
					gcdValue /= G_ARRAY[seqIndex % G_LENGTH]
					primalsPosJoin.append( [1] * len(primalPosJoin) )

				else:
					primalsPosJoin.append(primalPosJoin)
			else:
				primalsPosJoin.append( [1] * len(primalPosJoin) )

		primalSeqJoin.append(gcdValue)

	print "| Support value: {0}".format(countingSupport(primalSeqJoin))		
	print "|-> [seqExt]: {0}->{1}\t".format(key, targetKey),  primalSeqJoin, " - ", primalsPosJoin
	return (primalSeqJoin, primalsPosJoin)


# Return True if the primalPosJoins are all empty block
def isEmptyPrimalPos(primalPosJoin):
	return True if not list(filter(lambda number: number > 1, primalPosJoin)) else False





















