#!/usr/bin/env python3

import sys, json
import encodeRecord as Encoder
import utils as Util
from env_dev import *


def loadData(major):
	print("-> loadData for major {0}".format(major))

	with open(RESOURCE_PATH + "encodedRecordSample.data", "r") as fp:
		record = [value.strip() for value in fp.readlines()]
		recordList = decodeRecord(record)

	with open(RESOURCE_PATH + "encodedLabelSample.data", "r") as fp:
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
	print("\t... flat_record")
	print("\t... encode [ IT ]")
	print("\t... load_data [ IT ]")
	print("( Leave your configurations in env_[dev|prod].py)")
	return


if __name__ == "__main__":
	args = sys.argv
	if len(args) < 2:
		help()
		exit(0)

	func = args[1]
	
	if func == "help":
		help()

	elif func == "flat_record":
		Encoder.flatRecord(COURSE_GRADE_PATH, "A1", "G23", FLAT_RECORD_DICT_PATH)

	elif func == "encode":
		major = args[2] # FIXME: Need safer
		Encoder.encode(major)

	elif func == "load_data":
		major = args[2] # FIXME: Need safer
		(record, label) = loadData(major)

	else:
		help()



