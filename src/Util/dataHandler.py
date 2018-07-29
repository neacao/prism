#!/usr/bin/env python3

import sys, json
import recordHandler as Encoder

def loadData(recordEncodedPath, labelEncodedPath):
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


def loadConfiguration(path):
	with open(path) as fp:
		conf = json.load(fp)
	return conf


def processFlatRecord(major, configurePath):
	conf 						= loadConfiguration(configurePath)
	coursePath 			= conf["COURSE_GRADE_PATH"]
	flatRecordPath 	= conf["FLAT_RECORD_DICT_PATH"]
	rows 						= conf["COURSE_ROWS"][major]
	startRow 				= rows["start"]
	endRow 					= rows["end"]

	print("> Start flat record ...")
	Encoder.flatRecord(coursePath, flatRecordPath, startRow, endRow)
	print("=> Flat record done !")
	return


def processEncode(major, configurePath):
	conf = loadConfiguration(configurePath)

	rows 			= conf["COURSE_ROWS"][major]
	startRow 	= rows["start"]
	endRow 		= rows["end"]

	courseGradePath 		= conf["COURSE_GRADE_PATH"]
	recordEncodedPath 	= conf["RECORD_ENCODED_PATH"]
	ignoreRecordPath 		= conf["IGNORE_RECORD_DICT_PATH"]

	print("> Start encoding ...")
	Encoder.encode(
		courseGradePath, recordEncodedPath, ignoreRecordPath,
		startRow, endRow, 4.0)
	print("=> Encode done !")
	return




