#!/usr/env/bin python3

from termcolor import colored

class Logger:
	def __init__(self, isDebugMode = False, logFilePath = None):
		self.isDebugMode = isDebugMode
		self.logFilePath = logFilePath
	# --

	def log(self, content, diskMode = False):
		if diskMode:
			self._writeLog(content)
		else:
			print(content)
	# --

	def _writeLog(self, content):
		if self.logFilePath == None:
			print('[ERROR] Not found log file path')
			exit(1)
		# -

		with open(self.logFilePath, 'a') as fp:
			fp.write(content)
	# --
# ---