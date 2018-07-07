#!/usr/bin/env python3
# coding=utf-8

#http://www.pythonforbeginners.com/basics/getting-user-input-from-the-keyboard
#http://zetcode.com/articles/openpyxl/

import sys, openpyxl, json
import utils as Util
from env_dev import *

def flatRecord(fileName, fromCell, toCell, replaceDictPath):

	with open(FLAT_RECORD_DICT_PATH) as fp:
		replaceDict = json.load(fp)

	recordData = openpyxl.load_workbook(fileName)
	sheet = recordData.active
	cells = sheet[fromCell: toCell]

	for row in cells:
		courseName = row[5].value
		if courseName in replaceDict:
			row[5].value = replaceDict[courseName]

	recordData.save(fileName)
	return

def encodeRecord(fileName, fromCell, toCell, minGrade):
	recordData 	= openpyxl.load_workbook(fileName)
	sheet 			= recordData.active
	cells 			= sheet[fromCell: toCell]
	sequences 	= [[]]
	studentIDs	= []

	# Index:
	# 1: Student ID
	# 2: Year
	# 3: Semester
	# 5: Course's name
	# 6: Course's grade
	
	curStudentID 		= cells[0][1].value
	# curYear 			= cells[0][2].value
	curSemester 		= cells[0][3].value
	sequences[0] 		= []
	sequences[0].append("")
	studentIDs.append(curStudentID)

	for row in cells:
		studentID = row[1].value
		year = row[2].value
		semester = row[3].value
		courseName = row[5].value
		courseGrade = row[6].value

		if courseGrade == "NULL": # Special case: user has no course's grade
			continue

		if courseGrade < minGrade:
			continue

		if curStudentID != studentID:
			curStudentID = studentID
			sequences.append([])
			curSemester = semester
			sequences[-1].append("")
			studentIDs.append(curStudentID)

		elif curSemester != semester:
			curSemester = semester
			sequences[-1].append("")

		encodedKey = str(Util.getLabel(courseName)) # Remove unicode
		if len(sequences[-1][-1]) > 0:
			sequences[-1][-1] += "."
		sequences[-1][-1] += encodedKey
	
	Util.cacheLabel()
	return (sequences, studentIDs)


def encode(major):
	
	startRow 	= ""
	endRow 		= ""

	if major == "IT":
		startRow = IT_START_ROW
		encodeRow = IT_END_ROW

	elif major == "CS":
		print("Not implement to encode CS yet")
		return

	elif major == "SE":
		print("Not implement to encode SE yet")
		return 

	elif major == "IS":
		print("Not implement to encode IS yet")
		return

	else:
		print("ERROR: What is this: {0}".format(major))
		return # Quick return

	(sequences, studentIDs) = encodeRecord("Resource/courseGrade.xlsx", startRow, encodeRow, 4)

	seqLength = len(sequences)
	with open("Resource/encodedRecord3.data", "w") as fp:
		for index in range(0, seqLength):
			fp.write("{0}\n".format(sequences[index]))
			# #print "{0:2} {1}".format(studentIDs[index], sequences[index])


if __name__ == "__main__":
	encode("IT")




