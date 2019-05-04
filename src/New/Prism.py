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
		self.primeArray = PRIME_ARRAY
		self.primeLength = PRIME_LENGTH
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

	def getGCD(self, val1, val2):
		rankVal1 = self.getRank(val1)
		rankVal2 = self.getRank(val2)
		rankGCD = self.rankGCDList[rankVal1][rankVal2]
		ret = self.rankList[rankGCD]
		return ret
	# --


	def extendItemset(self, item, prismItems, targetItem, targetPrismItems):
		return 1
	# --


	# Refer data/resource/ItemsetExtension.png
	# Can exec under parallel process
	# seqPrimal: array of seq primal value
	# offsets: array of indexing of each pos primal in posItems
	# posItems: all pos primal blocks belong to that item
	def extendItemsetSingleBlock(self, 
		seqPrimal, offsets, posItems,
		targetSeqPrimal, targetOffsets, targetPosItems):

		gcd = self.getGCD(seqPrimal, targetSeqPrimal)

		print('seqPrimal {} - targetSeqPrimal {} - gcd {}'.format(seqPrimal, targetSeqPrimal, gcd))

		primeIdx = 0
		offsetIdx = 0
		itemOffsetLength = len(offsets)
		targetOffsetLength = len(targetOffsets)

		while gcd > 1:
			primeVal = self.primeArray[primeIdx]
			print('> gcd: {}'.format(gcd))
			if gcd % primeVal == 0: # Valid block to count pos blocks
				# Get pos blocks to calculate
				print('> Process at {}'.format(primeIdx))
				startIndex = offsets[primeIdx].value
				length = min(offsets[primeIdx].length, targetOffsets[primeIdx].length)
				endIndex = startIndex + length
				print('> startIndex {} - endIndex {}'.format(startIndex, endIndex))

				for idx in range(startIndex, endIndex):
					blockIdx = posItems[idx].blockIndex
					targetIdx = targetPosItems[idx].blockIndex

					# Make sure they same block index
					if blockIdx == targetIdx:
						posPrimal = posItems[idx].value
						targetPrimal = targetPosItems[idx].value

						_gcd = self.getGCD(posPrimal, targetPrimal)
						print('  > pos blocks joining: posPrimal {} targetPrimal {} gcd {}'.format(posPrimal, targetPrimal, _gcd))
					# -
				# -
				print('  < pos blocks joined')
			# -

			gcd /= self.primeArray[primeIdx]
			primeIdx += 1
		# -

		return 1
	# --


	def extendItemset(self, item, seq):
		return 1
	# --


# ---

if __name__ == "__main__":
	helper = PrismHelper(['a', 'b', 'c'])
	prism = Prism(helper)
	prismItems = list(helper.mockup())

	prism.extendItemsetSingleBlock(
		prismItems[0].seqPrimals[0], prismItems[0].offsets[0], prismItems[0].posItems,
		prismItems[1].seqPrimals[0], prismItems[1].offsets[0], prismItems[1].posItems)



