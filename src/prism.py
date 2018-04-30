#!/usr/bin/env python

from util import *
from constant import *
from prism_encode import *
from prism_extension import *

def processSeqExtension(lastFrequent, items, primalSeqExt, primalPosSeqExt, primalSeqAllIteams, primalsPosAllItems):
	lengthOfItems = len(primalSeqAllIteams)

	for _index in xrange(0, lengthOfItems):
		(_primalSeqExt, _primalPosSeqExt) = seqExtension(lastFrequent, items[_index], primalSeqExt, primalSeqAllIteams[_index], primalPosSeqExt, primalsPosAllItems[_index])
		lastFrequent += "->{0}".format(items[_index])

		if countingSupport(_primalSeqExt) >= MIN_SUPP:
			if _index == 1:
				exit(0)

			print "##### Frequent seq: {0}\n".format(lastFrequent)
			processSeqExtension(lastFrequent, items, _primalSeqExt, _primalPosSeqExt, primalSeqAllIteams, primalsPosAllItems)
		
		else:
			print "######## Reject seq: {0}\n".format(lastFrequent)

	return


if __name__ == "__main__":
	primalsPosAllItems = processPrimalEncodingPos()
	primalSeqAllIteams = processPrimalEncodingSeq()

	processSeqExtension(ITEMS[0], ITEMS, primalSeqAllIteams[0], primalsPosAllItems[0], primalSeqAllIteams, primalsPosAllItems)
	


	# Items extension only



