#!/usr/bin/env python3

import sys, argparse
sys.path.insert(0, 'Prism')
sys.path.insert(0, 'Util')


# import prism_compute as Computer
# import prism_encode_adv as Encoder
# import prism_extension_adv as Prism
import prism as Prism
import dataHandler as Data
import helper as Helper

# Common setup
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--func", required = False, help = "function want to run")
ap.add_argument("-m", "--major", required = False, help = "major want to train")
ap.add_argument("-minSup", "--minSupport", required = False, help = "minimun support value that approved")
ap.add_argument("-q", "--query", required = False, help = "the raw query want to predict")
ap.add_argument("-q2", "--queryEncoded", required = False, help = "the query encoded want to predict")
ap.add_argument("-p", "--trainedPath", required = False, help = "the trained data path")
ap.add_argument("-c", "--configurePath", required = False, help = "configure data files path")
args = vars(ap.parse_args())


def usage():
	print("./run")
	print("... -f train -m <major> -c <configure file path> -minSup <minimun support value>" )
	print("... -f predict -q \"<raw query>\" -c <configure file path> -p <trained data path>")
	print("... -f predict -q2 \"<query encoded>\" -c <configure file path> -p <trained data path>")
	print("... -f show -p <trained data path>")
	print("... -f encode -m <major> -c <configure file path>")
	print("... -f flat_record -m <major> -c <configure file path>")
	exit(0)


def parseParam(args):
	func 					= args["func"]
	major 				= args["major"] 				if "major" in args 					else None
	minSup 				= args["minSupport"] 		if "minSupport" in args 		else None
	query 				= args["query"] 				if "query" in args 					else None
	queryEncoded	= args["queryEncoded"] 	if "queryEncoded" in args 	else None
	trainedPath 	= args["trainedPath"]		if "trainedPath" in args 		else None
	configurePath = args["configurePath"] if "configurePath" in args 	else None

	if major:
		major = major.upper()

	if minSup:
		minSup = int(minSup)

	if func == "encode":
		if not major or not configurePath:
			usage()

		Data.processEncode(major, configurePath)

	elif func == "flat_record":
		if not major or not configurePath:
			usage()

		Data.processFlatRecord(major, configurePath) 

	elif func == "train":	
		if not major or not configurePath or not minSup:
			usage()
			
		Prism.train(major, minSup, configurePath)

	elif func == "predict":
		if (not query and not queryEncoded) or (not trainedPath or not configurePath):
			usage()

		Prism.predict(query, queryEncoded, minSup, trainedPath,  configurePath)

	elif func == "show":
		if not trainedPath:
			usage()

		showTrained(trainedPath)

	else:
		usage()


if __name__ == "__main__":
	parseParam(args)
	




