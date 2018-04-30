#!/usr/bin/env python

from util import *
from constant import *
from prism_encode import *
from prism_extension import *

if __name__ == "__main__":
	primalsPosAllItems = processPrimalEncodingPos()
	primalSeqAllIteams = processPrimalEncodingSeq()

	(primalSeqExt, primalPosSeqExt) = seqExtension(ITEMS[0], ITEMS[1], primalSeqAllIteams[0], primalSeqAllIteams[1], primalsPosAllItems[0], primalsPosAllItems[1])
	seqExt2 = seqExtension("a->b", ITEMS[0], primalSeqExt, primalSeqAllIteams[0], primalPosSeqExt , primalsPosAllItems[0])

	





