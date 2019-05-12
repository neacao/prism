#!/usr/bin/env python3

import copy, sys
sys.path.insert(0, './Item')

from termcolor import colored
from PrismHelper import *
from PrismLookupTable import *
from PositionEncodedItem import *
from OffsetItem import *
from Logger import *
from functools import reduce

class Prism:
	def __init__(self, helper, logger):
		self.helper = helper
		self.rankList = RANK
		self.rankSupportList = SUPPORT
		self.rankMaskList = MASK
		self.rankGCDList = GCD
		self.primeArray = PRIME_ARRAY
		self.primeLength = PRIME_LENGTH
		self.logger = logger
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
		# self.logger.log(colored('_maskPosItems {}'.format(reduce(lambda ret, info: '{}, '.format(ret) + info, map(lambda item: item.getDescription(), posItems))[:-2]), 'magenta'))

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

	def _maskPosItemsMax(self, index):
		val = self._getMask(None)
		ret = PositionEncodedItem(val, index, None)
		return ret
	# --


	def _joinBlocksInSingleSequence(self, posItems, offset, targetPosItems, targetOffset, isMask):
		self.logger.log(colored('-- _joinBlocksInSingleSequence', 'cyan'))

		_posItemsProcess = []
		_targetPosItemsProcess = []
		_posItemsJoined = []

		length = offset.length
		_index = offset.value
		targetLength = targetOffset.length
		_targetIndex = targetOffset.value

		if isMask: # If process under mask (seq extend) force posItems process based on targetLength
			_posItemsProcess = self._maskPosItems(posItems[_index:(_index+length)])
			
			if length < targetLength:
				for idx in range(length, length+targetLength-1):
					_posItemsProcess.append(self._maskPosItemsMax(idx))
				length = targetLength
			# -
		else:
			_posItemsProcess = copy.deepcopy(posItems[_index:(_index+length)])
		# -
		_targetPosItemsProcess = copy.deepcopy(targetPosItems[_targetIndex:(_targetIndex+targetLength)])
		_length = min(length, targetLength)

		self.logger.log('process w/ length: {}'.format(_length))
		self.logger.log(colored('start from {} length {}, posItems: {}'.format(
			_index, length, helper.getPosItemsStr(_posItemsProcess)), 'red'))
		self.logger.log(colored('start from {} length {}, targetPosItems: {}'.format(
			_targetIndex, targetLength, helper.getPosItemsStr(_targetPosItemsProcess)), 'red'))

		for idx in range(0, _length):
			blockIdx = _posItemsProcess[idx].blockIndex
			targetIdx = _targetPosItemsProcess[idx].blockIndex

			# Make sure they same block index
			if blockIdx == targetIdx:
				posPrimal = _posItemsProcess[idx].value
				targetPrimal = _targetPosItemsProcess[idx].value

				_gcd = self._getGCD(posPrimal, targetPrimal)
				posItem = None

				self.logger.log('  * pos blocks joining: posPrimal {} targetPrimal {} gcd {}'.format(posPrimal, targetPrimal, _gcd))
				if _gcd > 1:
					self.logger.log(colored('  * append pos block: {}'.format(_gcd), 'green'))
					posItem = PositionEncodedItem(_gcd, idx, None)
				# -

				if posItem != None:
					if idx > 0:
						_posItemsJoined[-1].nextPos = posItem
					_posItemsJoined.append(posItem)
				# -

			else:
				self.logger.log(colored('  * pos blocks joining:', 'white'),
					colored('IGNORE different block idx {} {}'.format(blockIdx, targetIdx), 'yellow'))
			# -

			_index += 1
			_targetIndex += 1
		# -
		self.logger.log(colored('_joinBlocksInSingleSequence w/ posJoined: {} --'.format(helper.getPosItemsStr(_posItemsJoined)), 'cyan'))
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
		lastOffsetIdx, isMask):

		def __printLogs(target = 'output'):
			if target == 'output':
				posItemsStr = helper.getPosItemsStr(_posItems)
				offsetsStr = helper.getOffsetsStr(_offsets)
				print(colored('  + gcd: {}\n  + posItemsStr:\n{}\n  + offsetStr:\n{}'.format(_gcd, posItemsStr, offsetsStr), 'green'))
			else :
				print(colored(' - (1) posItemsStr:\n{}\n  + offsetStr:\n{}'.format(helper.getPosItemsStr(posItems), helper.getOffsetsStr(offsets)), 'white'))
				print(colored(' - (2) posItemsStr:\n{}\n  + offsetStr:\n{}'.format(helper.getPosItemsStr(targetPosItems), helper.getOffsetsStr(targetOffsets)), 'white'))
			# -
		# -

		gcd = self._getGCD(seqPrimal, targetSeqPrimal)
		_gcd = gcd

		primeIdx = 0
		curOffsetIdx = lastOffsetIdx
		_posItems = []
		_offsets = []

		if gcd == 1:
			return gcd, _posItems, _offsets
		# -

		while gcd > 1:
			primeVal = self.primeArray[primeIdx]
			isValid = True if gcd % primeVal == 0 else False
			print(' > gcd: {} -> {}'.format(gcd, ('Process' if isValid else 'IGNORE') + ' idx {}'.format(primeIdx)))

			if isValid:
				posItemsJoined = self._joinBlocksInSingleSequence(posItems, offsets[primeIdx], targetPosItems, targetOffsets[primeIdx], isMask)
				joinedLength = len(posItemsJoined)
				if joinedLength > 0:
					_offsets.append(OffsetItem(curOffsetIdx, joinedLength))
					_posItems += posItemsJoined
					curOffsetIdx += joinedLength
				else:
					print(colored('_joinBlocksInSingleSequence return empty joined block -> should device _gcd {} for {}'.format(_gcd, primeVal),'red'))
					_gcd = int(_gcd/primeVal)
				# -
			# -

			gcd /= self.primeArray[primeIdx]
			primeIdx += 1
		# -
		__printLogs()
		return _gcd, _offsets, _posItems, curOffsetIdx
	# --


	def _extendSeqBlocks(self, 
		seqPrimals, offsetsList, posItems,
		targetSeqPrimals, targetOffsetList, targetPosItems, 
		isMask = False):

		seqJoined = []
		offsetsListJoined = []
		posItemsJoined = []
		lastOffsetIdx = 0

		def __printLogs():
			print('seqJoined: {}'.format(seqJoined))
			offsetStr = '['
			for offsets in offsetsListJoined:
				if len(offsets) == 0: 
					offsetStr += '[], '
				else:
					offsetStr += '[' + reduce(lambda ret, _info: '{}, '.format(ret) + _info, map(lambda offset: offset.getDescription(), offsets)) + '], '
			print('offsetsListJoined: {}'.format(offsetStr[:-2]))
			print('posItemsJoined: {}'.format(reduce(lambda ret, info: '{}, '.format(ret) + info, map(lambda posItem: posItem.getDescription(), posItemsJoined))))
		# -

		length = min(len(seqPrimals), len(targetSeqPrimals))
		for idx in range(0, length):
			print(colored('_extendSeqBlocks idx {}'.format(idx), 'blue'))

			seq = seqPrimals[idx]
			targetSeq = targetSeqPrimals[idx]
			offsets = offsetsList[idx]
			targetOffsets = targetOffsetList[idx]

			_gcd, _offsets, _posItems, _curOffsetIdx = self._extendSingleSeqBlock(
				seq, offsets, posItems, 
				targetSeq, targetOffsets, targetPosItems,
				lastOffsetIdx, isMask)

			seqJoined.append(_gcd)
			offsetsListJoined.append(_offsets)
			posItemsJoined += _posItems
			lastOffsetIdx = _curOffsetIdx
			print(colored('_extendSeqBlocks -----', 'blue'))

		# -
		__printLogs()
		return seqJoined, offsetsListJoined, posItemsJoined
	# --


	def _extendItems(self, lastSeq, items):
		return 1
	# --
 	
# ---


if __name__ == "__main__":
	helper = PrismHelper(['a', 'b', 'c'])
	prism = Prism(helper, Logger(True))
	prismItems = list(helper.mockup())

	_idx = 0
	_targetIdx = 1

	maskPosItems = prism._maskPosItems(prismItems[_idx].posItems)
	prism._extendSeqBlocks(
		prismItems[_idx].seqPrimals, prismItems[_idx].offsets, prismItems[_idx].posItems,
		prismItems[_targetIdx].seqPrimals, prismItems[_targetIdx].offsets, prismItems[_targetIdx].posItems,
		True)







