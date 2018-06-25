#!/usr/bin/env python3

class string(str):
	
	def sample(self):
		#print self, "hello"
		return 


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

		for index in range(_idx, lengOfSelf):
			curChar = self[index]
			if curChar == "." or curChar == "-":
				break
			realWord += curChar

		return idx if realWord == word else -1


def sortAdv(sequence):
	# List = [ 'A', 'D.C', ...] - C must appear before D
	numberOfItemsets = len(sequence)
	ret = [None] * numberOfItemsets

	for index in range(0, numberOfItemsets):
		itemset 					= sequence[index]
		componenets 			= itemset.split(".")
		componenetsSorted = list(sorted(componenets))
		strJoined 				= ".".join(componenetsSorted)
		ret[index] 				= strJoined

	return ret


def test():
	#print sortAdv(['A', 'B', 'R1.V1', 'L.E.M.C', 'F.R', 'Y.I1.I', 'J.T.Q', 'G.Z.X'])
	return

if __name__ == "__main__":
	test()

	