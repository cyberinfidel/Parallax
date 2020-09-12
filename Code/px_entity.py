# external lib import
import enum
import copy

# Parallax
from px_vector import Vec3
import px_log

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

	# called when an entity is created that contains this component
	def initEntity(self, entity, data=False):
		pass

	def process(self, entity, command, args=None):
		return False

	def delete(self, data):
		px_log.log(f"Missing delete function for Component:{type(self)}")

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

	# only works for named entities
	def getEntityByName(self, name):
		return self.named_entities[name]

	# all templates have names
	def getTemplateByName(self, name):
		return self.templates[name]

class EntityList(list):
	def killEntitiesNotInList(self, list):
		for entity in self:
			if entity.name not in list:
				entity.setState(eStates.dead)

class Entity(object):
	def __init__(self,
							 name,
							 game,
							 graphics=False,
							 sounds=False,
							 controller=False,
							 collider=False,
							 init=False,
							 parent=False,
							 data=False):
		self.data = data	# note this is done first so things like init can use the data
		self.game = game
		self.name = name
		self.pos = Vec3(0, 0, 0)
		self.state = eStates.stationary
		self.new_state = True
		self.blink = False
		self.parent = parent

		self.components={}
		for type in [
			['graphics',graphics],
			['sounds', sounds],
			['controller', controller],
			['collider', collider],
		 ]:
			if type[1]:
				self.components[type[0]] = type[1]
				type[1].initEntity(self, data)

		if init:
			# px_log.log(f"Init entity: {name} code: {init}")
			# execute init
			exec(init,globals(),locals())

	def delete(self):
		pass


	def hasComponent(self, type):
		return type in self.components

	def getComponent(self, type):
		return self.components[type]

	def getName(self):
		return self.name

	def draw(self):
		# px_log.log(f"drawing entity: {self.name}")
		self.components['graphics'].draw(self)

	def setPos(self,pos):
		self.pos = copy.deepcopy(pos)

	def getPos(self):
		return self.pos

	def setParent(self,parent):
		self.parent = parent

	def getParent(self):
		return self.parent

	def setState(self,state):
		if self.hasComponent('controller'):
			# play nice with entities that have controllers
			# and let them choose how to handle this a bit more
			self.components['controller'].setState(self, state)
		else:
			self.state = state

	def getState(self):
		return self.state

	def process(self, command, args=None):
		for component in self.components:
			ret = self.components[component].process(self, command, args)
			if ret:
				return ret

# basic update method. Override for fancier behaviour
	def update(self, dt):
		# todo: make 'update' standard by iterating across components
		# i.e. fix sounds to be less weird
		# prob make graphics component decide if it actually draws or not
		# px_log.log(f"updating entity {self.name}")
		if self.hasComponent('controller'):
			self.components['controller'].update(self, dt)
		if self.state!=eStates.hide and self.state!=eStates.dead:
			if self.hasComponent('sounds'):
				self.components['sounds'].play(self)
			if self.hasComponent('graphics'):
				self.components['graphics'].update(self, dt)

	# def setController(self, controller):
	# 	self.controller = controller
	# 	self.controller_data = controller.makeData()

	def setGamePad(self, game_pad):
		self.game_pad = game_pad

	# def setGraphics(self,graphics):
	# 	self.graphics = graphics
	# 	if self.graphics:
	# 		self.graphics_data = graphics.makeData()

	# def setSounds(self,sounds):
	# 	self.sounds = sounds
	# 	if self.sounds:
	# 		self.sounds_data = sounds.makeData()


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
		return Entity(name=name,
									game = self.game,
									graphics=self.graphics,
									sounds=self.sounds,
									controller = self.controller,
									collider = self.collider,
									init=init,
									parent=parent,
									data=data)

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
