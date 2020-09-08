# external lib import
import enum
import copy

# my file import
from vector import Vec3

# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')

# note stationary(2)is the default starting state
class eStates:
	dead,\
	hide,\
	stationary,\
	runLeft,\
	runRight,\
	runUp,\
	runDown,\
	fallLeft,\
	fallRight,\
	idle,\
	down,\
	gettingUp,\
	attackSmallLeft,\
	attackSmallRight,\
	attackBigLeft,\
	attackBigRight,\
	blockLeft,\
	blockRight,\
	jumpLeft,\
	jumpRight,\
	jumpUp,\
	jumpDown,\
	jumpStat,\
	standDown,\
	standLeft,\
	standUp,\
	standRight,\
	hurtLeft,\
	hurtRight,\
	shadow,\
	appear,\
	fade,\
	numStates = range(0,33)

class eDirections(enum.IntEnum):
	down = 0
	left = 1
	up = 2
	right = 3
	num_directions = 4




# Component template root class
class Component(object):
	def __init__(self, game):
		self.game = game

# define a Data class if your component needs
#  instance specific data. If all the data is
#  static in the template and will not change
#  then there is no need to define this class
#  at all
	class Data(object):
		def __init__(self, common_data):
			pass

	def makeData(self, common_data):
		return self.Data(common_data)

	def delete(self, data):
		log(f"Missing delete function for Component:{type(self)}")

class EntityManager(object):
	def __init__(self, game):
		self.templates = {}
		self.entities = []
		self.game = game

	def makeEntityTemplate(self, name, graphics=False, sounds=False, controller=False, collider=False):
		self.templates[name] = EntityTemplate(self.game, graphics=graphics, sounds=sounds, controller=controller, collider=collider)

	def makeEntity(self, template, name=False, init=False):
		self.entities.append( self.templates[template].instanceEntity(name if name else template, init))
		return self.entities[-1]

	def deleteDead(self):
		self.entities[:] = [x for x in self.entities if x.getState() != eStates.dead]

class EntityList(list):
	def killEntitiesNotInList(self, list):
		for entity in self:
			if entity.common_data.name not in list:
				entity.setState(eStates.dead)

class Entity(object):
	class Data():
		def __init__(self):
			pass

	def __init__(self,
							 name,
							 game,
							 graphics=False,
							 sounds=False,
							 controller=False,
							 collider=False,
							 init=False):
		self.common_data = self.Data()
		self.common_data.game = game
		self.common_data.entity = self
		self.common_data.name = name
		self.common_data.pos = Vec3(0, 0, 0)
		self.common_data.state = eStates.stationary
		self.common_data.new_state = True
		self.common_data.blink = False
		self.common_data.parent = False

		self.graphics = graphics
		if self.graphics:
			self.graphics_data = graphics.makeData(self.common_data)

		self.sounds = sounds
		if self.sounds:
			self.sounds_data = sounds.makeData(self.common_data)

		self.controller = controller
		if self.controller:
			self.controller_data = controller.makeData(self.common_data)	# store data for this instance

		self.collider = collider
		if self.collider:
			self.collider_data = collider.makeData(self.common_data)	# store data for this instance

		if init:
			# execute init
			exec(init,globals(),locals())

	def delete(self):
		if self.graphics:
			self.graphics.delete(self.graphics_data)

		if self.sounds:
			self.sounds.delete(self.sounds_data)

		if self.controller:
			self.controller.delete(self.controller_data)

		if self.collider:
			self.collider.delete(self.collider)

	def getName(self):
		return self.common_data.name

	def setPos(self,pos):
		self.common_data.pos = copy.deepcopy(pos)

	def getPos(self):
		return self.common_data.pos

	def setParent(self,parent):
		self.common_data.parent = parent

	def getParent(self):
		return self.common_data.parent

	def setState(self,state):
		if self.controller:
			# play nice with entities that have controllers
			# and let them choose how to handle this a bit more
			self.controller.setState(self.controller_data, self.common_data, state)
		else:
			self.common_data.state = state

	def getState(self):
		return self.common_data.state


# basic update method. Override for fancier behaviour
	def update(self, dt):
		if self.controller:
			self.controller.update(self.controller_data, self.common_data, dt)
		if self.common_data.state!=eStates.hide and self.common_data.state!=eStates.dead:
			if self.sounds:
				self.sounds.play(self.sounds_data,self.common_data)
			if self.graphics:
				self.graphics.update(self.graphics_data,self.common_data, dt)

	def setController(self, controller):
		self.controller = controller
		self.controller_data = controller.makeData()

	def setGamePad(self, game_pad):
		self.controller_data.game_pad = game_pad

	def setGraphics(self,graphics):
		self.graphics = graphics
		if self.graphics:
			self.graphics_data = graphics.makeData()

	def setSounds(self,sounds):
		self.sounds = sounds
		if self.sounds:
			self.sounds_data = sounds.makeData()


class EntityTemplate(object):

	def __init__(self, game, graphics = False, sounds = False, controller = False, collider = False, name = False):
		self.game = game
		self.graphics = graphics
		self.sounds = sounds
		self.controller = controller
		self.collider = collider
		self.name = f"{name}(t)"

	def instanceEntity(self, name, init):
		if not name:
			name=self.name	# use template name
		return Entity(name=name,
									game = self.game,
									graphics=self.graphics,
									sounds=self.sounds,
									controller = self.controller,
									collider = self.collider,
									init=init)

	def delete(self):
		print(f"{self.name} - delete template doesn't do anything right now...")

class ComponentManager(object):
	def __init__(self, game):
		self.templates = []
		self.game = game
		self.instances = []

	def append(self, item):
		self.instances.append(item)
		return len(self.instances) - 1

	def pop(self, index):
		return self.instances.pop(index)

	# extras is a dictionary that can be added to the template_data
	# e.g. for injecting contextual stuff like the RenderLayer for graphics
	def makeTemplate(self, template_data, extras=None):
		if extras:
				template_data.update(extras)
		template = template_data['Template'](self.game, template_data)
		self.templates.append(template)
		return self.templates[-1]
