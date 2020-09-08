# external lib import
import enum
import copy

# Parallax
from px_vector import Vec3


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
		def __init__(self, entity, data):
			pass

	def makeData(self, entity, data=False):
		return self.Data(entity, data)

	def delete(self, data):
		log(f"Missing delete function for Component:{type(self)}")

class EntityManager(object):
	def __init__(self, game):
		self.templates = {}
		self.entities = []				# all entities including generated no-names
		self.named_entities = {}	# keep a list of the names entities
		self.game = game

	def makeEntityTemplate(self, name, graphics=False, sounds=False, controller=False, collider=False):
		self.templates[name] = EntityTemplate(self.game, graphics=graphics, sounds=sounds, controller=controller, collider=collider)

	def makeEntity(self, template, name=False, init=False, parent=False, data=False):
		new_entity = self.templates[template].instanceEntity(name if name else template, init, parent, data)
		self.entities.append(new_entity)
		if name:
			self.named_entities[name]=new_entity
		return self.entities[-1]

	def deleteDead(self):
		self.entities[:] = [x for x in self.entities if x.getState() != eStates.dead]
		kill_list=[]
		for name, entity in self.named_entities.items():
			if entity.getState()==eStates.dead:
				kill_list.append(name)
		for name in kill_list:
			self.named_entities.pop(name)

	# only works for names entities
	def getEntityByName(self, name):
		return self.named_entities[name]

class EntityList(list):
	def killEntitiesNotInList(self, list):
		for entity in self:
			if entity.name not in list:
				entity.setState(eStates.dead)

class Entity(object):
	class Data():
		def __init__(self):
			pass

	def __init__(self,
							 _name,
							 _game,
							 _graphics=False,
							 _sounds=False,
							 _controller=False,
							 _collider=False,
							 _init=False,
							 _parent=False,
							 _data=False):
		self.data = _data
		self.game = _game
		self.name = _name
		self.pos = Vec3(0, 0, 0)
		self.state = eStates.stationary
		self.new_state = True
		self.blink = False
		self.parent = _parent

		self.graphics = _graphics
		if self.graphics:
			self.graphics_data = _graphics.makeData(self, _data)

		self.sounds = _sounds
		if self.sounds:
			self.sounds_data = _sounds.makeData(self, _data)

		self.controller = _controller
		if self.controller:
			self.controller_data = _controller.makeData(self, _data)	# store data for this instance

		self.collider = _collider
		if self.collider:
			self.collider_data = _collider.makeData(self, _data)	# store data for this instance

		if _init:
			# execute init
			exec(_init,globals(),locals())

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
		return self.name

	def setPos(self,pos):
		self.pos = copy.deepcopy(pos)

	def getPos(self):
		return self.pos

	def setParent(self,parent):
		self.parent = parent

	def getParent(self):
		return self.parent

	def setState(self,state):
		if self.controller:
			# play nice with entities that have controllers
			# and let them choose how to handle this a bit more
			self.controller.setState(self.controller_data, self, state)
		else:
			self.state = state

	def getState(self):
		return self.state


# basic update method. Override for fancier behaviour
	def update(self, dt):
		if self.controller:
			self.controller.update(self.controller_data, self, dt)
		if self.state!=eStates.hide and self.state!=eStates.dead:
			if self.sounds:
				self.sounds.play(self.sounds_data,self)
			if self.graphics:
				self.graphics.update(self.graphics_data,self, dt)

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

	def instanceEntity(self, name, init, parent, data):
		if not name:
			name=self.name	# use template name
		return Entity(_name=name,
									_game = self.game,
									_graphics=self.graphics,
									_sounds=self.sounds,
									_controller = self.controller,
									_collider = self.collider,
									_init=init,
									_parent=parent,
									_data=data)

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
