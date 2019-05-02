#!/usr/bin/env python3

class PositionEncodedItem:
	def __init__(self, primal, index):
		self.value = primal
		self.blockIndex = index
	# --

	def description(self):
		print(self.getDescription)
	# --

	def getDescription(self):
		ret = 'value: {}, index: {}'.format(self.value, self.blockIndex)
		return ret
	# --
# ---