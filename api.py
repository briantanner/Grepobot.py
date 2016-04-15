#!/usr/bin/python3

import urllib, json, Skype4Py
from time import time, sleep
from lib import formatter
skype = Skype4Py.skype.Skype()

apiurl = "http://www.grepinformant.com/api/v1"
# lastcheck = int(time())
chatname = "#us.grepo/$bfa07f64b369b5bf"

config = { "monitor": {}, "apiurl": "http://www.grepinformant.com/api/v1" }
config['monitor']['us50'] = {}
config['monitor']['us50']['#us.grepo/$bfa07f64b369b5bf'] = {}
config['monitor']['us50']['#us.grepo/$bfa07f64b369b5bf']['alliances'] = [1341, 1131, 740, 862, 1201, 1543]
config['monitor']['us50']['#us.grepo/$bfa07f64b369b5bf']['lastcheck'] = int(time())
config['monitor']['us50']['#us.grepo/$af63eeb34358462'] = {}
config['monitor']['us50']['#us.grepo/$af63eeb34358462']['alliances'] = [191, 481]
config['monitor']['us50']['#us.grepo/$af63eeb34358462']['lastcheck'] = int(time())

def api_request(url):
  # get conquers from api
  response = urllib.request.urlopen(url)

  # parse response data
  data = response.read()
  # only return conquers if there is data
  if (len(data) > 0):
    data = json.loads(data)
    return data

  # no data, just return
  return

def message_status(Message, Status):
  if Status not in ('SENT','RECEIVED') or len(Message.Body) < 2: return
  if Message.Body[0] not in ('.',): return
  cmd = Message.Body.split()[0][1:].upper()
  params = '' if len(Message.Body.split()) < 2 else ' '.join(Message.Body.split()[1:])

  if cmd in ('PLAYER',):
    url = '%s/%s/player/%s' % (config['apiurl'], 'us50', params.replace(" ", "+"))
    print(url)
    player = api_request(url)

    if (player):
      Message.Chat.SendMessage(formatter.format_player(player))

def main():
  global config
  nextcheck = 0
  skype.Attach()
  skype.OnMessageStatus = message_status
  chat = skype.Chat(chatname)

  for server in config['monitor']:
    alliances = [d['alliances'] for chatnames in config['monitor'][server] for d in chatnames]
    print(alliances)
    alliances = [item for sublist in alliances for item in sublist]
    print(alliances)
    
  while True:
    sleep(.01)

  # while True:
  #   # if nextcheck <= int(time()):
  #   sleep(.01)

    # http://www.grepinformant.com/api/v1/us50/player/Lance+The+Strange

  # lastcheck = int(time()) - 3600
  # alliances = [191, 481]
  # # updates url for test
  # url = '%s/%s/monitor/updates?time=%d&alliances=%s' % (apiurl, "us50", lastcheck, ','.join(str(x) for x in alliances))
  # updates = api_request(url)

  # if (updates):
  #   chat.SendMessage(formatter.format_updates(updates))

  # # conquers url for test
  # url = '%s/%s/monitor/conquers?time=%d&alliances=%s' % (apiurl, server, lastcheck, ','.join(str(x) for x in alliances))
  # conquers = api_request(url)

  # if (conquers):
  #   chat.SendMessage(formatter.format_conquers(conquers))

  # # member changes url for test
  # url = '%s/%s/monitor/allianceChanges?time=%d&alliances=%s' % (apiurl, server, lastcheck, ','.join(str(x) for x in alliances))
  # changes = api_request(url)

  # if (changes):
  #   chat.SendMessage(formatter.format_changes(changes))

if __name__ == '__main__':
  main()
