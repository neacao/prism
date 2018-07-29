#!/usr/bin/env python3

import sys, json, argparse
import recordHandler as Encoder


# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--func", required=True, help="function want to run")
# ap.add_argument("-m", "--major", required=False, help="major will process")
# ap.add_argument("-p", "--configurePath", required=False, help=".env file path")
# args = vars(ap.parse_args())


def loadData(major, configurePath):

	conf = loadConfiguration(configurePath)
	recordEncodedPath = conf["RECORD_ENCODED_PATH"]
	labelEncodedPath = conf["LABEL_ENCODED_PATH"]

	print("-> loadData for major {0}".format(major))

	with open(recordEncodedPath, "r") as fp:
		record = [value.strip() for value in fp.readlines()]
		recordList = decodeRecord(record)

	with open(labelEncodedPath, "r") as fp:
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


def usage():
	print("./dataHandler")
	print("\t... -f flat_record -m [ IT ] -p [.env path]")
	print("\t... -f encode -m [ IT ] -p [.env path]")
	print("\t... -f load_data -m [ IT ] -p [.env path]")
	return


def loadConfiguration(path):
	with open(path) as fp:
		conf = json.load(fp)
	return conf


def processFlatRecord(major, conf):
	rows 			= conf["COURSE_ROWS"][major]
	startRow 	= rows["start"]
	endRow 		= rows["end"]

	print("> Start flat record ...")
	Encoder.flatRecord(COURSE_GRADE_PATH, FLAT_RECORD_DICT_PATH, startRow, endRow)
	print(">> Flat record done !")
	return


def processEncode(major, conf):
	rows 			= conf["COURSE_ROWS"][major]
	startRow 	= rows["start"]
	endRow 		= rows["end"]

	courseGradePath 		= conf["COURSE_GRADE_PATH"]
	recordEncodedPath 	= conf["RECORD_ENCODED_PATH"]
	ignoreRecordPath 		= conf["IGNORE_RECORD_DICT_PATH"]

	print("> Start encoding ...")
	Encoder.encode(
		courseGradePath, recordEncodedPath, ignoreRecordPath,
		startRow, endRow, 4.0, None, None
	)
	print(">> Encode done !")
	return


def process(func, major, configurePath):
	if func == "help":
		usage()

	elif func == "encode":
		conf = loadConfiguration(configurePath)
		processEncode(major, conf)

	elif func == "flat_record":
		conf = loadConfiguration(configurePath)
		processFlatRecord(major, conf)

	elif func == "load_data":
		(record, label) = loadData(major, conf)
		return (record, label)

	return


# if __name__ == "__main__":
# 	func = args["func"]
# 	major = args["major"]
# 	configurePath = args["configurePath"]
	
# 	process(func, major, configurePath)



