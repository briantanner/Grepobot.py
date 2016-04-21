
class Formatter:

	def format_updates(server, data):
		msgList = []
		abpList = []
		dbpList = []

		for id, alliance in data.items():
			if (len(alliance) == 0): continue

			hasAbp = True if len(list(filter(lambda x: x.abp_delta != 0, alliance))) > 0 else False
			hasDbp = True if len(list(filter(lambda x: x.dbp_delta != 0, alliance))) > 0 else False

			if (hasAbp):
				# hard coded farsala here, this would need to be passed as an argument like format_updates(world, data)
				abpList.append("    *{0} ({1})*".format(alliance[0].alliance_name, server))
				for update in alliance:
					if (update.abp_delta == 0): continue
					abpList.append("        {0.name}: +{0.abp_delta}".format(update))

			if (hasDbp):
				# hard coded farsala here, this would need to be passed as an argument like format_updates(world, data)
				dbpList.append("    *{0} ({1})*".format(alliance[0].alliance_name, server))
				for update in alliance:
					if (update.dbp_delta == 0): continue
					dbpList.append("        {0.name}: +{0.dbp_delta}".format(update))

		# add abp updates to message
		if len(abpList):
			msgList.append(" (punch) ABP Alerts")
			msgList = msgList + abpList
			msgList.append(" ")

		# add dbp updates to message
		if len(dbpList):
			msgList.append(" (ninja) DBP Alerts")
			msgList = msgList + dbpList
			msgList.append(" ")

		return "\n".join(msgList)


	def format_conquers(server, data):
		msgList = []
		cqList = []

		for id, alliance in data.items():
			if (len(alliance) == 0): continue
			cqtowns = []

			for cq in alliance:
				# only show an internal once as conquered
				if (int(cq.newally) == int(cq.oldally) and cq.town.id in cqtowns): 
					continue

				# add town id for internal check
				cqtowns.append(cq.town.id)

			cqList.append("    *{0} ({1})*".format(alliance[0].alliance_name, server))

			# print conquered town
			if (int(cq.newally) == int(id)):
				cqList.append("        {0.newplayer_name} conquered '{0.town.name}' from {0.oldplayer_name} ({0.oldally_name})".format(cq))
				continue

			# print lost town
			if (int(cq.oldally) == int(id)):
				cqList.append("        {0.oldplayer_name} lost '{0.town.name}' to {0.newplayer_name} ({0.newally_name})".format(cq))
				continue

		# add conquers to message
		if len(cqList):
			msgList.append(" (bandit) Conquest Alerts")
			msgList = msgList + cqList
			msgList.append(" ")

		return "\n".join(msgList)

	def format_changes(server, data):
		msgList = []
		chgList = []

		for id, alliance in data.items():
			if (len(alliance) == 0): continue

			chgList.append("    *{0} ({1})*".format(alliance[0].alliance_name, server))
			for change in alliance:
				if (int(change.new_alliance) == int(id)):
					chgList.append("        Player {0.player_name} joined {0.new_alliance_name}".format(change))

				elif (int(change.old_alliance) == int(id)):
					chgList.append("        Player {0.player_name} left {0.old_alliance_name}".format(change))

		# add changes to message
		if len(chgList):
			msgList.append(" (star) Alliance Member Changes")
			msgList = msgList + chgList
			msgList.append(" ")

		return "\n".join(msgList)

	def format_player(data):
		msgList = []

		msgList.append("Name:\t" + str(data.name))
		msgList.append("Alliance:\t" + str(data.Alliance.name))
		msgList.append("Rank:\t" + str(data.rank))
		msgList.append("Towns:\t" + str(data.towns))
		msgList.append("Points:\t" + str(data.points))
		msgList.append("ABP:\t" + str(data.abp))
		msgList.append("DBP:\t" + str(data.dbp))

		msgList.append("\nUpdates:\n")

		msgList.append("Time\tTowns\tPoints\tABP\t\tDBP")

		for o in data.Updates:
			points_tab = "\t" if len(str(o.points_delta)) > 3 else "\t\t"
			abp_tab = "\t" if len(str(o.abp_delta)) > 3 else "\t\t"

			msgList.append("{0.time!s}\t{0.towns_delta!s}\t\t{0.points_delta!s}".format(o) +
				"{1}{0.abp_delta!s}{2}{0.dbp_delta!s}".format(o, points_tab, abp_tab))
			# msgList.append(str(o['time']) + "\t" + str(o['towns_delta']) + "\t\t" + str(o['points_delta']) + points_tab + str(o['abp_delta']) + abp_tab + str(o['dbp_delta']))

		return "\n".join(msgList)
