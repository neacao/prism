#!/usr/bin/env python3

import json
from env_dev import *

# Funtions
def getLabel(courseName):
	ret = ""
	global CHARACTER_INDEX
	global CHARACTER_INDEX
	global LABEL
	
	if courseName in LABEL:
		ret = LABEL[courseName]
	else:
		value = CHARACTER[CHARACTER_INDEX]
		CHARACTER_INDEX += 1
		LABEL[courseName] = value
		ret = value
	return ret


def cacheLabel():
	encodedLabel = [str(LABEL[key]) for key in LABEL]
	with open(RESOURCE_PATH + "encodedLabel.data", "w") as fp:
		fp.write("{0}".format(encodedLabel))
	with open(RESOURCE_PATH + "labelMapping.json", "w") as fp:
		json.dump(LABEL, fp, ensure_ascii=False, indent=2, sort_keys=True)
	return
	
	
def loadLabel():
	result = {}
	with open(RESOURCE_PATH + "labelMapping.json", "r") as fp:
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

