#!/usr/bin/env python3

from termcolor import colored
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
		print('> seqPrimal {} - targetSeqPrimal {} - gcd {}'.format(seqPrimal, targetSeqPrimal, gcd))

		primeIdx = 0
		offsetIdx = 0

		while gcd > 1:
			primeVal = self.primeArray[primeIdx]
			print(' > gcd: {}'.format(gcd))
			if gcd % primeVal == 0: # Valid block to count pos blocks
				# Get pos blocks to calculate
				print(' > Process at {}'.format(primeIdx))

				length = min(offsets[primeIdx].length, targetOffsets[primeIdx].length)

				startIndex1 = offsets[primeIdx].value
				startIndex2 = targetOffsets[primeIdx].value

				for tempIdx in range(0, length): # No need to process tempIdx
					blockIdx = posItems[startIndex1].blockIndex
					targetIdx = targetPosItems[startIndex2].blockIndex

					# Make sure they same block index
					if blockIdx == targetIdx:
						posPrimal = posItems[startIndex1].value
						targetPrimal = targetPosItems[startIndex2].value

						_gcd = self.getGCD(posPrimal, targetPrimal)
						print('  > pos blocks joining: posPrimal {} targetPrimal {} gcd {}'.format(posPrimal, targetPrimal, _gcd))
					else:
						print(colored('  > pos blocks joining:', 'white'),
							colored('IGNORE different block idx {} {}'.format(blockIdx, targetIdx), 'red'))
					# -

					startIndex1 += 1
					startIndex2 += 1
				# -
				print('  < pos blocks joined')
			# -

			gcd /= self.primeArray[primeIdx]
			primeIdx += 1
		# -
		print(colored('--- extendItemsetSingleBlock', 'magenta'))
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

	_idx = 0
	_targetIdx = 1

	for idx in range(0, 2):
		prism.extendItemsetSingleBlock(
			prismItems[_idx].seqPrimals[idx], prismItems[_idx].offsets[idx], prismItems[_idx].posItems,
			prismItems[_targetIdx].seqPrimals[idx], prismItems[_targetIdx].offsets[idx], prismItems[_targetIdx].posItems)
	# -

	



