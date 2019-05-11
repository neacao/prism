#!/usr/bin/env python3

import copy, sys
sys.path.insert(0, './Item')

from termcolor import colored
from PrismHelper import *
from PrismLookupTable import *
from PositionEncodedItem import *
from OffsetItem import *
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

	def _getRank(self, val):
		try:
			_index = self.rankList.index(val)
			return _index
		except ValueError:
			print("[FATAL ERROR] Not found Rank of this: {0}".format(val))
			exit(1)
	# --

	def _getSupportOfList(self, primalList):
		tempRankList = map(lambda primal: self._getRank(primal), primalList)
		tempRankSupportList = map(lambda rank: self.rankSupportList[rank], tempRankList)
		ret = reduce(lambda val, support: val + support, tempRankSupportList)
		return ret
	# --

	def _getGCD(self, val1, val2):
		rankVal1 = self._getRank(val1)
		rankVal2 = self._getRank(val2)
		rankGCD = self.rankGCDList[rankVal1][rankVal2]
		ret = self.rankList[rankGCD]
		return ret
	# --

	def _getMask(self, val):
		ret = 1
		if val == None:
			ret = self.rankList[-1]
		else:
			rank = self._getRank(val)
			rankMark = self.rankMaskList[rank]
			ret = self.rankList[rankMark]
		return ret
	# --

	def _maskPosItems(self, posItems):
		def _printLog():
			posItemsStr = ""
			for item in posItems:
				posItemsStr += "{}, ".format(item.getDescription())
			print(colored('_maskPosItems {}'.format(posItemsStr[:-2]), 'magenta'))
		# -

		idx = 0
		length = len(posItems)
		ret = copy.deepcopy(posItems)

		while idx < length: # nextPos is blocks in same sequence
			ret[idx].value = self._getMask(ret[idx].value)

			while ret[idx].nextPos != None:
				idx += 1
				ret[idx].value = self._getMask(None)
			# -
			idx += 1
		# -
		return ret
	# --

	def _joinBlocksInSingleSequence(self, startIndex1, startIndex2, length, posItems, targetPosItems, isMask = False):
		_posItemsJoined = []

		print(colored('-- _joinBlocksInSingleSequence', 'cyan'))

		for idx in range(0, length):
			blockIdx = posItems[startIndex1].blockIndex
			targetIdx = targetPosItems[startIndex2].blockIndex

			# Make sure they same block index
			if blockIdx == targetIdx:
				posPrimal = posItems[startIndex1].value
				targetPrimal = targetPosItems[startIndex2].value

				_gcd = self._getGCD(posPrimal, targetPrimal)
				posItem = None

				print('  * pos blocks joining: posPrimal {} targetPrimal {} gcd {}'.format(posPrimal, targetPrimal, _gcd))
				if _gcd > 1:
					print(colored('  * append pos block: {}'.format(_gcd), 'green'))
					posItem = PositionEncodedItem(_gcd, idx, None)
				# -

				if posItem != None:
					if idx > 0:
						_posItemsJoined[-1].nextPos = posItem
					_posItemsJoined.append(posItem)
				# -

			else:
				print(colored('  * pos blocks joining:', 'white'),
					colored('IGNORE different block idx {} {}'.format(blockIdx, targetIdx), 'yellow'))
			# -

			startIndex1 += 1
			startIndex2 += 1
		# -
		# infoStr = 
		# infoStr = reduce(lambda ret, posItemStr: '{}\n'.format(ret) + posItemStr , list(map(lambda x: x.getDescription(), _posItemsJoined)))
		infoStr = helper.getPosItemsStr(_posItemsJoined)
		print(colored('_joinBlocksInSingleSequence w/ posJoined: {} --'.format(infoStr), 'cyan'))
		return _posItemsJoined
	# --

	# Refer data/resource/ItemsetExtension.png
	# Can exec under parallel process
	# seqPrimal: array of seq primal value
	# offsets: array of indexing of each pos primal in posItems
	# posItems: all pos primal blocks belong to that item
	def _extendSingleSeqBlock(self, 
		seqPrimal, offsets, posItems,
		targetSeqPrimal, targetOffsets, targetPosItems,
		isMask = False):

		gcd = self._getGCD(seqPrimal, targetSeqPrimal)
		_gcd = gcd
		print('> seqPrimal {} - targetSeqPrimal {} - gcd {}'.format(seqPrimal, targetSeqPrimal, gcd))

		primeIdx = 0
		curOffsetIdx = 0
		_posItems = []
		_offsets = []

		if gcd == 1:
			return gcd, _posItems, _offsets
		# -

		def __printLogs():
			posItemsStr = helper.getPosItemsStr(_posItems)
			offsetsStr = helper.getOffsetsStr(_offsets)
			print(colored('  + gcd: {}\n  + posItemsStr:\n{}\n  + offsetStr:\n{}'.format(_gcd, posItemsStr, offsetsStr), 'green'))
		# -

		while gcd > 1:
			primeVal = self.primeArray[primeIdx]
			print(' > gcd: {}'.format(gcd))
			if gcd % primeVal == 0:
				# Get pos blocks to calculate
				info = colored(' > Process at {}'.format(gcd, primeIdx), 'magenta')
				print(info)

				length = min(offsets[primeIdx].length, targetOffsets[primeIdx].length)
				startIndex1 = offsets[primeIdx].value
				startIndex2 = targetOffsets[primeIdx].value

				posItemsJoined = self._joinBlocksInSingleSequence(startIndex1, startIndex2, length, posItems, targetPosItems)
				joinedLength = len(posItemsJoined)
				offset = OffsetItem(curOffsetIdx, joinedLength)

				_posItems += posItemsJoined
				_offsets.append(offset)
			# -

			gcd /= self.primeArray[primeIdx]
			primeIdx += 1
		# -
		__printLogs()
		return _gcd, _offsets, _posItems
	# --


	def _extendSeqBlocks(self, 
		seqPrimals, offsetsList, posItems,
		targetSeqPrimals, targetOffsetList, targetPosItems, 
		isMask = False):

		seqJoined = []
		offsetsListJoined = []
		posItemsJoined = []

		length = min(len(seqPrimals), len(targetSeqPrimals))
		for idx in range(0, length):
			print(colored('_extendSeqBlocks idx {}'.format(idx), 'blue'))

			seq = seqPrimals[idx]
			targetSeq = targetSeqPrimals[idx]
			offsets = offsetsList[idx]
			targetOffsets = targetOffsetList[idx]

			_gcd, _offsets, _posItems = self._extendSingleSeqBlock(
				seq, offsets, posItems, 
				targetSeq, targetOffsets, targetPosItems,
				isMask)

			seqJoined.append(_gcd)
			offsetsListJoined.append(_offsets)
			posItemsJoined += _posItems
			print(colored('_extendSeqBlocks -----', 'blue'))

		# -
		return seqJoined, offsetsListJoined, posItemsJoined
	# --
 
# ---

if __name__ == "__main__":
	helper = PrismHelper(['a', 'b', 'c'])
	prism = Prism(helper)
	prismItems = list(helper.mockup())

	_idx = 0
	_targetIdx = 1

	maskPosItems = prism._maskPosItems(prismItems[_idx].posItems)
	prism._extendSeqBlocks(
			prismItems[_idx].seqPrimals, prismItems[_idx].offsets, prismItems[_idx].posItems,
			prismItems[_targetIdx].seqPrimals, prismItems[_targetIdx].offsets, prismItems[_targetIdx].posItems)







