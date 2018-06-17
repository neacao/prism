#!/usr/bin/env python2.7

import json

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
	with open("Resource/labelCourseReverse.json", "w") as fp:
		json.dump(LABEL, fp, ensure_ascii=False, indent=2, sort_keys=True)
	return
	
def loadLabel():
	result = {}
	with open("Resource/labelCourseReverse.json", "r") as fp:
		result = json.load(fp)
	return result


# Characters
CHARACTER_INDEX = 0
CHARACTER = []

for c in ['', '1', '2', '3', '4']:
	for index in xrange(65, 91):
		char = chr(index) + c
		CHARACTER.append(char)


# Labeling
LABEL = loadLabel()


# def encodeRawData():
# 	with open("Resource/it.data") as f:
# 		lineContent = f.readlines()
# 		lineContent = [x.strip() for x in lineContent]

# 	jsonObject = {}
# 	reverseObject = {}

# 	for line in lineContent:
# 		components = line.split(" - ")
# 		key = components[1]
# 		value = components[0]

# 		jsonObject[key] = value
# 		reverseObject[value] = key

# 	with open("Resource/label.json", "w") as fp:
# 		json.dump(jsonObject, fp, ensure_ascii=False, indent=4, sort_keys=True)

# 	with open("Resource/labelReverse.json", "w") as fp:
# 		json.dump(reverseObject, fp, ensure_ascii=False, indent=4, sort_keys=True)

# 	return
