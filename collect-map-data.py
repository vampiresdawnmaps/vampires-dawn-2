import json, os, re, sys
import xml.etree.ElementTree as ET


temp_dir = os.path.join(os.path.dirname(__file__), 'out', 'temp')


map_data = {}
with open(os.path.join(temp_dir, 'map-tree.dot')) as file_in:
	for line in file_in:
		m = re.match(r'(\d+) \[label=\"([^\"]+)\"', line)
		if m:
			map_id = int(m.group(1))
			map_name = m.group(2)
			map_data[map_id] = {'name': map_name}

item_data = {}
with open(os.path.join(temp_dir, 'RPG_RT.xml'), encoding='utf8') as file_in:
	root = ET.parse(file_in)
	for item in root.findall('./Database/items/Item'):
		id = int(item.get('id'))
		name = item.find('name').text
		item_data[id] = name

# TODO
#from contextlib import nullcontext
#i = 0
#map_id = 419
#map = map_data[map_id]
#with nullcontext() as ctx:
for i, (map_id, map) in enumerate(map_data.items()):
	print(f'Processing map {i+1}/{len(map_data)} ...')
	map_file = os.path.join(temp_dir, f'Map{int(map_id):04d}.xml')
	root = ET.parse(map_file)

	map['width'] = int(root.find('.//width').text)
	map['height'] = int(root.find('.//height').text)

	map['teleports'] = []	
	map['items'] = []
	map['hiddenPassages'] = []
	map['traps'] = []
	map['events'] = []
	map['treasure'] = []

	for event in root.findall(".//Event"):
		#print(f'Processing event {event.get('id')} ...')
		x = int(event.find('x').text)
		y = int(event.find('y').text)

		hasTeleport = False
		items = []
		teleportParams = {}
		hasTrap = False
		hiddenPassage = -1
		lockLevel = 0
		searchSkill = 0
		readMapSkill = 0
		treasureMapName = None

		pages = event.findall('./pages/EventPage')

		for page in pages:
			conditionVariableId = int(page.findtext('./condition/EventPageCondition/variable_id'))
			if conditionVariableId == 312:
				hiddenPassage = int(page.findtext('./character_direction'))
			elif conditionVariableId == 319:
				searchSkill = int(page.findtext('./condition/EventPageCondition/variable_value'))
			elif conditionVariableId == 321:
				readMapSkill = int(page.findtext('./condition/EventPageCondition/variable_value'))
				item_id = int(page.findtext('./condition/EventPageCondition/item_id'))
				treasureMapName = item_data.get(item_id, '???')

			for command in page.findall('./event_commands/EventCommand'):
				code = int(command.findtext('code'))
				params = command.findtext('parameters').split(' ')

				# ChangeGold = 10310, params = [(0=Increase |1=Decrease), (0=Constant | 1=Variable), (Ammount | VariableID)]
				if code == 10310:
					if int(params[0]) == 0:
						ammount = int(params[2])
						condition = int(command.findtext('indent')) > 0
						items.append({'name': 'Filar', 'ammount': ammount, 'hasCondition': condition})

				# ChangeItems = 10320, params = [(0=Increase |1=Decrease), ?, ItemID, ?, Ammount]
				if code == 10320:
					if int(params[0]) == 0:
						item_id = int(params[2])
						ammount = int(params[4])
						condition = int(command.findtext('indent')) > 0
						items.append({'name': item_data.get(item_id, '???'), 'ammount': ammount, 'hasCondition': condition})

				# CallEvent = 12330
				if code == 12330:
					called_common_event_id = int(command.findtext('parameters').split(' ')[1])
					# 4 = CommonEvent: 'Geheimnis'
					# 51-53 = CommonEvent: 'GeheimnisKlein', 'GeheimnisMittel', 'GeheimnisGross'
					# 56-58 = CommonEvent: 'GeheimgangKlein', 'GeheimgangMittel', 'GeheimgangGross'
					# 130 = CommonEvent: 'Kistengeheimnis'
					if called_common_event_id in {4, 51, 52, 53, 56, 57, 58, 130}:
						items.append({'name': 'Secret', 'ammount': 1, 'hasCondition': False})

				# Teleport = 10810
				if code == 10810:
					hasTeleport = True
					teleportParams ={'map': int(params[0]), 'x': int(params[1]), 'y': int(params[2])}
				
				# ConditionalBranch = 12010
				if code == 12010:
					# 323: SkillFallenFinden
					if int(params[0]) == 1 and int(params[1]) == 323:
						hasTrap = True
					
					# 311: SkillSchlossKnacken
					if int(params[0]) == 1 and int(params[1]) == 311:
						lockLevel = int(params[3])

		if len(items) > 0:
			map['items'].append({'x': x, 'y': y, 'items': items, 'lockLevel': lockLevel, 'searchSkill': searchSkill})
		elif hasTeleport:
			map['teleports'].append({'from': {'x': x, 'y': y}, 'to': teleportParams})
		elif hiddenPassage >= 0 and hiddenPassage < 4:
			map['hiddenPassages'].append({'x': x, 'y': y, 'direction': hiddenPassage})
		elif hasTrap:
			map['traps'].append({'x': x, 'y': y})
		elif readMapSkill > 0 and treasureMapName is not None:
			map['treasure'].append({'x': x, 'y': y, 'treasureMapName': treasureMapName})
		else:
			map['events'].append({'x': x, 'y': y})


json = json.dumps(map_data, indent=4)		

outfilename = os.path.join(os.path.dirname(__file__), 'out', 'html', 'map-data.js')
with open(outfilename, 'w', encoding='utf-8') as outfile:
	outfile.write('window.mapData = ')
	outfile.write(json)
	outfile.write(';')
	print(f'Created file {outfilename}')
