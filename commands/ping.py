from .command import Command
from time import sleep

class Ping(Command):
	def __init__(self):
		self._aliases = ['ping']
		self._doc = "Pings the bot"
		self._usage = "{prefix}ping"

	def execute(self, Message, args):
		if args and args[0] == 'sleep':
			sleep(10)
		Message.Chat.SendMessage('Pong!')