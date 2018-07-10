#!/usr/bin/env python3

import sys, json
import encodeRecord as Encoder
import utils as Util
from env_dev import *

def loadData(major):
	print("-> loadData for major {0}".format(major))

	with open(RECORD_ENCODED_PATH, "r") as fp:
		record = [value.strip() for value in fp.readlines()]
		recordList = decodeRecord(record)

	with open(LABEL_ENCODED_PATH, "r") as fp:
		label = fp.read()
		labelList = decodeLabel(label)

	return recordList, labelList


def decodeRecord(recordEncoded):
	ret = []
	for element in recordEncoded:
		element = element[1:-1] # Remove '[' & ']'
		_array = element.split(', ')
		_array = [x[1:-1] for x in _array]
		ret.append(_array)
	return ret


def decodeLabel(labelEncoded):
	labelEncoded = labelEncoded[1:-1] # Remove '[' & ']'
	_array = labelEncoded.split(', ')
	_array = [x[1:-1] for x in _array]
	return _array


def help():
	print("./dataHandler")
	print("\t... flat_record [ IT ]")
	print("\t... encode [ IT ]")
	print("\t... load_data [ IT ]")
	print("( Leave your configurations in env_[dev|prod].py)")
	return


if __name__ == "__main__":
	args = sys.argv
	if len(args) < 3:
		help()
		exit(0)

	func = args[1]
	major = args[2].lower()
	
	# DATA_PATH = "."
	# RESOURCE_PATH = "Resource/"
	# COURSE_GRADE_PATH = RESOURCE_PATH + "courseGradeSample.xlsx"
	# IGNORE_RECORD_DICT_PATH = RESOURCE_PATH + "ignoreRecordDictSample.json"

	if func == "help":
		help()

	elif func == "flat_record":
		rows = COURSE_ROWS[major]
		startRow = rows["start"]
		endRow = rows["end"]

		Encoder.flatRecord(COURSE_GRADE_PATH, FLAT_RECORD_DICT_PATH, startRow, endRow)

	elif func == "encode":
		rows = COURSE_ROWS[major]
		startRow = rows["start"]
		endRow = rows["end"]	

		Encoder.encode(
			COURSE_GRADE_PATH, RECORD_ENCODED_PATH, IGNORE_RECORD_DICT_PATH,
			startRow, endRow, 4.0, None, None
		)

	elif func == "load_data":
		(record, label) = loadData(major)

	else:
		help()



