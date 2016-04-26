from .command import Command
from time import sleep

class Ping(Command):
	def __init__(self):
		self._aliases = ['ping']
		self._doc = "Pings the bot"
		self._usage = "{prefix}ping"

	def execute(self, msg, settings, args):
		# sleep used in debugging, test threading/concurrency
		if args and args[0] == 'sleep':
			m = msg.Chat.SendMessage("Sleeping...")
			sleep(10)
		else:
			m = msg.Chat.SendMessage("Pong")
			return

		m.Body = "Pong!"