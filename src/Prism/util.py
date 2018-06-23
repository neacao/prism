#!/usr/bin/env python2.7

class string(str):
	
	def sample(self):
		print self, "hello"

	def findAdv(self, word): # This function resolve problem with dot character in Prism itemset
		idx = self.find(word)
		if idx == -1:
			return idx

		# Recaculate position to make sure the words is matching
		realWord = self[idx]
		_idx = idx
		lengOfSelf = len(self)

		while realWord[-1] != "." and _idx < lengOfSelf - 1:
			_idx += 1
			realWord += self[_idx]

		realWord = realWord[:-1] if realWord[-1] == "." else realWord
		return idx if realWord == word else -1


#print string('A.B1.C34').findAdv('B')

