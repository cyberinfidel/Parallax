# external lib import
import enum

# my file import
from vector import Vec3

# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')

class eStates(enum.IntEnum):
	dead = 0
	hide = 1
	stationary = 2
	runLeft = 3
	runRight = 4
	runUp = 5
	runDown = 6
	fallLeft = 7
	fallRight = 8
	idle = 9
	down = 10
	gettingUp = 11
	attackSmallLeft = 12
	attackSmallRight = 13
	attackBigLeft = 14
	attackBigRight = 15
	blockLeft = 16
	blockRight = 17
	jumpLeft = 18
	jumpRight = 19
	jumpUp = 20
	jumpDown = 21
	jumpStat = 22
	standDown = 23
	standLeft = 24
	standUp = 25
	standRight = 26
	hurtLeft = 27
	hurtRight = 28
	shadow = 29
	appear = 30
	fade = 31
	numStates = 32

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


class EntityManager(object):
	def __init__(self, game):
		self.templates = []
		self.entities = []
		self.game = game

	def makeEntityTemplate(self, graphics=False, sounds=False, controller=False, collider=False):
		self.templates.append(EntityTemplate(self.game, graphics=graphics, sounds=sounds, controller=controller, collider=collider))
		return len(self.templates)-1

	def makeEntity(self, entity_t_index, name = False):
		self.entities.append( self.templates[entity_t_index].instanceEntity(name))
		return self.entities[-1]

class Entity(object):
	class Data():
		def __init__(self):
			pass

	def __init__(self, name, game, graphics=False, sounds=False, controller=False, collider=False):
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

	def getName(self):
		return self.common_data.name

	def setPos(self,pos):
		self.common_data.pos = pos

	def getPos(self):
		return self.common_data.pos

	def setParent(self,parent):
		self.common_data.parent = parent

	def getParent(self):
		return self.common_data.parent

	def setState(self,state):
		self.controller.setState(self.controller_data, self.common_data, state)

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

	def __init__(self, game, graphics = False, sounds = False, controller = False, collider = False):
		self.game = game
		self.graphics = graphics
		self.sounds = sounds
		self.controller = controller
		self.collider = collider

	def instanceEntity(self, name):
		return Entity(name, game = self.game, graphics=self.graphics, sounds=self.sounds, controller = self.controller, collider = self.collider)


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


	def makeTemplate(self, template_data):
		template = template_data['Template'](self.game, template_data)
		self.templates.append(template)
		return self.templates[-1]
