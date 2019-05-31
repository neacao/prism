

class PrismEncodedItem:
	def __init__(self, seqPrimals, offsets, posItems):
		self.seqPrimals = seqPrimals
		self.offsets = offsets
		self.posItems = posItems
	# --

	def description(self):
		print('seqPrimals: {}'.format(self.seqPrimals))
		offsetItemStr =  ""
		for offset in self.offsets:
			tempStr = ", ".join(map(lambda element: element.getDescription(), offset))
			if tempStr != None and tempStr != "":
				offsetItemStr += "[ {} ], ".format(tempStr)
			else:
				offsetItemStr += "[ ], "
			# -
		# -
		
		print('offsets: {}'.format(offsetItemStr))
		posItemStr = ", ".join(map(lambda posItem: posItem.getDescription(), self.posItems))
		print('posItems: {}\n---'.format(posItemStr))
	# --
# ---