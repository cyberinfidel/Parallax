# external lib import
import enum

# import sdl files
import sdl2

# my file import
from entity import Component

# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')

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
	pause = 9
	quit = 10
	fullscreen = 11
	select = 12
	numActions = 13

class GamePad(Component):
	def __init__(self, game):
		super(GamePad, self).__init__(game)
		self.actions = {
			eActions.up:False,
			eActions.right:False,
			eActions.down:False,
			eActions.left:False,
			eActions.jump:False,
			eActions.attack_small:False,
			eActions.attack_big:False,
			eActions.block:False,
			eActions.pause:False,
			eActions.quit:False,
			eActions.fullscreen:False,
			eActions.stationary:True,
			eActions.select: False
		}

	def set(self,action):
		self.actions[action]=True

	def clear(self,action):
		self.actions[action]=False

class GameController(object):
	def __init__(self, handler, joy_number):
		self.handler = handler
		self.joy_number = joy_number
		self.name = sdl2.SDL_GameControllerName(self.handler)

class Input(object):
	def __init__(self, game):
		if sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)!=0:
			raise("Coudldn't initialise joysticks")

		self.quit = False
		self.game_pads = [GamePad(game)]

		self.key_map = {}
		self.key_map[eActions.up] = [sdl2.SDLK_UP]
		self.key_map[eActions.right] = [sdl2.SDLK_RIGHT]
		self.key_map[eActions.down] = [sdl2.SDLK_DOWN]
		self.key_map[eActions.left] = [sdl2.SDLK_LEFT]

		self.key_map[eActions.jump] = [sdl2.SDLK_SPACE]
		self.key_map[eActions.attack_small] = [sdl2.SDLK_g]
		self.key_map[eActions.attack_big] = [sdl2.SDLK_b]
		self.key_map[eActions.block] = [sdl2.SDLK_f]

		self.key_map[eActions.pause] = [sdl2.SDLK_p, sdl2.SDLK_ESCAPE]
		self.key_map[eActions.quit] = [sdl2.SDLK_q, sdl2.SDLK_ESCAPE]
		self.key_map[eActions.fullscreen] = [sdl2.SDLK_f]
		self.key_map[eActions.select] = [sdl2.SDLK_TAB, sdl2.SDLK_o]

		self.controllers = {}

		if sdl2.SDL_NumJoysticks()>0:
			for joy in range(sdl2.SDL_NumJoysticks()):
				if sdl2.SDL_IsGameController(joy):
					self.controllers[joy]=(GameController(handler=sdl2.SDL_GameControllerOpen(joy), joy_number=joy))
			if len(self.controllers)>1:
				self.game_pads.append(GamePad(game))


	def getGamePad(self, id):
		if id<len(self.game_pads): return self.game_pads[id]

	def update(self, events):
		for event in events:
				if event.type == sdl2.SDL_QUIT:
					self.game_pads[0].set(eActions.quit)
					self.game_pads[0].set(eActions.pause)

				if event.type == sdl2.SDL_CONTROLLERBUTTONDOWN:
					for player in [0, 1]:
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_A and event.cbutton.which==player:
							self.game_pads[player].set(eActions.jump)
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_Y and event.cbutton.which==player:
							self.game_pads[player].set(eActions.attack_big)
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_X and event.cbutton.which==player:
							self.game_pads[player].set(eActions.attack_small)
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_B and event.cbutton.which==player:
							self.game_pads[player].set(eActions.block)
		
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_DPAD_UP and event.cbutton.which==player:
							self.game_pads[player].set(eActions.up)
							self.game_pads[player].clear(eActions.down)
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_DPAD_DOWN and event.cbutton.which==player:
							self.game_pads[player].set(eActions.down)
							self.game_pads[player].clear(eActions.up)
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_DPAD_LEFT and event.cbutton.which==player:
							self.game_pads[player].set(eActions.left)
							self.game_pads[player].clear(eActions.right)
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_DPAD_RIGHT and event.cbutton.which==player:
							self.game_pads[player].set(eActions.right)
							self.game_pads[player].clear(eActions.left)
	
				elif event.type == sdl2.SDL_CONTROLLERBUTTONUP:
					for player in [0, 1]:
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_A and event.cbutton.which==player:
							self.game_pads[player].clear(eActions.jump)
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_Y and event.cbutton.which==player:
							self.game_pads[player].clear(eActions.attack_big)
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_X and event.cbutton.which==player:
							self.game_pads[player].clear(eActions.attack_small)
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_B and event.cbutton.which==player:
							self.game_pads[player].clear(eActions.block)
		
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_DPAD_UP and event.cbutton.which==player:
							self.game_pads[player].clear(eActions.up)
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_DPAD_DOWN and event.cbutton.which==player:
							self.game_pads[player].clear(eActions.down)
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_DPAD_LEFT and event.cbutton.which==player:
							self.game_pads[player].clear(eActions.left)
						if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_DPAD_RIGHT and event.cbutton.which==player:
							self.game_pads[player].clear(eActions.right)
	
				elif event.type == sdl2.SDL_KEYDOWN:
					if event.key.keysym.sym in self.key_map[eActions.up]:
						self.game_pads[0].set(eActions.up)
						self.game_pads[0].clear(eActions.down)
					if event.key.keysym.sym in self.key_map[eActions.down]:
						self.game_pads[0].set(eActions.down)
						self.game_pads[0].clear(eActions.up)
					if event.key.keysym.sym in self.key_map[eActions.left]:
						self.game_pads[0].set(eActions.left)
						self.game_pads[0].clear(eActions.right)
					if event.key.keysym.sym in self.key_map[eActions.right]:
						self.game_pads[0].set(eActions.right)
						self.game_pads[0].clear(eActions.left)
	
					if event.key.keysym.sym in self.key_map[eActions.jump]:
						self.game_pads[0].set(eActions.jump)
					if event.key.keysym.sym in self.key_map[eActions.attack_small]:
						self.game_pads[0].set(eActions.attack_small)
					if event.key.keysym.sym in self.key_map[eActions.attack_big]:
						self.game_pads[0].set(eActions.attack_big)
					if event.key.keysym.sym in self.key_map[eActions.block]:
						self.game_pads[0].set(eActions.block)
	
					if event.key.keysym.sym in self.key_map[eActions.pause]:
						self.game_pads[0].set(eActions.pause)
					if event.key.keysym.sym in self.key_map[eActions.quit]:
						self.game_pads[0].set(eActions.quit)
					if event.key.keysym.sym in self.key_map[eActions.fullscreen]:
						self.game_pads[0].set(eActions.fullscreen)
					if event.key.keysym.sym in self.key_map[eActions.select]:
						self.game_pads[0].set(eActions.select)

				elif event.type == sdl2.SDL_KEYUP:
					if event.key.keysym.sym in self.key_map[eActions.up]:
						self.game_pads[0].clear(eActions.up)
					if event.key.keysym.sym in self.key_map[eActions.down]:
						self.game_pads[0].clear(eActions.down)
					if event.key.keysym.sym in self.key_map[eActions.left]:
						self.game_pads[0].clear(eActions.left)
					if event.key.keysym.sym in self.key_map[eActions.right]:
						self.game_pads[0].clear(eActions.right)
	
					if event.key.keysym.sym in self.key_map[eActions.jump]:
						self.game_pads[0].clear(eActions.jump)
					if event.key.keysym.sym in self.key_map[eActions.attack_small]:
						self.game_pads[0].clear(eActions.attack_small)
					if event.key.keysym.sym in self.key_map[eActions.attack_big]:
						self.game_pads[0].clear(eActions.attack_big)
					if event.key.keysym.sym in self.key_map[eActions.block]:
						self.game_pads[0].clear(eActions.block)
	
					if event.key.keysym.sym in self.key_map[eActions.pause]:
						self.game_pads[0].clear(eActions.pause)
					if event.key.keysym.sym in self.key_map[eActions.quit]:
						self.game_pads[0].clear(eActions.quit)
					if event.key.keysym.sym in self.key_map[eActions.fullscreen]:
						self.game_pads[0].clear(eActions.fullscreen)
					if event.key.keysym.sym in self.key_map[eActions.select]:
						self.game_pads[0].clear(eActions.select)


