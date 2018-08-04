#!/usr/bin/env python3

import sys, copy, json

import prism_compute as Computer
import prism_encode_adv as Encoder
import prism_extension_adv as Prism
import recordHandler as Data
import helper as Helper

# --- TRAIN ---
def processExtension(result,
 lastFrequent, lastItemIndex,
 lastSeqBlocks, lastOffsets, lastPosBlocks,
 seqBlocksList, posOffsetsList, posBlocksList, 
 items, isSeqExt, minSup):
	
	lengthOfItems = len(items)

	for itemIndex in range(lastItemIndex, lengthOfItems):
		curItem 							= items[itemIndex]
		seqBlockTarget 				= seqBlocksList[itemIndex]
		posOffsetsListTarget 	= posOffsetsList[itemIndex]
		posBlocksTarget 			= posBlocksList[itemIndex]

		(seqBlocksExt, posOffsetsExt, posBlocksExt) = Prism.extend(
			lastFrequent, curItem,
			lastSeqBlocks, seqBlockTarget,
			lastOffsets, posOffsetsListTarget,
			lastPosBlocks, posBlocksTarget,
			isSeqExt
		)

		supp = Computer.countSupportFromPrimalArray(seqBlocksExt)
		if supp < minSup:
			continue

		if isSeqExt:
			lastFrequent += "->{0}".format(curItem)
			numerOfCharsRemove = 2
		else:
			lastFrequent += ".{0}".format(curItem)
			numerOfCharsRemove = 1

		# Ensure to make a copy instead of assign reference
		_lastSeqBlocks 	= copy.deepcopy(seqBlocksExt)
		_lastPosOffsets = copy.deepcopy(posOffsetsExt)
		_lastPosBlocks 	= copy.deepcopy(posBlocksExt)

		# Sequence extension
		processExtension(result, lastFrequent, 0,
			_lastSeqBlocks, _lastPosOffsets, _lastPosBlocks, 
			seqBlocksList, posOffsetsList, posBlocksList, 
			items, True, minSup)

		# Itemset extension
		processExtension(result, lastFrequent, itemIndex + 1, 
			_lastSeqBlocks, _lastPosOffsets, _lastPosBlocks, 
			seqBlocksList, posOffsetsList, posBlocksList, 
			items, False, minSup)

		result.append({
			"frequent": lastFrequent,
			"support": supp
		})
		print("[x] New frequent {0} has support {1}".format(lastFrequent, supp))

		numerOfCharsRemove += len(curItem)
		lastFrequent = lastFrequent[:-numerOfCharsRemove]
			
	return


def train(major, minSup, configurePath):
	with open(configurePath) as fp:
		conf = json.load(fp)

	trainedFolderPath = conf["TRAINED_FOLDER_PATH"]
	recordEncodedPath = conf["RECORD_ENCODED_PATH"]
	labelEncodedPath 	= conf["LABEL_ENCODED_PATH"]

	print("> Loading data encoded from data/ ...")
	(sequences, items) = Data.loadData(recordEncodedPath, labelEncodedPath)

	print("> Encode all records ...")
	(primalBlocks, posOffsetList) = Encoder.encodePrimalItemsetsAdv(items, sequences)
	seqBlocks = Encoder.encodePrimalSeqsAdv(items, sequences)

	numberOfItems = len(items)
	result = []

	print("> Start training ...")
	for itemIndex in range(0, numberOfItems):
		seqBlockOfItem 			= seqBlocks[itemIndex]
		primalOffetsOfItem 	= posOffsetList[itemIndex]
		primalBlockOfItem 	= primalBlocks[itemIndex]

		print("-> Label {0} is processing ...".format(items[itemIndex]))

		processExtension(result, items[itemIndex], 0,
			seqBlockOfItem , primalOffetsOfItem, primalBlockOfItem, 
			seqBlocks, posOffsetList, primalBlocks,
			items, True, minSup
		)

		processExtension(result, items[itemIndex], itemIndex + 1,
			seqBlockOfItem, primalOffetsOfItem, primalBlockOfItem, 
			seqBlocks, posOffsetList, primalBlocks,
			items, False, minSup
		)

	print("> Training done")
	# for element in result:
	# 	print("{0} - {1}".format(element["frequent"], element["support"]))
	
	Helper.saveTrainedData(result, major, trainedFolderPath)
	return
# --- END TRAIN ---


# --- PREDICT ----
def searchItemset(itemset, itemsetTarget):
	itemsetComponents = itemset.split(".")

	for item in itemsetComponents:
		if Helper.string(itemsetTarget).findAdv(item) == -1:
			return False

	return True


def predict(query, queryEncoded, minSup, trainedDataPath, configurePath):
	if queryEncoded:
		_queryEncoded = queryEncoded
	else:
		with open(configurePath) as fp:
			conf = json.load(fp)
		labelMappingPath 	= conf["LABEL_MAPPING_PATH"]
		_queryEncoded 		= Encoder.encodeQuery(query, labelMappingPath)
	
	trainedDataList = Helper.loadTrainedData(trainedDataPath)

	# Split based on sequence
	itemsetQueryComponents 				= _queryEncoded.split("->")
	itemsetQueryComponentsLength 	= len(itemsetQueryComponents)

	for trainedData in trainedDataList:
		trainedItemsetComponents = trainedData["frequent"].split("->")
		idxQuery = 0

		for itemset in trainedItemsetComponents:
			itemsetQuery = itemsetQueryComponents[idxQuery]
			idxQuery += 1 if searchItemset(itemsetQuery, itemset) else 0

			if idxQuery == itemsetQueryComponentsLength:
				if minSup and int(trainedData["support"]) < minSup:
					continue

				print("{0} - {1}".format(trainedData["frequent"], trainedData["support"]))
				break

	return
# --- END PREDICT ---


# --- SHOW ----
def showTrained(filePath):
	trainedData = Helper.loadTrainedData(filePath)
	[print(item) for item in trainedData]
	return
# --- END SHOW ---




