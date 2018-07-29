#!/usr/bin/env python3
# coding=utf-8

#http://www.pythonforbeginners.com/basics/getting-user-input-from-the-keyboard
#http://zetcode.com/articles/openpyxl/

import sys, openpyxl, json, os
import utils as Util
import helper as Helper

def flatRecord(fileName, replaceDictPath, fromCell, toCell):
	
	if not os.path.exists(replaceDictPath):
		print("[ERROR] Leave your flat diction at {0}".format(replaceDictPath))
		exit(0)

	with open(replaceDictPath, "r") as fp:
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
	

def encodeRecord(fileName, ignoreDict, fromCell, toCell,
 minGrade, exceptedYear = None, approvedYear = None):
	recordData 	= openpyxl.load_workbook(fileName)
	sheet 			= recordData.active
	cells 			= sheet[fromCell: toCell]
	sequences 	= [[]]
	studentIDs	= []

	counter = 0
	print("Ignore year {0}\nApproved year {1}".format(exceptedYear, approvedYear))

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

		if courseName in ignoreDict:
			print("Ignore courseName {0}".format(courseName))
			continue

		if courseGrade == "NULL" or courseGrade == None: # Special case: user has no course's grade
			print("Ignore unknow course grade: {0}".format(courseGrade))
			continue

		if courseGrade < minGrade:
			print("Ignore courseGrade: {0}".format(courseGrade))
			continue

		if exceptedYear != None and year == exceptedYear:
			print("=> Ignore curYear {0}".format(year))
			continue

		if approvedYear != None and year != approvedYear:
			continue

		counter += 1

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
	
	print("Counter {0}".format(counter))

	Util.cacheLabel()
	sequences = [Helper.sortAdv(seq) for seq in sequences]
	return (sequences, studentIDs)


def encode(resourcePath, encodedPath, ignoreDictPath,
 startRow, endRow,
 minGrade, exceptedYear = None, approvedYear = None):
	
	with open(ignoreDictPath, "r") as fp:
		ignoreDict = json.load(fp)

	(sequences, studentIDs) = encodeRecord(resourcePath, ignoreDict, startRow, endRow,
	 minGrade, exceptedYear, approvedYear)

	seqLength = len(sequences)
	with open(encodedPath, "w") as fp: # JULY 8TH TESTING
		[fp.write("{0}\n".format(seq)) for seq in sequences]
			


