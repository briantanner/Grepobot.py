import os
import json

class ConfigNotFoundError:
	def __init__(self, message, errors):
		super(ConfigNotFoundError, self).__init__(message)

class Config:
	def __init__(self, file):
		self._basedir = os.getcwd()
		self._file = file
		self._settings = {}

		if os.path.isfile(os.path.join(self._basedir, file)):
			with open(os.path.join(self._basedir, file), 'r') as f:
				self._settings = json.load(f)
		else:
			raise ConfigNotFoundError("Configuration file not found: {}".format(file))

	def get(self):
		return self._settings

	def set(self, key, value):
		self._settings[key] = value

	def save(self, settings=None):
		if settings:
			self._settings = settings

		with open(os.path.join(self._basedir, self._file), 'w') as f:
			json.dump(self._settings, f, indent=4)