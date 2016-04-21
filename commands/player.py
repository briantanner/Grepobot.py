from .command import Command
from api import Api
from formatter import Formatter

try:
	from urllib import quote
except ImportError:
	from urllib.parse import quote

api = Api()

class Player(Command):
	def __init__(self):
		self._aliases = ['player','pl']
		self._doc = "Get player stats"
		self._usage = "{prefix}player us22 NoobLance"
	
	def execute(self, Message, args):
		url = '/{server}/player/{player}'.format(server=args[0], player=quote(' '.join(args[1:]).replace(" ", "+")))
		player = api.request(url)

		Message.Chat.SendMessage(Formatter.format_player(player))