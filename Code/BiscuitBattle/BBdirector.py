from px_director import Event

class SpawnEnemies(Event):
	def __init__(self, spawns):
		super(Event, self).__init__()
		self.spawns = spawns

	def update(self, data, common_data, dt):
		# spawn entities in spawns list
		for spawn in self.spawns:
			common_data.game.requestNewEnemy(
				entity_template= spawn.template,
				pos = spawn.pos,
				parent = False,
				name = spawn.name
			)
		return False # all done

class WaitForNoEnemies(Event):
	def __init__(self):
		super(Event, self).__init__()

	def update(self, data, common_data, dt):
		return common_data.game.num_monsters > 0
