# external lib import
import enum

# import sdl files
import sdl2

# my file import
from vector import *

# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')

class eStates(enum.IntEnum):
	dead = 0
	stationary = 1
	runLeft = 2
	runRight = 3
	runUp = 4
	runDown = 5
	fallLeft = 6
	fallRight = 7
	idle = 8
	down = 9
	gettingUp = 10
	attackSmallLeft = 11
	attackSmallRight = 12
	attackBigLeft = 13
	attackBigRight = 14
	blockLeft = 15
	blockRight = 16
	jumpLeft = 17
	jumpRight = 18
	jumpUp = 19
	jumpDown = 20
	jumpStat = 21
	standDown = 22
	standLeft = 23
	standUp = 24
	standRight = 25
	shadow = 26
	numStates = 27

class Directions(enum.IntEnum):
	down = 0
	left = 1
	up = 2
	right = 3


class eActions(enum.IntEnum):
	up = 0
	right = 1
	down = 2
	left = 3
	jump = 4
	attack_small = 5
	attack_big = 6
	block = 7
	stationary = 8
	numActions = 9

# Component template root class
class Component(object):

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
	def __init__(self):
		self.templates = []
		self.entities = []

	def makeEntityTemplate(self, game, graphics=False, controller=False, collider=False):
		self.templates.append(EntityTemplate(game,graphics,controller, collider))
		return len(self.templates)-1

	def makeEntity(self, entity_t_index, name = False):
		self.entities.append( self.templates[entity_t_index].instanceEntity(name))
		return self.entities[-1]

class Entity(object):
	class Data():
		def __init__(self):
			pass

	def __init__(self, name, game, graphics=False, controller=False, collider=False):
		self.common_data = self.Data()
		self.common_data.game = game
		self.common_data.entity = self
		self.common_data.name = name
		self.common_data.pos = Vec3(0, 0, 0)
		self.common_data.state = eStates.stationary
		self.common_data.new_state = True
		self.common_data.blink = False

		self.graphics = graphics
		if self.graphics:
			self.graphics_data = graphics.makeData(self.common_data)

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

	def setState(self,state):
		self.common_data.state = state

	def getState(self):
		return self.common_data.state


# basic update method. Override for fancier behaviour
	def update(self, dt):
		if self.controller:
			self.controller.update(self.controller_data, self.common_data, dt)
		if self.common_data.state!=eStates.dead:
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


class EntityTemplate(object):

	def __init__(self, game, graphics = False, controller = False, collider = False):
		self.game = game
		self.graphics = graphics
		self.controller = controller
		self.collider = collider

	def instanceEntity(self, name):
		return Entity(name, game = self.game, graphics=self.graphics, controller = self.controller, collider = self.collider)


class ComponentManager(object):
	def __init__(self):
		self.templates = []
		self.data = []

	def makeTemplate(self, template_data):
		template = template_data['Template'](template_data)
		self.templates.append(template)
		return self.templates[-1]

	# def makeData(self, template_index, init_data=False):
	# 	self.data.append(self.templates[template_index].makeData())
	# 	return self.data[-1]




class GamePad(Component):
	def __init__(self):
		super(GamePad, self).__init__()
		self.actions = {
			eActions.up:False,
			eActions.right:False,
			eActions.down:False,
			eActions.left:False,
			eActions.jump:False,
			eActions.attack_small:False,
			eActions.attack_big:False,
			eActions.block:False,
			eActions.stationary:True
		}

	def set(self,action):
		self.actions[action]=True

	def clear(self,action):
		self.actions[action]=False

	def control(self):
		for action in self.actions:
			if action and self.entity.react:
				self.entity.react.tryAction(action)

class Input(object):
	def __init__(self):
		self.quit = False
		self.game_pads = [ GamePad(), GamePad()]

	def getGamePad(self, id):
		return self.game_pads[id]

	def update(self, events):
		for event in events:
			if event.type == sdl2.SDL_QUIT:
				self.quit = True
				break
			if event.type == sdl2.SDL_KEYDOWN:
				if event.key.keysym.sym == sdl2.SDLK_UP:
					self.game_pads[0].set(eActions.up)
					self.game_pads[0].clear(eActions.down)
				if event.key.keysym.sym == sdl2.SDLK_DOWN:
					self.game_pads[0].set(eActions.down)
					self.game_pads[0].clear(eActions.up)
				if event.key.keysym.sym == sdl2.SDLK_LEFT:
					self.game_pads[0].set(eActions.left)
					self.game_pads[0].clear(eActions.right)
				if event.key.keysym.sym == sdl2.SDLK_RIGHT:
					self.game_pads[0].set(eActions.right)
					self.game_pads[0].clear(eActions.left)

				if event.key.keysym.sym == sdl2.SDLK_SPACE:
					self.game_pads[0].set(eActions.jump)
				if event.key.keysym.sym == sdl2.SDLK_g:
					self.game_pads[0].set(eActions.attack_small)
				if event.key.keysym.sym == sdl2.SDLK_b:
					self.game_pads[0].set(eActions.attack_big)
				if event.key.keysym.sym == sdl2.SDLK_f:
					self.game_pads[0].set(eActions.block)


			elif event.type == sdl2.SDL_KEYUP:
				if event.key.keysym.sym == sdl2.SDLK_UP:
					self.game_pads[0].clear(eActions.up)
				if event.key.keysym.sym == sdl2.SDLK_DOWN:
					self.game_pads[0].clear(eActions.down)
				if event.key.keysym.sym == sdl2.SDLK_LEFT:
					self.game_pads[0].clear(eActions.left)
				if event.key.keysym.sym == sdl2.SDLK_RIGHT:
					self.game_pads[0].clear(eActions.right)

				if event.key.keysym.sym == sdl2.SDLK_SPACE:
					self.game_pads[0].clear(eActions.jump)
				if event.key.keysym.sym == sdl2.SDLK_SPACE:
					self.game_pads[0].clear(eActions.jump)
				if event.key.keysym.sym == sdl2.SDLK_g:
					self.game_pads[0].clear(eActions.attack_small)
				if event.key.keysym.sym == sdl2.SDLK_b:
					self.game_pads[0].clear(eActions.attack_big)
				if event.key.keysym.sym == sdl2.SDLK_f:
					self.game_pads[0].clear(eActions.block)
				# 	if event.key.keysym.sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN, sdl2.SDLK_RIGHT, sdl2.SDLK_LEFT):
				# 		vel[0] = 0
				# 		vel[1] = 0


