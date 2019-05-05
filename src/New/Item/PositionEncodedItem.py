

class PositionEncodedItem:
	def __init__(self, primal, index, nextPos):
		self.value = primal
		self.blockIndex = index
		self.nextPos = nextPos
	# --

	def description(self):
		print(self.getDescription())
	# --

	def getDescription(self):
		ret = '{{ value: {}, index: {} nextPos: {} }}'.format(self.value, self.blockIndex, self.nextPos)
		return ret
	# --
# ---