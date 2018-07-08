#!/usr/bin/env python3

import json, os
from env_dev import *

# Funtions
def getLabel(courseName):
	ret = ""
	global CHARACTER_INDEX
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
	encodedLabel = [str(LABEL[key]) for key in LABEL]

	with open(LABEL_ENCODED_PATH, "w") as fp:
		fp.write("{0}".format(encodedLabel))

	with open(LABEL_MAPPING_PATH, "w") as fp:
		json.dump(LABEL, fp, ensure_ascii=False, indent=2, sort_keys=True)

	return
	
	
def loadLabel():
	if not os.path.exists(LABEL_MAPPING_PATH):
		print("The File {0} it's not created ".format(LABEL_MAPPING_PATH))
		with open(LABEL_MAPPING_PATH, "w+") as fp:
			fp.write("{\n}")
		print("The file {0} has been Created ...".format(LABEL_MAPPING_PATH))

	result = {}
	with open(LABEL_MAPPING_PATH, "r") as fp:
		result = json.load(fp)

	return result


# Characters
CHARACTER_INDEX = 0

CHARACTER = []

# Generate character to encoded the course's name
for c in ['', '1', '2', '3', '4']:
	for index in range(65, 91):
		char = chr(index) + c
		CHARACTER.append(char)


# Labeling
LABEL = loadLabel()

