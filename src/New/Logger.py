#!/usr/env/bin python3

import time, random
from termcolor import colored

class Logger:
	def __init__(self, isDebugMode = False, logFilePath = None):
		self.isDebugMode = isDebugMode
		self.logFilePath = logFilePath
		self.current_milli_time = lambda: int(round( * 1000))
	# --

	def log(self, content, forceDisplay = False, diskMode = False):
		if diskMode:
			self._writeLog(content)

		if forceDisplay or self.isDebugMode:
			print(content)
	# --

	def _writeLog(self, content):
		if self.logFilePath == None:
			print('[ERROR] Not found log file path')
			exit(1)
		# -

		path = self.logFilePath + str(int(time.time())) + str(random.randint(1,100))
		print('write to path: {}'.format(path))

		with open(path, 'a') as fp:
			fp.write(content)
			# sleep(1)

	# --
# ---