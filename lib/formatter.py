
def format_updates(data):
  msgList = []
  abpList = []
  dbpList = []

  for id, alliance in data.iteritems():
    if (len(alliance) == 0): continue

    hasAbp = True if len(filter(lambda x: x['abp_delta'] != 0, alliance)) > 0 else False
    hasDbp = True if len(filter(lambda x: x['dbp_delta'] != 0, alliance)) > 0 else False

    if (hasAbp):
      # hard coded farsala here, this would need to be passed as an argument like print_updates(world, data)
      abpList.append("    %s (farsala)" % (alliance[0]['alliance_name']))
      for update in alliance:
        if (update['abp_delta'] == 0): continue
        abpList.append("        %s:\t+%s" % (update['name'], update['abp_delta']))

    if (hasDbp):
      # hard coded farsala here, this would need to be passed as an argument like print_updates(world, data)
      dbpList.append("    %s (farsala)" % (alliance[0]['alliance_name']))
      for update in alliance:
        if (update['dbp_delta'] == 0): continue
        dbpList.append("        %s:\t+%s" % (update['name'], update['dbp_delta']))

  # add abp updates to message
  if (len(abpList)):
    msgList.append(" (punch) ABP Alerts")
    msgList = msgList + abpList

  # add dbp updates to message
  if (len(dbpList)):
    msgList.append(" (ninja) DBP Alerts")
    msgList = msgList + dbpList

  return "\n".join(msgList)


def format_conquers(data):
  msgList = []

  msgList.append(" (bandit) Conquest Alerts")
  for id, alliance in data.iteritems():
    if (len(alliance) == 0): continue
    cqtowns = []
    
    for cq in alliance:
      # only show an internal once as conquered
      if (int(cq['newally']['id']) == int(cq['oldally']['id']) and cq['town']['id'] in cqtowns): continue
      # add town id for internal check
      cqtowns.append(cq['town']['id'])

      msgList.append("    %s (farsala)" % (alliance[0]['alliance_name']))

      # print conquered town
      if (int(cq['newally']['id']) == int(id)):
        msgList.append("        %s conquered '%s' from %s (%s)" % (cq['newplayer']['name'], cq['town']['name'], cq['oldplayer']['name'], cq['oldally']['name']))
        continue

      # print lost town
      if (int(cq['oldally']['id']) == int(id)):
        msgList.append("        %s lost '%s' to %s (%s)" % (cq['oldplayer']['name'], cq['town']['name'], cq['newplayer']['name'], cq['newally']['name']))
        continue

  return "\n".join(msgList)

def format_changes(data):
  msgList = []

  msgList.append(" (star) Alliance Member Changes")
  for id, alliance in data.iteritems():
    if (len(alliance) == 0): continue

    msgList.append("    %s (farsala)" % (alliance[0]['alliance_name']))
    for change in alliance:
      if (int(change['new_alliance']) == int(id)):
        msgList.append("        Player %s joined %s" % (change['player_name'], change['new_alliance_name']))
      elif (int(change['old_alliance']) == int(id)):
        msgList.append("        Player %s left %s" % (change['player_name'], change['old_alliance_name']))

  return "\n".join(msgList)

def format_player(data):
  msgList = []

  msgList.append("Name:\t" + str(data['name']))
  msgList.append("Alliance:\t" + str(data['Alliance']['name']))
  msgList.append("Rank:\t" + str(data['rank']))
  msgList.append("Towns:\t" + str(data['towns']))
  msgList.append("Points:\t" + str(data['points']))
  msgList.append("ABP:\t" + str(data['abp']))
  msgList.append("DBP:\t" + str(data['dbp']))

  # msgList.append("Name:".ljust(10, '.') + str(data['name']))
  # msgList.append("Alliance:".ljust(10, '.') + str(data['Alliance']['name']))
  # msgList.append("Rank:".ljust(10, '.') + str(data['rank']))
  # msgList.append("Towns:".ljust(10, '.') + str(data['towns']))
  # msgList.append("Points:".ljust(10, '.') + str(data['points']))
  # msgList.append("ABP:".ljust(10, '.') + str(data['abp']))
  # msgList.append("DBP:".ljust(10, '.') + str(data['dbp']))

  msgList.append("\nUpdates:\n")

  msgList.append("Time\tTowns\tPoints\tABP\t\tDBP")

  for o in data["Updates"]:
    points_tab = "\t" if len(str(o['points_delta'])) > 3 else "\t\t"
    abp_tab = "\t" if len(str(o['abp_delta'])) > 3 else "\t\t"
    msgList.append(str(o['time']) + "\t" + str(o['towns_delta']) + "\t\t" + str(o['points_delta']) + points_tab + str(o['abp_delta']) + abp_tab + str(o['dbp_delta']))

  # msgList.append("Time".ljust(7, '.') + "Towns".ljust(6, '.') + "Points".ljust(8, '.') + "ABP".ljust(8, '.') + "DBP")

  # for o in data["Updates"]:
  #   msgList.append(str(o['time']).ljust(7, '.') + str(o['towns_delta']).ljust(6, '.') + str(o['points_delta']).ljust(8, '.') + str(o['abp_delta']).ljust(8, '.') + str(o['dbp_delta']))

  return "\n".join(msgList)
