#!/usr/bin/env python3

import openpyxl, json

class PrismHelper:
	def __init__(self):
	# --

	def convertHorizontalRecord(self, resourcePath):
		wb = openpyxl.load_workbook(resourcePath)
		ws = wb.active
		wsRange = ws['A{}:H{}'.format(ws.min_row, ws.max_row)]

		seqList = []
		
	# --



	def encode(self, resoucrePath, mappingPath):


	# --
# ---


if __name__ == "__main__":

# ---