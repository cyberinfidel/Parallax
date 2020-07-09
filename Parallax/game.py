# import python libs
import time
import enum
import copy

# import sdl files
import sdl2.ext
import sdl2.sdlmixer

# import my files
import Parallax.entity as entity
import Parallax.game_pad as game_pad
import Parallax.vector as vector

# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')

class eGameModes(enum.IntEnum):
	quit=0
	init=1
	title=2
	start=3
	play=4
	game_over=5
	win = 6
	paused = 7
	numGameModes = 8


class Game(object):

	def __init__(self, title, res_x, res_y, zoom, fullscreen):
		# Initialize the video system - this implicitly initializes some
		# necessary parts within the SDL2 DLL used by the video module.
		#
		# You SHOULD call this before using any video related methods or
		# classes.
		sdl2.ext.init()

		# Create a new window (like your browser window or editor window,
		# etc.) and give it a meaningful title and size. We definitely need
		# this, if we want to present something to the user.
		if(fullscreen):
			self.window = sdl2.ext.Window(title, size=(res_x*zoom, res_y*zoom), flags=sdl2.SDL_WINDOW_FULLSCREEN)
		else:
			self.window = sdl2.ext.Window(title, size=(res_x*zoom, res_y*zoom))  # ,flags=sdl2.SDL_WINDOW_FULLSCREEN)

		# By default, every Window is hidden, not shown on the screen right
		# after creation. Thus we need to tell it to be shown now.
		self.window.show()

		# set up a renderer to draw stuff. This is a HW accelerated one.
		# Switch on VSync to avoid running too fast
		# and wasting power and keep graphics nice and clean
		self.ren = sdl2.ext.Renderer(self.window, flags=sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC)
		# makes zoomed graphics blocky (for retro effect)
		sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"nearest")
		# makes the graphics look and act like Atari ST screen size, even though rendered much larger
		sdl2.SDL_RenderSetLogicalSize(self.ren.renderer, res_x, res_y)



		self.running = True
		self.game_mode = eGameModes.title


		self.input = game_pad.Input(self)

		self.drawables = []
		self.audibles = []
		self.updatables = []

		self.graphics_manager = entity.ComponentManager(game=self)
		self.controller_manager = entity.ComponentManager(game=self)
		self.entity_manager = entity.EntityManager(game=self)
		self.sound_manager = entity.ComponentManager(game=self)


	def render(self):
		self.ren.color = sdl2.ext.Color(0, 0, 0)
		self.ren.clear()

		self.draw()
		# present graphics and actually display
		sdl2.SDL_RenderPresent(self.ren.renderer)
		self.window.refresh()

	def tick(self, dt):
		self.input.update(sdl2.ext.get_events())
		self.update(dt)
		if self.input.quit:
			self.running = False

	def interpolate(self, alpha):
		pass
		if alpha>0.0001:
			self.interp(alpha)
#			self.pos_int[0] = self.pos[0]* alpha + self.pos_old[0] * (1.0 - alpha)
#			self.pos_int[1] = self.pos[1]* alpha + self.pos_old[1] * (1.0 - alpha)


	def run(self):
		# uses a fixed time step for physics - see article about "Fixing Your Time Step"

		self.lastTime = time.time()

		t = 0.0
		dt = 0.016
		self.render()
		currentTime = time.time()
		accum = 0.0

		while self.running:
			newTime = time.time()
			frameTime = newTime - currentTime
			currentTime = newTime

			accum += frameTime

			while accum>=dt:
				self.tick(dt)
				accum -= dt
				t += dt

			self.interpolate(accum/dt)

			self.render()

		# Clear up and exit
		sdl2.ext.quit()

	def setGameMode(self, game_mode):
		self.game_mode = game_mode
		if self.game_mode==eGameModes.title:
			self.killPlayEntities()

	def requestNewEntity(self,
											 entity_template,
											 pos=vector.Vec3(0,0,0),
											 parent=False,
											 name=False):
		new_entity = self.entity_manager.makeEntity(entity_template, name)
		new_entity.setPos(copy.deepcopy(pos))
		new_entity.setParent(parent)
		#	TODO: add generic names to entity templates
		# if name:
		# 	new_entity.name=name
		#		else:
		#			new_entity.name=entity_template.getName()

		if new_entity.graphics:
			self.drawables.append(new_entity)
		if new_entity.sounds:
			self.audibles.append(new_entity)
		if new_entity.controller:
			self.updatables.append(new_entity)
		if new_entity.collider:
			self.collision_manager.append(new_entity)
		return new_entity

# end requestNewEntity()

	def __del__(self):
		sdl2.sdlmixer.Mix_CloseAudio()

	def runTests(self):
		result = 0
		fails = vector.runTests()
		if len(fails)>0:
			log("Unit tests failed.")
			for fail in fails:
				log(f"Fail in: {fail}")
			return 1
		return result