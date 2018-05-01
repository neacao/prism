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


if __name__ == "__main__":
	primalsPosAllItems = processPrimalEncodingPos()
	primalSeqAllIteams = processPrimalEncodingSeq()

	result = []
	processSeqExtension(result, ITEMS[0], ITEMS, primalSeqAllIteams[0], primalsPosAllItems[0], primalSeqAllIteams, primalsPosAllItems)
	for element in result:
		print "{0} - {1}".format(element["frequent"], element["support"])

	# Items extension only



