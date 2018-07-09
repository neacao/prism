#!/usr/bin/env python3

'''

	This file define all variables needed in development
	MAKE SURE THAT WE ARE TESTIN UNDER IT 2014-2017

'''

DIRECTLY_DEBUG = True

DATA_PATH = "../data"

RESOURCE_PATH = "../data/Resource/"

COURSE_GRADE_PATH = RESOURCE_PATH + "courseGrade.xlsx"

RECORD_ENCODED_PATH = RESOURCE_PATH + "encodedRecordSample.data"

RECORD_ENCODED_PATH_2017 = RESOURCE_PATH + "encodedRecordSample2017.data"

RECORD_ENCODED_PATH_FULL = RESOURCE_PATH + "encodedRecord.data"

LABEL_ENCODED_PATH = RESOURCE_PATH + "encodedLabelSample.data"

# Map with label and course name
LABEL_MAPPING_PATH = RESOURCE_PATH + "labelMappingSample.json"

FLAT_RECORD_DICT_PATH = RESOURCE_PATH + "flatRecordDictSample.json"

# Row indexs
IT_START_ROW = "A61393" # 2014
IT_END_ROW = "G72926" #2017

CS_START_ROW = ""
CS_END_ROW = ""

IS_START_ROW = ""
IS_END_ROW = ""

SE_START_ROW = ""
SE_END_ROW = ""

COURSE_ROWS = {
	"it": {
		"start": IT_START_ROW,
		"end": IT_END_ROW
	},
	"cs": {
		"start": "",
		"end": ""
	},
	"is": {
		"start": "",
		"end": ""
	},
	"se": {
		"start": "",
		"end": ""
	}
}