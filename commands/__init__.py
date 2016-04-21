from .command import Command
from .ping import Ping
from .player import Player

commands = {}
aliases = {}

def register(name, command):
	command = command()
	commands[name] = command

	if not hasattr(command, 'aliases'):
		return

	for i in command.aliases:
		aliases[i] = command

"""Register commands below"""

register('ping', Ping)
register('player', Player)