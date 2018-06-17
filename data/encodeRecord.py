#!/usr/bin/env python2.7
# coding=utf-8

#http://www.pythonforbeginners.com/basics/getting-user-input-from-the-keyboard
#http://zetcode.com/articles/openpyxl/
import openpyxl
import json, codecs
import sys
import utils as Util

reload(sys)
sys.setdefaultencoding('utf8')


def flatRecord(fileName, fromCell, toCell, replaceDict):

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


if __name__ == "__main__":

	# IT - 2014 -> 2017
	(sequences, studentIDs) = encodeRecord("Resource/courseGrade.xlsx", "A61393", "G72926", 4)
	# sequences = encodeRecord("Resource/courseGradeSample.xlsx", "A1", "G23", 0)

	seqLength = len(sequences)
	with open("Resource/encodedRecord.data", "w") as fp:
		for index in xrange(0, seqLength):
			print "{0:2} {1}".format(studentIDs[index], sequences[index])
			fp.write("{0}\n".format(sequences[index]))

	### Encode the data


	# Flat the record
	# with open("Resource/flatRecordDict.json", "r") as fp:
	# 	replaceDict = json.load(fp)
	# flatRecord("Resource/sampleResult.xlsx", "A1", "G23", replaceDict)




