

class OffsetItem:
	def __init__(self, value, length):
		self.value = value
		self.length = length
	# --

	def getDescription(self):
		ret = '{{ value: {}, length: {} }}'.format(self.value, self.length)
		return ret
	# ---
# ---