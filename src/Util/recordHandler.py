#!/usr/bin/env python3
# coding=utf-8

#http://www.pythonforbeginners.com/basics/getting-user-input-from-the-keyboard
#http://zetcode.com/articles/openpyxl/

import sys, openpyxl, json, os
import utils as Util
import helper as Helper	

def decodeRecord(recordEncoded):
	ret = []
	for element in recordEncoded:
		element = element[1:-1] # Remove '[' & ']'
		_array = element.split(', ')
		_array = [x[1:-1] for x in _array]
		ret.append(_array)
	return ret
# -----


def decodeLabel(labelEncoded):
	labelEncoded = labelEncoded[1:-1] # Remove '[' & ']'
	_array = labelEncoded.split(', ')
	_array = [x[1:-1] for x in _array]
	return _array
# -----


def encodeRecord(fileName, ignoreDict, fromCell, toCell, minGrade):
	recordData 	= openpyxl.load_workbook(fileName)
	sheet = recordData.active
	cells  = sheet[fromCell: toCell]
	sequences = [[]]
	studentIDs = []

	# Index:
	# [Student ID, Year, Semester, N/A, Course's name, Course's grade]
	
	curStudentID 		= cells[0][1].value
	curSemester 		= cells[0][3].value
	sequences[0] 		= []
	sequences[0].append("")
	studentIDs.append(curStudentID)

	for row in cells:
		studentID = row[1].value
		# year = row[2].value
		semester = row[3].value
		courseName = row[5].value
		courseGrade = row[6].value
		
		# if courseName in ignoreDict:
		# 	print("Ignore courseName {0}".format(courseName))
		# 	continue

		if courseGrade == "NULL" or courseGrade == None: # Special case: user has no course's grade
			#print("Ignore unknow course {0} with grade: {1} of student {2}".format(courseName, courseGrade, studentID))
			continue

		if courseGrade < minGrade:
			#print("Ignore course \"{0}\" with grade: {1} of student {2}".format(courseName, courseGrade, studentID))
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
	sequences = [Helper.sortAdv(seq) for seq in sequences]
	return (sequences, studentIDs)
# -----

# Encode the course grade based on A (10 - 8.0) B (7.9 - 6.0) C (5.9 - 4.0) D (3.9 - 0.0)
# resourcePath: path to .xlsx file
def encodeCourseGrade(resourcePath, fromCell, toCell):
	recordData 	= openpyxl.load_workbook(resourcePath)
	sheet = recordData.active
	cells  = sheet[fromCell: toCell]
	courseGradeIndedx = 6
	courseGradeTypeIndex = 7

	for row in cells:
		courseGrade = row[courseGradeIndedx].value
		key = "<unknown>"

		if courseGrade == "NULL" or courseGrade == None or courseGrade < 4.0: # Special case: user has no course's grade
			key = "D"
		elif courseGrade >= 4.0 and courseGrade < 6.0:
			key = "C"
		elif courseGrade >= 6.0 and courseGrade < 8.0:
			key = "B"
		elif courseGrade >= 8.0:
			key = "A"

		row[courseGradeTypeIndex].value = key
	
	recordData.save(resourcePath)
	print("Completed =====")

# - encodeCourseGrade


def encode(resourcePath, encodedPath, ignoreDictPath,
 startRow, endRow, minGrade):
	ignoreDict = None
	if ignoreDictPath:
		with open(ignoreDictPath, "r") as fp:
			ignoreDict = json.load(fp)

	(sequences, studentIDs) = encodeRecord(resourcePath, ignoreDict, startRow, endRow, minGrade)

	seqLength = len(sequences)
	with open(encodedPath, "w") as fp: 
		[fp.write("{0}\n".format(seq)) for seq in sequences]
# -----

def loadData(recordEncodedPath, labelEncodedPath):
	with open(recordEncodedPath, "r") as fp:
		record = [value.strip() for value in fp.readlines()]
		recordList = decodeRecord(record)

	with open(labelEncodedPath, "r") as fp:
		label = fp.read()
		labelList = decodeLabel(label)

	return recordList, labelList
# -----


def flatRecord(resourcePath, replaceDictPath, startRow, endRow):
	
	if not os.path.exists(replaceDictPath):
		print("[ERROR] Leave your flat diction at {0}".format(replaceDictPath))
		exit(0)

	with open(replaceDictPath, "r") as fp:
		replaceDict = json.load(fp)

	recordData = openpyxl.load_workbook(resourcePath)
	sheet = recordData.active
	cells = sheet[startRow: endRow]

	for row in cells:
		courseName = row[5].value
		if courseName in replaceDict:
			row[5].value = replaceDict[courseName]

	recordData.save(resourcePath)
# -----


if __name__ == "__main__":
	encodeCourseGrade("../../data/raw/KHMT_lite.xlsx", "A1", "H248")


