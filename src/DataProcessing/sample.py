#!/usr/bin/env python3

class Sample:
	def __init__(self):
		print("Hello ")
		self._abc()

	def __abc(self):
		print("From private")



sample = Sample()
sample.__abc()