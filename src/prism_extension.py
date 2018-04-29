#!/usr/bin/env python

from util import *
from constant import *

def calculatePrimalPos(primalPos, primalPosTarget):
	result = []
	for posIndex in xrange(0, len(primalPos)):
		gcdValue = gcd( primalPos[posIndex], primalPosTarget[posIndex] )
		result.append(gcdValue)

	return result 

##########
# primalsPos & primalsPosTarget is an 2D array
##########
def itemExtension(key, targetKey, primalsPos, primalsPosTarget, primalSeq, primalSeqTarget):
	if (len(primalsPos) != len(primalsPosTarget) or 
		len(primalSeq) != len(primalSeqTarget)):
		print "[PRISM_SEQ_EXTENSION.ERROR] Invalid input params"
		return 0
 	
	primalsPosJoin = []
	primalSeqJoin = []
	lengthPrimalSeq = len(primalSeq)

	for index in xrange(0, lengthPrimalSeq):
		gcdValue = gcd( primalSeq[index], primalSeqTarget[index] )
		primalSeqJoin.append(gcdValue)

		inverseBitSeq = inverseMultiplyBitEncoding(gcdValue)

		startPosition = index * G_LENGTH
		for posIndex in xrange(startPosition, startPosition + G_LENGTH):
			if inverseBitSeq[posIndex - startPosition] == 1: # key & targetKey appear simultaneously
				primalPosJoin = calculatePrimalPos( primalsPos[posIndex], primalsPosTarget[posIndex] )
				primalsPosJoin.append(primalPosJoin)

	print "[itemExt]: {0}{1}\t".format(key, targetKey),  primalSeqJoin, " - ", primalsPosJoin

	return (primalSeqJoin, primalsPosJoin)


def seqExtension(key, targetKey, primalsPos, primalsPosTarget, primalSeq, primalSeqTarget):
	if (len(primalsPos) != len(primalsPosTarget) or 
		len(primalSeq) != len(primalSeqTarget)):
		print "[PRISM_SEQ_EXTENSION.ERROR] Invalid input params"
		return 0
 	
	primalsPosJoin = []
	primalSeqJoin = []
	lengthPrimalSeq = len(primalSeq)

	for index in xrange(0, lengthPrimalSeq):
		gcdValue = gcd( primalSeq[index], primalSeqTarget[index] )
		primalSeqJoin.append(gcdValue)

		inverseBitSeq = inverseMultiplyBitEncoding(gcdValue)

		startPosition = index * G_LENGTH
		for posIndex in xrange(startPosition, startPosition + G_LENGTH):
			if inverseBitSeq[posIndex - startPosition] == 1: # key & targetKey appear simultaneously
				
				maskPrimalPos = maskPrimalPosition(primalsPos[posIndex])
				primalPosJoin = calculatePrimalPos( maskPrimalPos, primalsPosTarget[posIndex] )
				primalsPosJoin.append(primalPosJoin)

	print "[seqExt]: {0}->{1}\t".format(key, targetKey),  primalSeqJoin, " - ", primalsPosJoin

	return (primalSeqJoin, primalsPosJoin)




















