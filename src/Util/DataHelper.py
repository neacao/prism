#!/usr/bin/env python3

import os, sys, openpyxl, json

class DataHelper:
	def __init__(self, resourceRootPath, courseGradePath):
		self.resourceRootPath = resourceRootPath
		self.courseGradePath = courseGradePath
		self.targetPath = "{}/{}".format(resourceRootPath, courseGradePath)
		self.alphaRange = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F']
	# ---

	# Encoded grade rage [0...10] to [A...F]
	def symbolizeCourseGrade(self):
		fullPath = "{0}/{1}".format(self.resourceRootPath, courseGradePath)
		wb 	= openpyxl.load_workbook(fullPath)
		ws = wb.active
		wsRange = ws['A{}:H{}'.format(ws.min_row, ws.max_row)]

		gradeIdx = 6 # G column
		gradeTypeIdx = 7 # H column

		for row in wsRange:
			key = ""
			grade = row[gradeIdx].value

			if grade == "NULL" or grade == None or grade < 4.0: # Special case: user has no course's grade
				key = "F"
			elif grade >= 4.0 and grade <= 4.9:
				key = "D"
			elif grade >= 5.0 and grade <= 5.4:
				key = "D+"
			elif grade >= 5.5 and grade <= 5.9:
				key = "C"
			elif grade >= 6.0 and grade <= 6.9:
				key = "C+"
			elif grade >= 7.0 and grade <= 7.9:
				key = "B"
			elif grade >= 8.0 and grade <= 8.4:
				key = "B+"
			elif grade >= 8.5 and grade <= 8.9:
				key = "A"
			elif grade >= 9.0 and grade <= 10.0:
				key = "A+"

			row[gradeTypeIdx].value = key
		
		wb.save(fullPath)
	# ---

	# Mapping course ID & name to the output path as json
	def collectCouseID(self, outputPath):
		wb = openpyxl.load_workbook(self.targetPath)
		ws = wb.active
		wsRange = ws['A{}:H{}'.format(ws.min_row, ws.max_row)]

		courseIDIdx = 4 # E
		courseNameIdx = 5 # F
		curCourseID = ""
		curCourseName = ""

		retJson = {} # { id: name, id2: name2, ...}

		for row in wsRange:
			tempCourseID = row[courseIDIdx].value

			if curCourseID != tempCourseID:
				curCourseID = tempCourseID
				curCourseName = row[courseNameIdx].value

				retJson[curCourseID] = curCourseName
			# -
		# -

		fileOutputPath = "{}/IDAndNameMap.json".format(outputPath)
		with open(fileOutputPath, 'w') as f:
			json.dump(retJson, f, ensure_ascii=False, indent=2, sort_keys=True)

		return fileOutputPath
	# ---

	def encodeCourseGrade(self, symbolizedCourseMapPath, outputPath):
		with open(symbolizedCourseMapPath, 'r') as fp:
			symbolizedDict = json.load(fp)

		wb = openpyxl.Workbook()
		ws = wb.active # Using default sheet

		# Write alpha range (A)
		alphaRangeLength = len(self.alphaRange)
		firstCharVal = 67 # 'C'

		for idx in range(0, alphaRangeLength):
			ws['{}1'.format(chr(firstCharVal+idx))] = self.alphaRange[idx]
		# - (A)

		# Write course id & name (B)
		dictLength = len(symbolizedDict)
		startIdx = 2
		for key in symbolizedDict:
			ws['A{}'.format(startIdx)] = symbolizedDict[key]
			ws['B{}'.format(startIdx)] = key
			startIdx += 1
		# - (B)

		# Write course encode by id & alpha (C)
		counter = 1
		firstCharVal = 67 # 'C'
		for row in range(0, dictLength):
			for column in range(0, alphaRangeLength):
				wsAlpha = chr(firstCharVal+column)
				wsNumber = row+2
				ws['{}{}'.format(wsAlpha, wsNumber)] = counter
				counter += 1
		# - (C)
 
		fileOutputPath = '{}/IDAndSymbolizeGradeMap.xlsx'.format(outputPath)
		wb.save(fileOutputPath)
		return fileOutputPath
	# ---

# --- Data Helper


if __name__ == "__main__":
	dataPath = "../../data"
	litePath = "../../data/lite"
	data = DataHelper(dataPath, "resource/KHMT_lite2.xlsx")
	jsonPath = data.collectCouseID(litePath)
	xlsxMappingPath = data.encodeCourseGrade(jsonPath, litePath)

	# Test
	os.system('open {}'.format(xlsxMappingPath))








