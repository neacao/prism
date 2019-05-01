#!/usr/bin/env python3

import openpyxl, json

class PrismHelper:
	def __init__(self):
		self.primeArray = [2, 3, 5, 7]
		self.primeLength = len(self.primeArray)
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


	def createPrimalBlockEncode(self, horizontalRecordPath):
		return 1
	# --

	# Encode primal blocks for single sequence
	# sequence: a string contain course grade encoded
	# item: numberic value
	def createPrimalEncodedPos(self, item, sequence):
		semesterList = sequence.split("->")
		semesterLenght = len(semesterList)

		counter = 0
		ret = []

		while counter < semesterLenght:
			primalVal = 1
			primseIdx = 0

			for idx in range(0, self.primeLength): # Loop on blocks
				realIdx = idx + counter
				if realIdx == semesterLenght:
					break

				courseList = semesterList[realIdx].split(".")

				for course in courseList:
					if course == item:
						primalVal *= self.primeArray[primseIdx]
						break
				# -
				primseIdx += 1
			# -
			ret.append(primalVal)
			primseIdx = 0
			primalVal = 1
			counter += self.primeLength
		# -
		return ret
	# --

	def createPrimalEncodedSiq(self, item, seqList):
		counter = 0
		seqListLength = len(seqList)
		ret = []

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
		for itemset in itemsetList:
			if self.doesItemInItemset(targetItem, itemset):
				return True
		# -
		return False
	# --

	def doesItemInItemset(self, targetItem, itemset):
		itemList = itemset.split(".")
		for item in itemList:
			if targetItem == item:
				return True
		# -
		return False
	# --

# --- PrismHelper


if __name__ == "__main__":
	litePath = "../../data/lite"
	helper = PrismHelper()
	helper.convertHorizontalRecord('{}/CourseGradeEncoded.xlsx'.format(litePath), litePath)

	# Using block w/ length 4 to test -> [2, 3, 5, 7]
	string = [
		"a.b->b->b->a.b->b->a",
		"a.b->b->b",
		"b->a.b",
		"b->b->b",
		"a.b->a.b->a.b->a->b.c"
	]

	# for sub in string:
	# 	helper.createPrimalEncodedPos('a', sub)
	helper.createPrimalEncodedSiq('b', string)

# ---

















