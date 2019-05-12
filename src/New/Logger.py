#!/usr/env/bin python3

from termcolor import colored

class Logger:
	def __init__(self, isDebugMode):
		self.isDebugMode = isDebugMode
	# --

	def log(self, content):
		print(content)
	# --
# ---