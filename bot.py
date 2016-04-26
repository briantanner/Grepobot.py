import Skype4Py
import logging
import threading
import signal
import commands
from time import time, sleep
from config import Config
from monitor import Monitor

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', 
	level=logging.INFO, datefmt='%H:%M:%S')

config = Config('config.json')

class Bot(object):
	def __init__(self):
		self.settings = config.get()
		self.skype = Skype4Py.Skype(Events=self)
		self.skype.Attach()
		logging.info("Skype Attached.")
		
		self.monitor = Monitor(self.skype, config)
		
		# start the monitor
		self.monitor.create()
	
	def generateHelp(self):
		msgList = []
			
		msgList.append("{:<15}{:<30}".format("Command", "Description"))
		msgList.append("{:-<30}".format(""))
		
		for c in commands.commands:
			c = commands.commands[c]
			if hasattr(c, 'permissions') and c.permissions == 'admin':
				continue
			msgList.append("{:<15} {:<30}".format(c.aliases[0], c.doc))
		
		return msgList

	def MessageStatus(self, msg, status):

		if status in (Skype4Py.cmsSent, Skype4Py.cmsReceived) or len(msg.Body) < 2: return

		# ignore itself
		# if (msg.FromHandle == self.skype.CurrentUser.Handle): return

		# check if it's a command
		if msg.Body[0] not in self.settings['prefixes']: return

		# get command
		cmd = msg.Body.split()[0][1:].lower()
		
		# split args into array
		args = [] if len(msg.Body.split()) < 2 else msg.Body.split()[1:]

		# generate help
		if cmd == 'help':
			help = self.generateHelp()
			if help:
				msg.Chat.SendMessage("\n".join(help))

		elif cmd in commands.aliases:
			thread = threading.Thread(target=commands.aliases[cmd].execute, args=(msg, self.settings, args))
			thread.start()

		return

if __name__ == '__main__':
	# fix keyboard interrupt hangups
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	bot = Bot()
