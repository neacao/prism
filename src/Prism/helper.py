#!/usr/bin/env python2.7

class string(str):
	
	def sample(self):
		print self, "hello"


	def findAll(self, word):
		lengOfSelf = len(self)
		return [i for i in range(lengOfSelf) if self.startswith(word, i)]


	def findAdv(self, word): # This function resolve problem with dot character in Prism itemset
		idx = self.find(word)
		if idx == -1:
			return idx

		# Recaculate position to make sure the words is matching
		realWord = self[idx]
		_idx = idx + 1
		lengOfSelf = len(self)

		for index in xrange(_idx, lengOfSelf):
			curChar = self[index]
			if curChar == "." or curChar == "-":
				break
			realWord += curChar

		return idx if realWord == word else -1
