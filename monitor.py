import logging
import threading
from time import time, sleep
from api import Api
from formatter import Formatter

api = Api()

class Monitor:

	def __init__(self, skype, config):
		self._skype = skype
		self._config = config
		self._settings = config.get()
		self._nextrun = int(time()) + 10 
		logging.info("Created monitor")

	def create(self):
		logging.info("Starting monitor")
		while True:
			if self._nextrun <= int(time()):
				settings = self._settings

				# iterate and run monitor checks
				for server, monitors in settings['monitor']['servers'].items():
					thread = threading.Thread(target=self.run, args=(server, monitors))
					thread.start()

				# update timestamps
				self._nextrun = int(time()) + 300
				settings['monitor']['lastrun'] = int(time())
				self._config.save(settings)

			sleep(.01)

	def run(self, server, monitors):
		logging.info("Checking for updates")
		settings = self._settings

		# for server, monitors in settings['monitor']['servers'].items():
		data = {}
		# get a list of alliances from monitors in server
		alliances = [d['alliances'] for d in monitors]
		# flatten the list of lists which subsequently removes duplicates
		alliances = [l for sublist in alliances for l in sublist]
		# get a comma delimited string for use in api urls
		alliances_joined = ",".join(str(i) for i in alliances)

		lastrun = settings['monitor']['lastrun']

		# get data from api
		url = "/{0}/monitor/updates?time={1!s}&alliances={2}".format(server, lastrun, alliances_joined)
		data['updates'] = api.request(url)
		url = "/{0}/monitor/conquers?time={1!s}&alliances={2}".format(server, lastrun, alliances_joined)
		data['conquers'] = api.request(url)
		url = "/{0}/monitor/allianceChanges?time={1!s}&alliances={2}".format(server, lastrun, alliances_joined)
		data['changes'] = api.request(url)

		# determine if we have updates to send
		hasUpdates = any(data['updates']) or any(data['conquers']) or any(data['changes'])
		if not hasUpdates:
			return

		for monitor in monitors:
			self.update(server, monitor, data)

	def update(self, server, monitor, data):
		# clone monitor so we don't overwrite settings
		_monitor = dict(monitor)

		# TODO: delete monitor
		# skip empty monitor
		if not _monitor['alliances']: return

		logging.info("Sending Updates to chat %s", monitor['chatname'])

		# filter updates, conquers, and changes per this monitor
		_monitor['updates'] = {k: data['updates'][str(k)] for k in _monitor['alliances'] if data['updates'][str(k)] != None}
		_monitor['conquers'] = {k: data['conquers'][str(k)] for k in _monitor['alliances'] if data['conquers'][str(k)] != None}
		_monitor['changes'] = {k: data['changes'][str(k)] for k in _monitor['alliances'] if data['changes'][str(k)] != None}

		# get chat for monitor
		chat = self._skype.Chat(monitor['chatname'])
		
		# send updates to chat
		if (_monitor['updates']):
			chat.SendMessage(Formatter.format_updates(server, _monitor['updates']))
		if (_monitor['conquers']):
			chat.SendMessage(Formatter.format_conquers(server, _monitor['conquers']))
		if (_monitor['changes']):
			chat.SendMessage(Formatter.format_changes(server, _monitor['changes']))
