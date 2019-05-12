#!/usr/env/bin python3

from termcolor import colored

class Logger:
	def __init__(self, isDebugMode=False):
		self.isDebugMode = isDebugMode
	# --

	def log(self, content):
		print(content)
	# --
# ---