#!/usr/bin/env python3
# coding=utf-8

#http://www.pythonforbeginners.com/basics/getting-user-input-from-the-keyboard
#http://zetcode.com/articles/openpyxl/

import sys, openpyxl, json, os
import utils as Util
from env_dev import *

def flatRecord(fileName, fromCell, toCell, replaceDictPath):
	
	if not os.path.exists(FLAT_RECORD_DICT_PATH):
		print("[ERROR] Leave your flat diction at {0}".format(FLAT_RECORD_DICT_PATH))
		exit(0)

	with open(FLAT_RECORD_DICT_PATH, "r") as fp:
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

		if courseGrade == "NULL" or courseGrade == None: # Special case: user has no course's grade
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


def encode(startRow, endRow):

	(sequences, studentIDs) = encodeRecord(COURSE_GRADE_PATH, startRow, endRow, 4)

	seqLength = len(sequences)
	with open(RECORD_ENCODED_PATH, "w") as fp: # JULY 8TH TESTING
		for index in range(0, seqLength):
			fp.write("{0}\n".format(sequences[index]))


if __name__ == "__main__":
	encode("IT")




