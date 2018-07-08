#!/usr/bin/env python3

'''

	This file define all variables needed in development
	MAKE SURE THAT WE ARE TESTIN UNDER IT 2014-2017

'''

DATA_PATH = "."

RESOURCE_PATH = "Resource/"

COURSE_GRADE_PATH = RESOURCE_PATH + "courseGradeSample.xlsx"

RECORD_ENCODED_PATH = RESOURCE_PATH + "encodedRecordSample.data"

LABEL_ENCODED_PATH = RESOURCE_PATH + "encodedLabelSample.data"

# Map with label and course name
LABEL_MAPPING_PATH = RESOURCE_PATH + "labelMappingSample.json"

FLAT_RECORD_DICT_PATH = RESOURCE_PATH + "flatRecordDictSample.json"

# Row indexs
IT_START_ROW = "A61393" # 2014
IT_END_ROW = "G72926" #2017 - Should be 2016 and use 2017 to test

CS_START_ROW = ""
CS_END_ROW = ""

IS_START_ROW = ""
IS_END_ROW = ""

SE_START_ROW = ""
SE_END_ROW = ""
