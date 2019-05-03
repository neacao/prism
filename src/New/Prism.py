#!/usr/bin/env python3

from PrismHelper import PrismHelper
from PrismLookupTable import *
from functools import reduce

class Prism:
	def __init__(self, helper):
		self.helper = helper
		self.rankList = RANK
		self.rankSupportList = SUPPORT
		self.rankMaskList = MASK
		self.rankGCDList = GCD
	# --

	def getSupportOfList(self, primalList):
		tempRankList = map(lambda primal: self.rankList.index(primal), primalList)
		tempRankSupportList = map(lambda rank: self.rankSupportList[rank], tempRankList)
		ret = reduce(lambda val, support: val + support, tempRankSupportList)
		return ret
	# --


# ---

if __name__ == "__main__":
	prism = Prism(PrismHelper())
	ret = prism.getSupportOfList([30, 210])
	print(ret)