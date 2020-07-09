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
	numActions = 11
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
			eActions.stationary:True
		}

	def set(self,action):
		self.actions[action]=True

	def clear(self,action):
		self.actions[action]=False

class Input(object):
	def __init__(self, game):
		self.quit = False
		self.game_pads = [ GamePad(game), GamePad(game)]

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

				if event.key.keysym.sym == sdl2.SDLK_p:
					self.game_pads[0].set(eActions.pause)
				if event.key.keysym.sym == sdl2.SDLK_q:
					self.game_pads[0].set(eActions.quit)

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

				if event.key.keysym.sym == sdl2.SDLK_p:
					self.game_pads[0].clear(eActions.pause)
				if event.key.keysym.sym == sdl2.SDLK_q:
					self.game_pads[0].clear(eActions.quit)


