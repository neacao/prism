#!/usr/bin/env python

from util import *
from constant import *
from prism_encode import *
from prism_extension import *

def processSeqExtension(result, lastFrequent, items, primalSeqExt, primalPosSeqExt, primalSeqAllIteams, primalsPosAllItems):
	lengthOfItems = len(items)

	for _index in xrange(0, lengthOfItems):
		(_primalSeqExt, _primalPosSeqExt) = seqExtension(lastFrequent, items[_index], primalSeqExt[:], primalSeqAllIteams[_index], primalPosSeqExt[:], primalsPosAllItems[_index])

		supp = countingSupport(_primalSeqExt)
		if supp >= MIN_SUPP:
			lastFrequent += "->{0}".format(items[_index])
			_primalSeqExtClone = _primalSeqExt[:]
			_primalPosSeqExtClone = _primalPosSeqExt[:]

			result.append({
				"frequent": lastFrequent,
				"support": supp
			})

			print "+ Frequent seq: {0}\n".format(lastFrequent)
			processSeqExtension(result, lastFrequent, items, _primalSeqExt[:], _primalPosSeqExt[:], primalSeqAllIteams, primalsPosAllItems)
			# print "----> Before split seq: {0}\n".format(lastFrequent)
			lastFrequent = lastFrequent[:-3]
			print "----> After seq: {0}\n".format(lastFrequent)

		else:
			print "~ Reject: {0}->{1}\n".format(lastFrequent, items[_index])

	return


if __name__ == "__main__":
	primalsPosAllItems = processPrimalEncodingPos()
	primalSeqAllIteams = processPrimalEncodingSeq()

	result = []

	processSeqExtension(result, ITEMS[0], ITEMS, primalSeqAllIteams[0], primalsPosAllItems[0], primalSeqAllIteams, primalsPosAllItems)
	
	for element in result:
		print "{0} - {1}".format(element["frequent"], element["support"])


	# Items extension only



