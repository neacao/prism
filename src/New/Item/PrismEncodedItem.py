#!/usr/env/bin python3

class PrismEncodedItem:
	def __init__(self, seqPrimals, offsets, posItems):
		self.seqPrimals = seqPrimals
		self.offsets = offsets
		self.posItems = posItems
	# --

	def description(self):
		print('seqPrimals: {}\noffsets: {}'.format(self.seqPrimals, self.offsets))
		posItemStr = ", ".join(map(lambda posItem: posItem.getDescription(), self.posItems))
		print('posItems: {}\n---'.format(posItemStr))
	# --
# ---