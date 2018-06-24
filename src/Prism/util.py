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
		_idx = idx
		lengOfSelf = len(self)

		while realWord[-1] != "." and _idx < lengOfSelf - 1:
			_idx += 1
			realWord += self[_idx]

		realWord = realWord[:-1] if realWord[-1] == "." else realWord
		return idx if realWord == word else -1


	# def findRecursiveAdv(self, word): # This function resolve problem with dot character in Prism itemset
	# 	idx = self.find(word)
	# 	if idx == -1:
	# 		return idx

	# 	# Recaculate position to make sure the words is matching
	# 	realWord = self[idx]
	# 	_idx = idx
	# 	lengOfSelf = len(self)

	# 	while realWord[-1] != char[-1] and _idx < lengOfSelf - 1:
	# 		_idx += 1
	# 		realWord += self[_idx]

	# 	charLength = len(char)

	# 	realWord = realWord[:charLength] if realWord[-1] == char[-1] else realWord
	# 	return idx if realWord == word else -1



