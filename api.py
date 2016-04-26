import requests
import json

class JSONObject:
	def __init__(self, d):
		self.__dict__ = d

	def __iter__(self):
		return iter(self.__dict__.items())

	def __str__(self):
		return str(self.__dict__)

	def __getitem__(self, key):
		if not key in self.__dict__:
			return
		return self.__dict__[key]

	def __setitem__(self, key, value):
		self.__dict__[key] = value

	def __delitem__(self, key):
		del self.__dict__[key]

class Api:

	def __init__(self):
		self.baseurl = "http://www.grepinformant.com/api/v1"
		return

	def request(self, url):
		url = self.baseurl + url
		res = requests.get(url)

		if (res.status_code == requests.codes.ok):
			data = json.loads(res.text, object_hook=JSONObject)
			return data

		res.raise_for_status()