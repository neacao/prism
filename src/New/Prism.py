#!/usr/bin/env python3

import copy, sys, os, argparse
sys.path.insert(0, './Item')

from termcolor import colored
from PrismHelper import *
from PrismLookupTable import *
from PositionEncodedItem import *
from OffsetItem import *
from Logger import *
from functools import reduce

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--func', required = False, help = "Function Name")
args = vars(ap.parse_args())

Log = Logger()
helper = PrismHelper()

class Prism:
	def __init__(self, helper):
		self.helper = helper
		self.rankList = RANK
		self.rankSupportList = SUPPORT
		self.rankMaskList = MASK
		self.rankGCDList = GCD
		self.primeArray = PRIME_ARRAY
		self.primeLength = PRIME_LENGTH
		self.seqFound = []
		self.debugCounter = 3
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
		# Log.log(colored('_maskPosItems {}'.format(reduce(lambda ret, info: '{}, '.format(ret) + info, map(lambda item: item.getDescription(), posItems))[:-2]), 'magenta'))

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
		Log.log(colored(' _joinBlocksInSingleSequence', 'cyan'))

		_posItemsProcess = []
		_targetPosItemsProcess = []
		_posItemsJoined = []

		length = offset.length
		_index = offset.value
		targetLength = targetOffset.length
		_targetIndex = targetOffset.value

		if isMask: # If process under mask (seq extend) force posItems process based on targetLength
			# Log.log(colored('items to be input {}'.format(self.helper.getPosItemsStr(posItems)), 'blue'))
			# Log.log(colored('items to be before process {}'.format(self.helper.getPosItemsStr(posItems[_index:(_index+length)])), 'blue'))
			_posItemsProcess = self._maskPosItems(posItems[_index:(_index+length)])
			# Log.log(colored('items to be processed {}'.format(self.helper.getPosItemsStr(_posItemsProcess)), 'blue'))
			
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

		# Log.log('process w/ length: {}'.format(_length))
		# Log.log(colored('start from {} length {}, posItems: {}'.format(
		# 	_index, length, helper.getPosItemsStr(_posItemsProcess)), 'red'))
		# Log.log(colored('start from {} length {}, targetPosItems: {}'.format(
		# 	_targetIndex, targetLength, helper.getPosItemsStr(_targetPosItemsProcess)), 'red'))

		for idx in range(0, _length):
			blockIdx = _posItemsProcess[idx].blockIndex
			targetIdx = _targetPosItemsProcess[idx].blockIndex

			# Make sure they same block index
			if blockIdx == targetIdx:
				posPrimal = _posItemsProcess[idx].value
				targetPrimal = _targetPosItemsProcess[idx].value

				_gcd = self._getGCD(posPrimal, targetPrimal)
				posItem = None

				Log.log('  * pos blocks joining: posPrimal {} targetPrimal {} gcd {}'.format(posPrimal, targetPrimal, _gcd))
				if _gcd > 1:
					Log.log(colored('  * append pos block: {}'.format(_gcd), 'green'))
					posItem = PositionEncodedItem(_gcd, idx, None)
				# -

				if posItem != None:
					if idx > 0 and len(_posItemsJoined) > 1:
						_posItemsJoined[-1].nextPos = posItem
					_posItemsJoined.append(posItem)
				# -

			else:
				Log.log(colored('  * pos blocks joining:', 'white'),
					colored('IGNORE different block idx {} {}'.format(blockIdx, targetIdx), 'yellow'))
			# -

			_index += 1
			_targetIndex += 1
		# -
		Log.log(colored(' _joinBlocksInSingleSequence return:', 'cyan'))
		Log.log(colored(self.helper.getPosItemsStr(_posItemsJoined), 'cyan'))
		Log.log(colored('---', 'cyan'))
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
				Log.log(colored('_extendSingleSeqBlock return:', 'blue'))
				Log.log(colored('  + gcd: {}\n  + posItemsStr:\n{}\n  + offsetStr:\n{}'.format(_gcd, self.helper.getPosItemsStr(_posItems), self.helper.getOffsetsStr(_offsets)), 'green'))
			else :
				Log.log(colored(' - (1) posItemsStr:\n{}\n  + offsetStr:\n{}'.format(self.helper.getPosItemsStr(posItems), self.helper.getOffsetsStr(offsets)), 'white'))
				Log.log(colored(' - (2) targetPosItemsStr:\n{}\n  + targetOffsetStr:\n{}'.format(self.helper.getPosItemsStr(targetPosItems), self.helper.getOffsetsStr(targetOffsets)), 'white'))
			# -
		# -

		def __getOffsetOfPrime(prime, offsets, index):
			while index < len(offsets) and offsets[index].prime % prime != 0 and offsets[index].prime < prime:
				index += 1
			ret = offsets[index] if (index < len(offsets) and offsets[index].prime % prime == 0) else None
			return ret, index
		# -

		gcd = self._getGCD(seqPrimal, targetSeqPrimal)
		_gcd = gcd

		primeIdx = 0
		curOffsetIdx = lastOffsetIdx
		_posItems = []
		_offsets = []
		_offsetIndex = 0
		_targetOffsetIndex = 0

		if gcd == 1:
			Log.log(colored('_extendSingleSeqBlock joined 1 from {} {} -> quick return empty'.format(seqPrimal, targetSeqPrimal), 'red'))
			return gcd, _posItems, _offsets, lastOffsetIdx
		# -

		__printLogs('input')

		positionArray = self.helper.getPositionArrayToLoopWithPrime(gcd)
		positionArrayLengh = len(positionArray)

		for idx in range(0, positionArrayLengh):

			__matchPosition = 1 if positionArray[idx] == 1 else 0 # Determine if this prime is in factorization of gcd
			__prime = self.primeArray[idx] # idx must from 0..<8
			__offset, _offsetIndex = __getOffsetOfPrime(__prime, offsets, _offsetIndex)
			__targetOffset, _targetOffsetIndex = __getOffsetOfPrime(__prime, targetOffsets, _targetOffsetIndex)

			isValid = (__matchPosition == 1 and __offset != None and __targetOffset != None)
			Log.log(' > gcd: {} at primeVal {} -> {}'.format(gcd, __prime, ('Process' if isValid else 'IGNORE') + ' idx {}'.format(idx)))

			if isValid:
				posItemsJoined = self._joinBlocksInSingleSequence(posItems, __offset, targetPosItems, __targetOffset, isMask)

				_offsetIndex += 1
				_targetOffsetIndex += 1
					
				joinedLength = len(posItemsJoined)
				if joinedLength > 0:
					_offsets.append(OffsetItem(curOffsetIdx, joinedLength, __prime))
					_posItems += posItemsJoined
					curOffsetIdx += joinedLength
				else:
					Log.log(colored('_joinBlocksInSingleSequence return empty joined block -> should device gcdToBeReturn {} for {}'.format(_gcd, __prime),'red'))
					_gcd = int(_gcd/__prime)
				# -
			# -
		# -
		__printLogs()
		return _gcd, _offsets, _posItems, curOffsetIdx
	# --


	def _extendSeqBlocks(self, seqPrimals, offsetsList, posItems, targetSeqPrimals, targetOffsetList, targetPosItems, isMask):
		seqJoined = []
		offsetsListJoined = []
		posItemsJoined = []
		lastOffsetIdx = 0

		Log.log(colored('_extendSeqBlocks w/ mask {} ...\nprimal {}'.format(('YES' if isMask else 'NO'),reduce(lambda ret, x: '{}, '.format(ret) + str(x), seqPrimals)), 'red'))
		Log.log(colored('target primal {}'.format(reduce(lambda ret, x: '{}, '.format(ret) + str(x), targetSeqPrimals)),'red'))

		length = min(len(seqPrimals), len(targetSeqPrimals))
		for idx in range(0, length):
			Log.log(colored('_extendSeqBlocks idx {}'.format(idx), 'blue'))

			seq = copy.deepcopy(seqPrimals[idx])
			targetSeq = copy.deepcopy(targetSeqPrimals[idx])
			offsets = copy.deepcopy(offsetsList[idx])
			targetOffsets = copy.deepcopy(targetOffsetList[idx])

			_gcd, _offsets, _posItems, _curOffsetIdx = self._extendSingleSeqBlock(
				seq, offsets, posItems,
				targetSeq, targetOffsets, targetPosItems,
				lastOffsetIdx, isMask)
			# Accept single seq block (8 seqs) to be 1 to process more
			seqJoined.append(_gcd)
			offsetsListJoined.append(_offsets)
			posItemsJoined += _posItems
			lastOffsetIdx = _curOffsetIdx
			Log.log(colored('_extendSeqBlocks idx {} end !'.format(idx), 'blue'))

		return seqJoined, offsetsListJoined, posItemsJoined
	# --


	def extendItems(self, lastSeq, lastItem, fromItemIdx, items, seqPrimals, offsetsList, posItems, allTargetSeqPrimals, allTargetOffsetsList, allTargetPosItems):
		itemLength = len(items)
		_seqPrimals = copy.deepcopy(seqPrimals)
		_offsetsList = copy.deepcopy(offsetsList)
		_posItems = copy.deepcopy(posItems)

		for idx in range(fromItemIdx, itemLength):
			item = items[idx]
			
			targetSeqPrimals = copy.deepcopy(allTargetSeqPrimals[idx])
			targetOffsetsList = copy.deepcopy(allTargetOffsetsList[idx])
			targetPosItems = copy.deepcopy(allTargetPosItems[idx])

			Log.log(colored('-> Extend lastSeq {} - > {} from idx {}'.format(lastSeq, item, fromItemIdx), 'magenta'))
			# Extend sequence 
			seqJoined, offsetsListJoined, posItemsJoined = self._extendSeqBlocks(
				_seqPrimals, _offsetsList, _posItems,
				targetSeqPrimals, targetOffsetsList, targetPosItems,
				True)

			if self._getSupportOfList(seqJoined) > 0: # Could extend seq more
				lastSeq += '->{}'.format(item)
				self.extendItems(lastSeq, item, 0, items, seqJoined, offsetsListJoined, posItemsJoined, 
					allTargetSeqPrimals, allTargetOffsetsList, allTargetPosItems)

				removeLength = len(item) + len('->')
				lastSeq = lastSeq[:-removeLength]
			# -

			# Must not extend same item in itemset extension
			_idx = self.helper.getNextIndexOfItem(item)
			Log.log(colored('_idx {}'.format(_idx), 'red'))
			if _idx == itemLength:
				break

			_item = items[_idx]
			Log.log(colored('-> Extend lastSeq {} . {} from idx {}'.format(lastSeq, _item, fromItemIdx), 'magenta'))
			
			# Extend itemset
			targetSeqPrimals2 = copy.deepcopy(allTargetSeqPrimals[_idx])
			targetOffsetsList2 = copy.deepcopy(allTargetOffsetsList[_idx])
			targetPosItems2 = copy.deepcopy(allTargetPosItems[_idx])

			seqJoined2, offsetsListJoined2, posItemsJoined2 = self._extendSeqBlocks(
				_seqPrimals, _offsetsList, _posItems,
				targetSeqPrimals2, targetOffsetsList2, targetPosItems2,
				False)

			if self._getSupportOfList(seqJoined2) > 0: # Could extend itemset more
				lastSeq += '.{}'.format(_item)
				self.extendItems(lastSeq, _item, _idx, items, seqJoined2, offsetsListJoined2, posItemsJoined2, 
					allTargetSeqPrimals, allTargetOffsetsList, allTargetPosItems)

				removeLength = len(_item) + len('.')
				lastSeq = lastSeq[:-removeLength]
			# -
		# - for
		Log.log(colored('- Extend extension got', 'magenta'))
		Log.log(colored('[x] lastSeq: {}'.format(lastSeq), 'magenta'))
		Log.log('{} \n'.format(lastSeq), diskMode=True)
		exit(1)
	# --

	def extendItemsV2(self, lastSeq, fromItemIdx, items, seqPrimals, offsetsList, posItems, 
		allTargetSeqPrimals, allTargetOffsetsList, allTargetPosItems, isMask):

		for idx in range(fromItemIdx, len(items)):
			_curItem = copy.deepcopy(items[idx])

			_seqPrimals = copy.deepcopy(seqPrimals)
			_offsetsList = copy.deepcopy(offsetsList)
			_posItems = copy.deepcopy(posItems)

			_targetSeqPrimals = copy.deepcopy(allTargetSeqPrimals[idx])
			_targetOffsetsList = copy.deepcopy(allTargetOffsetsList[idx])
			_targetPosItems = copy.deepcopy(allTargetPosItems[idx])

			seqJoined, offsetsListJoined, posItemsJoined = self._extendSeqBlocks(
				_seqPrimals, _offsetsList, _posItems,
				_targetSeqPrimals, _targetOffsetsList, _targetPosItems,
				isMask)

			if self._getSupportOfList(seqJoined) == 0: # Could not extend seq more
				continue

			_lastSeq = copy.deepcopy(lastSeq)
			if isMask:
				_lastSeq += '->{}'.format(_curItem)
			else:
				_lastSeq += '.{}'.format(_curItem)
			# -
			Log.log('{}\n'.format(_lastSeq), forceDisplay=True)
			self.seqFound.append(_lastSeq)

			self.extendItemsV2(_lastSeq, 0, items, seqJoined, offsetsListJoined, posItemsJoined, 
				allTargetSeqPrimals, allTargetOffsetsList, allTargetPosItems, True)

			self.extendItemsV2(_lastSeq, idx + 1, items, seqJoined, offsetsListJoined, posItemsJoined, 
				allTargetSeqPrimals, allTargetOffsetsList, allTargetPosItems, False)
		# -
	# --	
