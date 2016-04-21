import Skype4Py
import logging
import threading
import signal
import commands
from time import time, sleep
from api import Api
from config import Config
from monitor import Monitor

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', 
	level=logging.INFO, datefmt='%H:%M:%S')

skype = Skype4Py.skype.Skype()
config = Config('config.json')
settings = config.get()
monitor = Monitor(skype, config)
api = Api()

def message_status(msg, status):
	global settings

	# ignore itself
	if (msg.FromHandle == skype.CurrentUser.Handle): return

	if status not in ('SENT','RECEIVED') or len(msg.Body) < 2: return
	
	# check if it's a command
	if msg.Body[0] not in settings['prefixes']: return

	cmd = msg.Body.split()[0][1:].lower()
	args = [] if len(msg.Body.split()) < 2 else msg.Body.split()[1:]

	if cmd == 'help':
		msgList = []
		msgList.append("{:<15}{:<30}".format("Command", "Description"))
		msgList.append("{:-<30}".format(""))
		for c in commands.commands:
			c = commands.commands[c]
			if hasattr(c, 'permissions') and c.permissions == 'admin':
				continue
			# usage = c.usage.format(prefix=settings['prefixes'][0])
			msgList.append("{:<15} {:<30}".format(c.aliases[0], c.doc))
		if msgList:
			# msgList = ["Command List:"] + msgList
			print(msgList)
			msg.Chat.SendMessage("\n".join(msgList))

	elif cmd in commands.aliases:
		thread = threading.Thread(target=commands.aliases[cmd].execute, args=(msg, args))
		thread.start()

	return

def main():
	global settings

	skype.Attach()
	logging.info("Skype Attached.")

	skype.OnMessageStatus = message_status
	logging.info("Message Handler Attached.\n")

	# start the monitor
	monitor.create()

if __name__ == '__main__':
	# fix keyboard interrupt hangups
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	main()
