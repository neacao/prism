
'''
				NOTE FOR ME
	
	primalPos = an 1D array primal encoded position of a sequence for each key
	primalsPos = an 2D array primal encode position of all sequences for each key
	emptyBlock = a block that all elements are equal 0
'''


ITEMS = ["a", "b", "c"]

SEQUENCES = [
	["ab", "b", "b", "ab", "b", "a"],
	["ab", "b", "b"],
	["b", "ab"],
	["b", "b", "b"],
	["ab", "ab", "ab", "a", "bc"]
]

G_LENGTH = 4
G_ARRAY = [2, 3, 5, 7]
G_ARRAY_MULTIPLE = reduce( lambda x, y: x * y, G_ARRAY)

NO_LOGS = True


G_ARRAY_MASK = [105, 35, 7, 1]