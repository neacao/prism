#!/usr/bin/env python3

import json, os

# Characters
CHARACTER_INDEX = 0
CHARACTER = []

# Generate character to encoded the course's name
for c in ['0', '1', '2', '3', '4']:
	for index in range(65, 91):
		char = chr(index) + c
		CHARACTER.append(char)


# Called from src/run
with open("./env.dev") as fp:
	configInfo = json.load(fp)


############################## Public Funtions ##############################
def getLabel(courseName):
	ret = ""
	global CHARACTER
	global CHARACTER_INDEX
	global LABEL
	
	# Return if exist in dictionary
	if courseName in LABEL:
		ret = LABEL[courseName]

	# Cache new labeling, will be saved by cacheLabel()
	else:
		value = CHARACTER[CHARACTER_INDEX]
		CHARACTER_INDEX += 1
		LABEL[courseName] = value
		ret = value
		
	return ret


def cacheLabel():
	labelEncodedPath = configInfo["LABEL_ENCODED_PATH"]
	labelMappingPath = configInfo["LABEL_MAPPING_PATH"]
	encodedLabel = [str(LABEL[key]) for key in LABEL]
	encodedLabel = sorted(encodedLabel)

	with open(labelEncodedPath, "w") as fp:
		fp.write("{0}".format(encodedLabel))

	with open(labelMappingPath, "w") as fp:
		json.dump(LABEL, fp, ensure_ascii=False, indent=2, sort_keys=True)

	return
	
	
def loadLabel():
	labelMappingPath = configInfo["LABEL_MAPPING_PATH"]

	if not os.path.exists(labelMappingPath):
		print("The File {0} it's not created ".format(labelMappingPath))
		with open(labelMappingPath, "w+") as fp:
			fp.write("{\n}")
		print("The file {0} has been Created ...".format(labelMappingPath))

	result = {}
	with open(labelMappingPath, "r") as fp:
		result = json.load(fp)

	return result


def numberOfLabels():
	return len(LABEL)


LABEL = loadLabel()





