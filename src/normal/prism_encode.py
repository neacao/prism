# #!/usr/bin/env python

# import sys
# sys.path.insert(0, '/Users/nea/Desktop/Course/src/')

# from util import *
# from constant import *

# def encodeBitPosition(key, array):
# 	result = []
# 	for element in array:
# 		index = element.find(key)
# 		if index != -1:
# 			result.append(1)
# 		else:
# 			result.append(0)

# 	# Padding 0
# 	length = len(result)
# 	divisibleNumber = findNumberDivisible(length, G_LENGTH)
# 	for index in xrange(length, divisibleNumber):
# 		result.append(0)

# 	if NO_LOGS == False:
# 		print "[Pos Encode Bit]:", result
# 	return result


# def encodePrimalPosition(key, array):
# 	bitEncodedPos = encodeBitPosition(key, array)
# 	result = []
# 	length = len(bitEncodedPos)

# 	for blockIndex in xrange(0, length/G_LENGTH):
# 		index = blockIndex * G_LENGTH
# 		tmp = 1
		
# 		# Testing purpose, using G_LENGTH = 8
# 		if bitEncodedPos[index] == 1: tmp *= 2
# 		if bitEncodedPos[index + 1] == 1: tmp *= 3
# 		if bitEncodedPos[index + 2] == 1: tmp *= 5
# 		if bitEncodedPos[index + 3] == 1: tmp *= 7

# 		result.append(tmp)

# 	if NO_LOGS == False:
# 		print "[Pos Encode Primal]:", result
# 	return result

# def encodeBitSequences(key, sequences):
# 	result = []
# 	for sequence in sequences:
# 			foundFlag = False

# 			for itemset in sequence:
# 				index = itemset.find(key)
# 				if index != -1:
# 					foundFlag = True
# 					break

# 			if foundFlag == True:
# 				result.append(1)
# 			else:
# 				result.append(0)

# 	# Padding 0
# 	length = len(result)
# 	divisibleNumber = findNumberDivisible(length, G_LENGTH)
# 	for index in xrange(length, divisibleNumber):
# 		result.append(0)

# 	if NO_LOGS == False:
# 		print "[Seq Encode Bit]:", result
# 	return result


# def encodePrimalSequences(key, sequences): # Sequences is a 2D array
# 	bitEncodedSequences = encodeBitSequences(key, sequences)
# 	result = []
# 	length = len(bitEncodedSequences)

# 	for blockIndex in xrange(0, length/G_LENGTH):
# 		index = blockIndex * G_LENGTH
# 		tmp = 1
		
# 		# Testing purpose, using G_LENGTH = 4
# 		if bitEncodedSequences[index] == 1: tmp *= 2
# 		if bitEncodedSequences[index + 1] == 1: tmp *= 3
# 		if bitEncodedSequences[index + 2] == 1: tmp *= 5
# 		if bitEncodedSequences[index + 3] == 1: tmp *= 7
# 		result.append(tmp)
	
# 	if NO_LOGS == False:
# 		print "[Seq Encode Primal]:", result
# 	return result


# def processPrimalEncodingPos():
# 	items = ITEMS
# 	sequences = SEQUENCES

# 	fullPrimalPosBlocks = [] * len(items)
# 	for item in items:
# 		itemPrimalBlocks = [] * len(sequences)

# 		# Primal position encode for each item
# 		for sequence in sequences:
# 			# itemPrimalBlocks.append(encodePrimalPosition(item, sequence))
# 			itemPrimalBlocks.append( encodePrimalPosition(item, sequence) )

# 		length = len(sequences)
# 		divisibleNumber = findNumberDivisible(length, G_LENGTH)
# 		for index in xrange(length, divisibleNumber):
# 			itemPrimalBlocks.append( [1] * len(itemPrimalBlocks[0]) ) # Padding

# 		fullPrimalPosBlocks.append(itemPrimalBlocks)


# 	return fullPrimalPosBlocks


# def processPrimalEncodingSeq():
# 	items = ITEMS
# 	sequences = SEQUENCES

# 	fullPrimalSeqBlocks = [] * len(items)
# 	for item in items:
# 		fullPrimalSeqBlocks.append(encodePrimalSequences(item, sequences))
		
# 	return fullPrimalSeqBlocks



# 	