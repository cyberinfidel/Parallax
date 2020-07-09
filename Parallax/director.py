from Parallax import entity, controller, game, vector


class Event(object):
	def __init__(self):
		pass


# does nothing until enough updates have passed
class Delay(Event):
	def __init__(self, duration=False):
		super(Event, self).__init__()
		self.count_down = duration

	def update(self, data, common_data, dt):
		self.count_down -= dt
		return self.count_down > 0

# spawns a list of entities

class SpawnEntity(object):
	def __init__(self,
							entity_template,
							pos = vector.Vec3(0, 0, 0),
							parent = False,
							name = False):
		self.template=entity_template
		self.pos = pos
		self.parent = parent
		self.name = name

class Spawn(Event):
	def __init__(self, spawns):
		super(Event, self).__init__()
		self.spawns = spawns

	def update(self, data, common_data, dt):
		# spawn entities in spawns list
		for spawn in self.spawns:
			common_data.game.requestNewEntity(
				entity_template= spawn.template,
				pos = spawn.pos,
				parent = False,
				name = spawn.name
			)
		return False # all done

class EndGame(Event):
	def __init__(self):
		super(Event, self).__init__()

	def update(self, data, common_data, dt):
		common_data.game.setGameMode(game.eGameModes.win)
		common_data.game.restart_cooldown = 5

class WaitFor(Event):
	def __init__(self, condition):
		super(Event, self).__init__()
		# wait for condition
		self.condition=condition

	def update(self, data, common_data, dt):
		return self.condition()

class Controller(controller.Controller):
	def __init__(self, game, data):
		super(Controller, self).__init__(game)
		# values global to all this type of component

	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				self.game_pad = init.game_pad
			else:
				self.game_pad = False
			self.current_event = 0
			self.events = []

	def update(self, data, common_data, dt):
		if not data.events[data.current_event].update(data,common_data, dt):
			data.current_event+=1
		if data.current_event>=len(data.events):
			# run out of events so mark director for destruction
			self.setState(data, common_data, entity.eStates.dead)