# ---

def train():
	Log.isDebugMode = False
	Log.logFilePath = 'output/mined'
	
	prism = Prism(helper)
	items, seqList = helper.load(defaultMode=True)
	prismItems = list(helper.createFullPrimalEncodedFromData(seqList))

	_idx = items.index('310')

	allSeqPrimals = list(map(lambda element: element.seqPrimals, prismItems))
	allOffsetsList = list(map(lambda element: element.offsets, prismItems))
	allPosItems = list(map(lambda element: element.posItems, prismItems))

	prism.extendItemsV2(items[_idx], 0, items,
		prismItems[_idx].seqPrimals, prismItems[_idx].offsets, prismItems[_idx].posItems,
		allSeqPrimals, allOffsetsList, allPosItems, True)
	
	minedEncodedInfo = reduce(lambda ret, x: '{}\n'.format(ret) + x, prism.seqFound)
	readableArray = helper.parseReadableSeqsMined(prism.seqFound)
	readableInfo = reduce(lambda ret, x: '{}\n'.format(ret) + x, readableArray)
	
	Log.log(minedEncodedInfo, diskMode=True)
	Log.log(readableInfo, diskMode=True)
# --

def predict(minedFilePath):
	predictStr = 'Nhập môn Tin học (B)->Toán A2 (F)'
	Log.log(colored('predict {}'.format(predictStr), 'magenta'), forceDisplay=True)
	predictEncoded = helper.parsePredictRawStringToEncoded(predictStr)
	Log.log(colored('predict encoded {}'.format(predictEncoded), 'magenta'), forceDisplay=True)

	with open(minedFilePath, 'r') as fp:
		data = fp.readlines()
	seqs = list(map(lambda x: x.strip(), data))

	seqFound = helper.find(predictEncoded, seqs)
	if len(seqFound) > 0:
		seqFoundReadble = helper.parseReadableSeqsMined(seqFound)

		Log.logFilePath = 'output/predictResult'
		seqFoundReadbleInfo = reduce(lambda ret, x: '{}\n'.format(ret) + x, seqFoundReadble)
		Log.log(seqFoundReadbleInfo, forceDisplay=True, diskMode=True)
	else:
		print("NOT found {}".format(predictEncoded))
	# -
# --

if __name__ == "__main__":
	func = args['func']

	if func == 'train':
		train()
	else:
		predict('output/mined155877044953_test')
	# -