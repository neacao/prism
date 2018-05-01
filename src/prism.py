#!/usr/bin/env python

from util import *
from constant import *
from prism_encode import *
from prism_extension import *

#####
# PREREQUISITE: ItemSet must be sorted alpha bet
#####
def processItemsetExtension(lastResult, items, primalSeqExt, primalPosSeqExt, primalSeqAllIteams, primalsPosAllItems):
	lengthOfItems = len(items)

	for index in xrange(0, lengthOfItems):
		curItem = items[index]
		lastFrequent = lastResult["frequent"]

		if lastFrequent.find(curItem) != -1:
			continue

		(_primalSeqExt, _primalPosSeqExt) = itemExtension(lastFrequent, curItem, primalSeqExt[:], primalSeqAllIteams[index], primalPosSeqExt[:], primalsPosAllItems[index])

		supp = countingSupport(_primalSeqExt)
		if supp >= MIN_SUPP:
			lastFrequent += "{0}".format(curItem)
			lastResult["frequent"] = lastFrequent

			print "[ITEMSET - ADD] Frequent seq: {0} - Supp: {1}\n".format(lastFrequent, supp)
			processItemsetExtension(lastResult, items, _primalSeqExt[:], _primalPosSeqExt[:], primalSeqAllIteams, primalsPosAllItems)
			lastFrequent = lastFrequent[:-1]

		else:
			print "[ITEMSET - REJECT] Reject: {0}{1}\n".format(lastFrequent, items[index])

	return


def processSeqExtension(result, lastFrequent, items, primalSeqExt, primalPosSeqExt, primalSeqAllIteams, primalsPosAllItems):
	lengthOfItems = len(items)

	for index in xrange(0, lengthOfItems):
		(_primalSeqExt, _primalPosSeqExt) = seqExtension(lastFrequent, items[index], primalSeqExt[:], primalSeqAllIteams[index], primalPosSeqExt[:], primalsPosAllItems[index])

		supp = countingSupport(_primalSeqExt)
		if supp >= MIN_SUPP:
			lastFrequent += "->{0}".format(items[index])

			lastResult = {
				"frequent": lastFrequent,
				"support": supp
			}
			result.append(lastResult)

			print "+ Frequent seq: {0}\n".format(lastFrequent)
			processSeqExtension(result, lastFrequent, items, _primalSeqExt[:], _primalPosSeqExt[:], primalSeqAllIteams, primalsPosAllItems)
			processItemsetExtension(lastResult, items, _primalSeqExt[:], _primalPosSeqExt[:], primalSeqAllIteams, primalsPosAllItems)
			lastFrequent = lastFrequent[:-3]

		else:
			print "~ Reject: {0}->{1}\n".format(lastFrequent, items[index])

	return


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
				lastFrequent += curItem

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
	for element in result:
		print "{0} - {1}".format(element["frequent"], element["support"])

	# Items extension only



