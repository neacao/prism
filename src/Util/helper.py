#!/usr/bin/env python3

import datetime, json

class string(str):
	
	def findAll(self, word):
		lengOfSelf = len(self)
		return [i for i in range(lengOfSelf) if self.startswith(word, i)]


	def findAdv(self, word): # This function resolve problem with dot character in Prism itemset
		idx = self.find(word)
		if idx == -1:
			return idx

		# Recalculate position to make sure the words is matching
		realWord = self[idx]
		_idx = idx + 1
		lengOfSelf = len(self)

		for index in range(_idx, lengOfSelf):
			curChar = self[index]
			if curChar == "." or curChar == "-":
				break
			realWord += curChar

		# print("realWorld {0} - word {1}".format(realWord, word))
		return idx if realWord == word else -1


def sortAdv(sequence):
	# List = [ 'A', 'D.C', ...] - C must appear before D
	numberOfItemsets = len(sequence)
	ret = [None] * numberOfItemsets

	for index in range(0, numberOfItemsets):
		itemset 					= sequence[index]
		componenets 			= itemset.split(".")
		componenetsSorted = list(sorted(componenets))
		strJoined 				= ".".join(componenetsSorted)
		ret[index] 				= strJoined

	return ret
	

def saveTrainedData(result, major, trainedFolderPath):
	ts = datetime.datetime.now().timestamp()
	fileName = "{0}/{1}_trained_{2}".format(trainedFolderPath, major, ts)
	with open(fileName, "w") as fp:
		json.dump(result, fp, ensure_ascii=False, indent=2, sort_keys=True)
	return


def saveSortedSeq(major, seqs, trainedFolderPath):
	ts = datetime.datetime.now().timestamp()
	fileName = "{0}/{1}_encodeSorted_{2}".format(trainedFolderPath, major, ts)
	with open(fileName, "w") as fp:
		[fp.write("{0}\n".format(string(seq))) for seq in seqs]
	return


def loadTrainedData(filePath):
	with open(filePath) as fp:
		trainedData = json.load(fp)
	return trainedData


def parseReadableFromPrismEncodeResult(resultArray, mappingDict):
	if not resultArray or not mappingDict:
		print("resultArray or mappingDict is empty")
		return []

	result = []

	for sequence in resultArray:
		sequenceLength = len(sequence)

		encodedString = ""
		index = 0

		while index < sequenceLength:
			# Check if current char is "." or "-"
			# print("Process index: {0} of sequence {1}".format(index, sequence))
			isDot = (sequence[index] == ".")
			isDash = (sequence[index] == "-" and index+1 < sequenceLength and sequence[index+1] == ">")

			if isDot:
				encodedString += ", "
				index += 0

			elif isDash:
				encodedString += " -> "
				index += 1

			else:
				encodedKey, increaseVal = getKeyFromString(sequence[index:])
				index += increaseVal

				courseName = getKeyFrom(value=encodedKey, dict=mappingDict)
				if courseName:
					encodedString += courseName
				else:
					print("What the heck is this encodedKey: {0} mappingDict: {1}".format(encodedKey, mappingDict))
					exit(0)

			index += 1
		# End while
		result.append(encodedString)

	return result
# ---------------


def getKeyFrom(value, dict):
	for key, val in dict.items(): 
		if val == value: 
			return key 
	return None
# ------


def getKeyFromString(string):
	stringLength = len(string)

	# Empty string
	if stringLength == 0:
		return "", 0

	# Next is empty or "." or "->"
	if stringLength == 1 or string[1] == "." or string[1] == "-":
		return string[0], 0

	# If not here is a numberic [0...9] -> Return 2 characters
	# Currently we just support 2 characters for a course name e.g A1, Z9 ...
	return string[:2], 1 # index should increase 1
# ----------------
	

	