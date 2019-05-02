#!/usr/bin/env python3

import openpyxl, json

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


	''' ret = [
		[{seqPrimal:, offsets: []}, 
		{}, 
		...]
	] '''
	def createFullPrimalEncoded(self, horizontalRecordPath):
		with open(horizontalRecordPath, 'r') as fp:
			seqList = json.load(fp)

		ret = []

		for item in self.items:
			primalBlocksList = map(lambda x: self.createPosPrimalEncoded(item, x), seqList)
			offsets, posBlocks = self.createPosPrimalEncodedInfo(primalBlocksList)
			print('offsets: {}'.format(offsets))
			print('posBlocks: {}'.format(posBlocks))
			print('===')
		# -


		return 1
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

	# (offsets, posBlocks) = ([], [{primal: , blockIdx: }])
	# primalBlocksList is an 3D array
	def createPosPrimalEncodedInfo(self, primalBlocksList):
		offsets = []
		posBlocks = []
		curOffsetIdx = 0

		for primalBlocks in primalBlocksList:
			if len(primalBlocks) == 0:
				continue

			offsets.append(curOffsetIdx)

			posBlocks += map(lambda idx: 
				{ 'primal': primalBlocks[idx], 'blockIdx': idx }, 
				range(0, len(primalBlocks))
			)

			curOffsetIdx += len(primalBlocks)
		# -
		return offsets, posBlocks
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


if __name__ == "__main__":
	litePath = "../../data/lite"
	helper = PrismHelper()
	# helper.convertHorizontalRecord('{}/CourseGradeEncoded.xlsx'.format(litePath), litePath)

	# Using block w/ length 4 to test -> [2, 3, 5, 7]
	string = [
		"a.b->b->b->a.b->b->a",
		"a.b->b->b",
		"b->a.b",
		"b->b->b",
		"a.b->a.b->a.b->a->b.c"
	]

	helper.createFullPrimalEncoded("./CourseGradeEncodedHorizontalTest.json")


# ---

















