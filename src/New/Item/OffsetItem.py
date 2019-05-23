

class OffsetItem:
	def __init__(self, value, length, primeVal):
		self.value = value
		self.length = length
		self.prime = primeVal
	# --

	def getDescription(self):
		ret = '{{ value: {}, length: {}, prime: {} }}'.format(self.value, self.length, self.prime)
		return ret
	# ---
# ---