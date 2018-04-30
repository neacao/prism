#!/usr/bin/env python

from util import *
from constant import *
from prism_encode import *
from prism_extension import *

if __name__ == "__main__":
	fullPrimalPosBlocks = processPrimalEncodingPos()
	fullPrimalSeqBlocks = processPrimalEncodingSeq()

	# result = itemExtension(ITEMS[0], ITEMS[1], fullPrimalPosBlocks[0], fullPrimalPosBlocks[1], fullPrimalSeqBlocks[0], fullPrimalSeqBlocks[1])
	(primalSeqExt, primalPosSeqExt) = seqExtension(ITEMS[0], ITEMS[1], fullPrimalSeqBlocks[0], fullPrimalSeqBlocks[1], fullPrimalPosBlocks[0], fullPrimalPosBlocks[1])
	seqExt2 = seqExtension("a->b", ITEMS[0], primalSeqExt, fullPrimalSeqBlocks[0], primalPosSeqExt , fullPrimalPosBlocks[0])


	#for index in xrange(0, len(ITEMS)):
	#	print ITEMS[index], " ", fullPrimalSeqBlocks[index], "\t", fullPrimalPosBlocks[index]





