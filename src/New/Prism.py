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

	def getRank(self, val):
		try:
			_index = self.rankList.index(val)
			return _index
		except ValueError:
			print("[FATAL ERROR] Not found Rank of this: {0}".format(val))
			exit(1)
	# --

	def getSupportOfList(self, primalList):
		tempRankList = map(lambda primal: self.getRank(primal), primalList)
		tempRankSupportList = map(lambda rank: self.rankSupportList[rank], tempRankList)
		ret = reduce(lambda val, support: val + support, tempRankSupportList)
		return ret
	# --


	def getGCDOfValues(self, val1, val2):
		rankVal1 = self.getRank(val1)
		rankVal2 = self.getRank(val2)
		rankGCD = self.rankGCDList[rankVal1][rankVal2]
		ret = self.rankList[rankGCD]
		return ret
	# --

# ---

if __name__ == "__main__":
	prism = Prism(PrismHelper())
	ret = prism.getGCDOfValues(35, 6)
	print(ret)



	