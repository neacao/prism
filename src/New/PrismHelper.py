#!/usr/bin/env python3

import openpyxl, json, sys
sys.path.insert(0, './Item')

from functools import reduce
from PrismEncodedItem import *
from PositionEncodedItem import *
from OffsetItem import *
from PrismLookupTable import *

class PrismHelper:
	def __init__(self, items):
		self.primeArray = PRIME_ARRAY
		self.primeLength = PRIME_LENGTH
		# self.items = list(range(1, 442)) # Based on data/lite/CourseGradeMap.json last value
		self.items = items
	# --

	def convertHorizontalRecord(self, resourcePath, outputPath):
		wb = openpyxl.load_workbook(resourcePath)
		ws = wb.active
		wsRange = ws['A{}:I{}'.format(ws.min_row, ws.max_row)]

		studentIDIdx = 1
		semesterIdx = 3
		encodeIDIdx = 8
		nextSeqSyntax = "->"
		nextPosSyntax = "."
		seqList = []

		curStudentID = "" # Append new string to seqList
		curSemester = 0 # Append new nextSeqSyntax
		curString = "" # To be added into seqList's element

		for row in wsRange:	
			studentID = str(row[studentIDIdx].value)
			semester = row[semesterIdx].value
			encodeVal = str(row[encodeIDIdx].value)

			# New student
			if studentID != curStudentID:
				seqList.append(curString)
				curStudentID = studentID
				curSemester = semester
				curString = encodeVal
			# New semester
			elif semester != curSemester:
				curSemester = semester
				curString += (nextSeqSyntax + encodeVal)
			# New course
			else:
				curString += (nextPosSyntax + encodeVal)
			# -
		# -

		seqList = seqList[1:] # Remove first redundant element
		seqList.append(curString) # Append last student info

		fileOutputPath = '{}/CourseGradeEncodedHorizontal.json'.format(outputPath)
		with open(fileOutputPath, 'w') as fp:
			json.dump(seqList, fp, indent=2)
		return fileOutputPath
	# --


	def createFullPrimalEncoded(self, horizontalRecordPath):
		with open(horizontalRecordPath, 'r') as fp:
			seqList = json.load(fp)

		ret = map(lambda item: self.createPrimalItem(item, seqList), self.items)
		return ret
	# --

	def createPrimalItem(self, item, seqList):
		fullSeqPrimalBlocks = self.createSeqPrimalEncoded(item, seqList)
		fullPosPrimalBlocks = list(map(lambda x: self.createPosPrimalEncoded(item, x), seqList))
		offsets, posItems = self.createPosPrimalEncodedInfo(fullPosPrimalBlocks)
		prismItem = PrismEncodedItem(fullSeqPrimalBlocks, offsets, posItems)
		return prismItem
	# --


	def createPosPrimalEncoded(self, item, sequence):
		itemsetList = sequence.split("->")
		itemsetListLength = len(itemsetList)

		ret = []
		counter = 0

		while counter < itemsetListLength:
			primalVal = 1
			primseIdx = 0

			endIdx = min(itemsetListLength - counter, self.primeLength)
			subItemsetList = itemsetList[counter: counter+endIdx]

			for itemset in subItemsetList:
				if self.doesItemInItemset(item, itemset):
					primalVal *= self.primeArray[primseIdx]
				# -
				primseIdx += 1
			# -
			if primalVal > 1:
				ret.append(primalVal)
			primseIdx = 0
			primalVal = 1
			counter += self.primeLength
		# -
		return ret
	# --

	def createPosPrimalEncodedInfo(self, primalBlocksList):
		offsets = [] # For all seq blocks
		offset = [] # For each seq block
		posItems = []
		curOffsetIdx = 0

		primeArrayCounter = 0 # Start index
		primalBlocksListLength = len(primalBlocksList)

		def appendItemAndOffset(_posItems, _offset, primalBlocks, length):
			previous = None
			length = len(primalBlocks)

			for idx in range(0, length):
				item = PositionEncodedItem(primalBlocks[idx], idx, None)
				posItems.append(item)
				if previous != None:
					previous.nextPos = item
				# -
				previous = item
			# -
			_offset.append(OffsetItem(curOffsetIdx, length))
		# -

		for idx in range(0, primalBlocksListLength):
			primalBlocks = primalBlocksList[idx] # Single sequence
			primeArrayCounter += 1
			length = len(primalBlocks)
			
			if length > 0: # Ignore length is empty
				appendItemAndOffset(posItems, offset, primalBlocks, length)

			if primeArrayCounter == self.primeLength or idx == primalBlocksListLength - 1:
				offsets.append(offset)
				offset = []
				primeArrayCounter = 0
			# -

			if length > 0:
				curOffsetIdx += length
		# -

		return offsets, posItems
	# --


	def createSeqPrimalEncoded(self, item, seqList):
		seqListLength = len(seqList)
		ret = []
		counter = 0

		while counter < seqListLength:
			primalVal = 1
			primeIdx = 0

			endIdx = min(seqListLength - counter, self.primeLength)
			subSeqList = seqList[counter: counter+endIdx]

			for seq in subSeqList:
				if self.doesItemInSequence(item, seq):
					primalVal *= self.primeArray[primeIdx]
				primeIdx += 1
			# -
			ret.append(primalVal)
			counter += self.primeLength
			primalVal = 1
			primeIdx = 0
		# -
		return ret
	# --


	def doesItemInSequence(self, targetItem, sequence):
		itemsetList = sequence.split('->')
		isExist = len([itemset for itemset in itemsetList if self.doesItemInItemset(targetItem, itemset)]) > 0
		return isExist
	# --


	def doesItemInItemset(self, targetItem, itemset):
		itemList = itemset.split(".")
		isExist = len([item for item in itemList if item == targetItem]) > 0
		return isExist
	# --

	def getPosItemsStr(self, posItems):
		info = reduce(lambda ret, posItemStr: '{}\n'.format(ret) + posItemStr , list(map(lambda x: x.getDescription(), posItems)))
		return info
	# --


	def getOffsetsStr(self, offsets):
		ret = ""
		ret += reduce(lambda ret, itemStr: '{}, '.format(ret) + itemStr, list(map(lambda x: x.getDescription(), offsets)))
		# -
		return ret
	# --


	def mockup(self, display=False):
		string = [
			"a.b->b->b->a.b->b->a",
			"a.b->b->b",
			"b->a.b",
			"b->b->b",
			"a.b->a.b->a.b->a->b.c"
		]

		prismItems = self.createFullPrimalEncoded("./ResourceSample.json")
		if display == True:
			# for item in prismItems:
			list(prismItems)[0].description()
		# -
		return prismItems
	# --
# --- PrismHelper


if __name__ == "__main__":
	litePath = "../../data/lite"
	helper = PrismHelper(['a', 'b', 'c'])
	helper.mockup(True)

# ---

















