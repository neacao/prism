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
	now = datetime.datetime.now()
	fileName = "{0}/{1}_trained_{2}".format(trainedFolderPath, major, now.isoformat())
	with open(fileName, "w") as fp:
		json.dump(result, fp, ensure_ascii=False, indent=2, sort_keys=True)
	return


def saveSortedSeq(major, seqs, trainedFolderPath):
	now = datetime.datetime.now()
	fileName = "{0}/{1}_encodeSorted_{2}".format(trainedFolderPath, major, now.isoformat())
	with open(fileName, "w") as fp:
		[fp.write("{0}\n".format(string(seq))) for seq in seqs]
	return



	