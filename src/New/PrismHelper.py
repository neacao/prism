#!/usr/bin/env python3

import openpyxl, json, sys
sys.path.insert(0, './Item')

from PrismEncodedItem import PrismEncodedItem
from PositionEncodedItem import PositionEncodedItem

class PrismHelper:
	def __init__(self):
		self.primeArray = [2, 3, 5, 7]
		self.primeLength = len(self.primeArray)
		# self.items = list(range(1, 442)) # Based on data/lite/CourseGradeMap.json last value
		self.items = ['a', 'b', 'c'] # Testing purposed
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
		offset.append(curOffsetIdx)

		primeArrayCounter = 0 # Start index
		primalBlocksListLength = len(primalBlocksList)		

		for idx in range(0, primalBlocksListLength):
			primalBlocks = primalBlocksList[idx] # Single sequence
			primeArrayCounter += 1

			length = len(primalBlocks)
			curOffsetIdx += length

			if primeArrayCounter == self.primeLength or idx == primalBlocksListLength - 1:
				# If last one is empty remove it
				if length == 0:
					offsets.append(offset[:-1])
					offset = offset[-1:len(offset)]
				else:
					offsets.append(offset)
					offset = []
				# -
				primeArrayCounter = 0

			if length == 0:
				continue

			posItems += map(lambda _idx: 
				PositionEncodedItem(primalBlocks[_idx], _idx),
				range(0, len(primalBlocks))
			)
			offset.append(curOffsetIdx)
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
# --- PrismHelper


def testFunction():
	helper = PrismHelper()
	string = [
		"a.b->b->b->a.b->b->a",
		"a.b->b->b",
		"b->a.b",
		"b->b->b",
		"a.b->a.b->a.b->a->b.c"
	]

	prismItems = helper.createFullPrimalEncoded("./CourseGradeEncodedHorizontalTest.json")
	for item in prismItems:
		item.description()
# -- 


if __name__ == "__main__":
	litePath = "../../data/lite"
	testFunction()

# ---

















