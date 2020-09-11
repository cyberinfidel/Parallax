from px_entity import eStates
from px_controller import Controller
from px_game import eGameModes
from px_vector import Vec3
import px_graphics


# the director class takes a list of events
# and executes them in order
# Unless an event returns eEventState.block
# then it will keep executing events in a single
# update until it runs out or there is an EndScene
# or similar
# An event returning eEventState.block means
# that further event updates are put off to the next
# director update call.
# Events that continue to return eEventState.live
# will be called every director update until
# they return eEventState.dead at which point
# they're removed from the event list
# This way there are:
# one-off events (return dead immediately)
# events with duration (return live until they eventually return dead)
# events that block further events happeneing (return block)

class eEventStates:
	dead, live, block = range(0, 3)


class Event(object):
	def __init__(self):
		pass


# does nothing until enough updates pass/time passes
class Delay(Event):
	def __init__(self, duration=False):
		super(Event, self).__init__()
		self.count_down = duration

	def update(self, entity, dt):
		self.count_down -= dt
		return eEventStates.block if (self.count_down > 0) else eEventStates.dead


class Message(Event):
	def __init__(self, text, pos, color, duration=0, align=px_graphics.eAlign.left):
		super(Event, self).__init__()
		self.text = text
		self.pos = pos
		self.color = color
		self.duration = duration
		self.align = align

	def update(self, entity, dt):
		entity.game.message(self.text, self.pos, self.color, self.duration, self.align)
		return eEventStates.dead

class ClearColor(Event):
	def __init__(self, color):
		super(Event, self).__init__()
		self.color=color

	def update(self, entity, dt):
		entity.game.setClearColor(self.color)
		return eEventStates.dead

class SetClearColor(Event):
	def __init__(self, color):
		super(Event, self).__init__()
		self.color = color

	def update(self, entity, dt):
		entity.game.setClearColor(self.color)
		return eEventStates.dead

class FadeToClearColor(Event):
	def __init__(self, color, time):
		super(Event, self).__init__()
		self.color=color
		self.time = time
		self.step_color = None

	def update(self, entity, dt):
		current_color = entity.game.getClearColor()
		if not self.step_color:
			# get the incremental color, effectively the vector towards the final color
			# only calculate this once - but has to be when fade starts, not when instance created
			# (director creates instances of Events when director is created)
			self.step_color = px_graphics.Color(
				(self.color.r - current_color.r) / self.time,
				(self.color.g - current_color.g) / self.time,
				(self.color.b - current_color.b) / self.time,
				(self.color.a - current_color.a) / self.time,
				)
		# check when to stop
		self.time -= dt
		if self.time<=0:
			entity.game.setClearColor(self.color) # make sure completely get to color desired
			return eEventStates.dead

		entity.game.setClearColor(self.step_color * px_graphics.Color(dt, dt, dt, dt) + current_color)
		return eEventStates.live

class SetRenderLayerColor(Event):
	def __init__(self, rl, color):
		super(Event, self).__init__()
		self.rl = rl
		self.color = color

	def update(self, entity, dt):
		entity.game.setColorCast(self.rl, self.color)
		return eEventStates.dead


# Fades a RenderLayer held by the game instance to a color
# via changing value of rl's color cast
class FadeRenderLayer(Event):
	def __init__(self, rl, color, time):
		super(Event, self).__init__()
		self.rl = rl
		self.color = color
		self.time = time
		self.total_time = time
		self.step_color = False

	def update(self, entity, dt):
		current_color = entity.game.getColorCast(self.rl)
		if not self.step_color:
			# get the incremental color, effectively the vector towards the final color
			# only calculate this once - but has to be when fade starts, not when instance created
			# (director creates instances of Events when director is created)
			self.step_color = px_graphics.Color(
				(self.color.r - current_color.r) / self.time,
				(self.color.g - current_color.g) / self.time,
				(self.color.b - current_color.b) / self.time,
				(self.color.a - current_color.a) / self.time,
			)
		# check when to stop
		self.time -= dt
		if self.time <= 0:
			entity.game.setColorCast(self.rl, self.color)
			return eEventStates.dead

		entity.game.setColorCast(self.rl, self.step_color * px_graphics.Color(dt, dt, dt, dt) + current_color)
		return eEventStates.live


# Fades in a RenderLayer held by the game instance
# via changing alpha of color cast

# spawns a list of entities
# pass it a list of "SpawnEntity"s
class Spawn(Event):
	def __init__(self, spawns):
		super(Event, self).__init__()
		self.spawns = spawns

	def update(self, entity, dt):
		# spawn entities in spawns list
		for spawn in self.spawns:
			entity.game.requestNewEntity(
				template= spawn.template,
				name = spawn.name,
				pos = spawn.pos,
				parent = False,
				init = spawn.init,
				data = spawn.data
			)
		return eEventStates.dead # all done

# data container used by Spawn - not an Event itself
class SpawnEntity(object):
	def __init__(self,
							template,
							name = False,
							pos = Vec3(0, 0, 0),
							parent = False,
							init = False,
							 data = False):
		self.template=template
		self.pos = pos
		self.parent = parent
		self.name = name if name else template
		self.init = init
		self.data = data

# signals to end the scene
# todo: set up how to specify the next scene better
class NextScene(Event):
	def __init__(self, next_scene=-1, cooldown=5):
		super(NextScene, self).__init__()
		self.next_scene = next_scene
		self.cooldown=cooldown

	def update(self, entity, dt):
		entity.game.nextScene(self.next_scene)
		return eEventStates.dead

# signals to exit the program
class Quit(Event):
	def update(self, entity, dt):
		entity.game.quit()

class WaitFor(Event):
	def __init__(self, condition):
		super(Event, self).__init__()
		# wait for condition
		self.condition=condition

	def update(self, entity, dt):
		return eEventStates.dead if self.condition() else eEventStates.block

#############################
# Director controller class #
##############################
def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(Controller):
	def __init__(self, game, data):
		super(Controller, self).__init__(game)
		# values global to all this type of component

	def initEntity(self, entity, data=False):
			entity.latest_event = 0
			entity.events = []

	# eEventStates: 0 dead, 1 live, 2 blocking
	def update(self, entity, dt):
		index = 0
		while index< len(entity.events):
			result = entity.events[index].update(entity,dt)
			if result==eEventStates.dead:
				# remove this event from list
				entity.events.pop(index)
			elif result==eEventStates.block:
				# this event is blocking
				# so don't execute any more events
				return
			else:
				# live events live to be updated again next time
				# but need to go onto next event
				index+=1
