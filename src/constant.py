
'''
				NOTE FOR ME
	
	primalPos = an 1D array primal encoded position of a sequence for each key
	primalsPos = an 2D array primal encode position of all sequences for each key
	emptyBlock = a block that all elements are equal 0
'''

MIN_SUPP = 2

ITEMS = ["a", "b", "c"]

SEQUENCES = [
	["ab", "b", "b", "ab", "b", "a", "b", "b", "a"],
	["ab", "b", "b"],
	["b", "ab"],
	["b", "b", "b"],
	["ab", "ab", "ab", "a", "bc"]
]

G_ARRAY = [2, 3, 5, 7]
G_ARRAY_MULTIPLE = reduce( lambda x, y: x * y, G_ARRAY )
G_LENGTH = len(G_ARRAY)
G_ARRAY_MASK = [105, 35, 7, 1]

COUNTING_SUPPORT_ARRAY = {
	1: 0,
	2: 1, 3: 1, 5: 1, 7: 1, 11: 1, 13: 1, 17: 1, 19: 1,
	6: 2, 10: 2, 14: 2, 15: 2, 21: 2, 35: 2,
	30: 3, 42: 3, 70: 3, 105: 3,
	210: 4
}

NO_LOGS = True

G_ARRAY_ADVANCE = [2, 3, 5, 7, 11, 13, 17, 19]
G_LENGTH_ADVANCE = len(G_ARRAY_ADVANCE)