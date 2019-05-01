#!/usr/bin/env python3

import openpyxl, json

class PrismHelper:

	def convertHorizontalRecord(self, resourcePath):
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

		seqList = seqList[1:] # Remove first redundant element
		seqList.append(curString) # Append last student info

		for seq in seqList:
			print('{}\n'.format(seq))
		# -
	# --
# --- PrismHelper


if __name__ == "__main__":
	litePath = "../../data/lite"
	prismHelper = PrismHelper()
	prismHelper.convertHorizontalRecord('{}/CourseGradeEncoded.xlsx'.format(litePath))
# ---

















