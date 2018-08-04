#!/usr/bin/env python3

import glob, os, json
from run import *

def newest(path):
  files = os.listdir(path)
  paths = [os.path.join(path, basename) for basename in files]
  return max(paths, key=os.path.getctime)

def test():
	# Encode
	Data.processEncode("IT", "env.dev")

	# Remove some labels for faster testing
	with open("env.dev") as fp:
		conf = json.load(fp)
		maxNumberLabels = int(conf["MAX_NUMBER_LABELS"])
		recordEncodedPath = conf["RECORD_ENCODED_PATH"]
		labelEncodedPath = conf["LABEL_ENCODED_PATH"]
	
	(sequences, items) = Data.loadData(recordEncodedPath, labelEncodedPath)
	items = ["'{0}'".format(item) for item in items[:maxNumberLabels]]
	itemStr = "[{0}]".format(", ".join(items))
	with open(labelEncodedPath, "w+") as fp:
		fp.write(itemStr)

	# Train
	train("IT", 5, "env.dev")

	# Predict
	print("======================================== TEST PREDICT ========================================")
	trainedPath = newest("./Trained")
	predict(None, "H->A1", 7, trainedPath,  "env.dev")


if __name__ == "__main__":
	test()