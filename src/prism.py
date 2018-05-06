#!/usr/bin/env python

from util import *
from constant import *
from prism_encode import *
from prism_extension import *

def processExtension(result, lastFrequent, lastPrimalSeq, lastPrimalsPos, items, primalSeqAllIteams, primalsPosAllItems, isSeqExt):
	lengthOfItems = len(items)

	for index in xrange(0, lengthOfItems):
		curItem = items[index]
		curPrimalSeq = primalSeqAllIteams[index]
		curPrimalPos = primalsPosAllItems[index]

		# Continue if it's in itemset extension with same item
		if isSeqExt == False and lastFrequent.find(curItem) != -1:
			continue

		if isSeqExt == True:
			(primalSeqJoin, primalPosJoin) = seqExtension(lastFrequent, curItem, lastPrimalSeq[:], curPrimalSeq[:], lastPrimalsPos[:], curPrimalPos[:])
		else:
			(primalSeqJoin, primalPosJoin) = itemExtension(lastFrequent, curItem, lastPrimalSeq[:], curPrimalSeq[:], lastPrimalsPos[:], curPrimalPos[:])

		supp = countingSupport(primalSeqJoin)
		if supp >= MIN_SUPP:

			if isSeqExt == True:
				lastFrequent += "->{0}".format(curItem)
			else:
				lastFrequent += "{0}".format(curItem)

			# Ensure to make a copy instead of assign reference
			_lastPrimalSeq = primalSeqJoin[:]
			_lastPrimalsPos = primalPosJoin[:]

			processExtension(result, lastFrequent, _lastPrimalSeq, _lastPrimalsPos, items, primalSeqAllIteams, primalsPosAllItems, True)
			processExtension(result, lastFrequent, _lastPrimalSeq, _lastPrimalsPos, items, primalSeqAllIteams, primalsPosAllItems, False)

			result.append({
				"frequent": lastFrequent,
				"support": supp
			})

			if isSeqExt == True:
				lastFrequent = lastFrequent[:-3]
			else:
				lastFrequent = lastFrequent[:-1]
	return


if __name__ == "__main__":
	primalsPosAllItems = processPrimalEncodingPos()
	primalSeqAllIteams = processPrimalEncodingSeq()

	result = []
	processExtension(result, ITEMS[0], primalSeqAllIteams[0], primalsPosAllItems[0], ITEMS, primalSeqAllIteams, primalsPosAllItems, True)
	processExtension(result, ITEMS[0], primalSeqAllIteams[0], primalsPosAllItems[0], ITEMS, primalSeqAllIteams, primalsPosAllItems, False)
	for element in result:
		print "{0} - {1}".format(element["frequent"], element["support"])

	# Items extension only



