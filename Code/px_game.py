# import python libs
import time
import copy
import gc

# import sdl files
import sdl2.ext
import sdl2.sdlmixer

# import my files
import px_entity
import px_game_pad
import px_vector
import px_graphics
import px_sound
import px_utility
import px_log
import px_collision

class eGameModes:
	quit, \
	init, \
	title, \
	start, \
	play, \
	game_over, \
	win, \
	paused, \
	numGameModes = range(0,9)


class Game(object):
	def __init__(self):
		px_log.log("Getting game data...")
		self.game_data = px_utility.getDataFromFile('game.config')['game']

		px_log.log("Getting user data...")
		self.user_data = px_utility.getDataFromFile('user.config')['user']

		px_log.log("Setting up window...")
		# Initialize the video system - this implicitly initializes some
		# necessary parts within the SDL2 DLL used by the video module.
		#
		# You SHOULD call this before using any video related methods or
		# classes.
		sdl2.ext.init()

		self.title = self.game_data['title']
		self.res_x = self.game_data['res_x']
		self.res_y = self.game_data['res_y']
		self.zoom = self.user_data['zoom']
		self.fullscreen = self.user_data['fullscreen']
		self.clear_color =  self.game_data['clear_color']

		sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_JOYSTICK | sdl2.SDL_INIT_GAMECONTROLLER)

		# INITIALISE GRAPHICS & THE SCREEN

		# Create a new window (like your browser window or editor window,
		# etc.) and give it a meaningful title and size. We definitely need
		# this, if we want to present something to the user.
		# todo: calculate resolution more carefully esp for fullscreen

		# create the window (without showing it)
		self.windowed_width = self.res_x*self.zoom		# keep these for later
		self.windowed_height = self.res_y*self.zoom
		self.window = sdl2.ext.Window(self.title, size=(self.windowed_width, self.windowed_height))
		if(self.fullscreen):
			self.makeFullscreen()

		# set up a renderer to draw stuff. This is a HW accelerated one.
		# Switch on VSync to avoid running too fast
		# and wasting power and keep graphics nice and clean
		self.ren = sdl2.ext.Renderer(self.window, flags=sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC)
		# makes zoomed graphics blocky (for retro effect)
		sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"nearest")
		# makes the graphics look and act like the desired screen size, even though they may be rendered at a different one
		sdl2.SDL_RenderSetLogicalSize(self.ren.renderer, self.res_x, self.res_y)

		self.running = True
		self.game_mode = eGameModes.title

		self.input = px_game_pad.Input(self)

		self.render_layers = {}
		self.scroll = False
		self.flags={}

		self.drawables = px_entity.EntityList()
		self.audibles = px_entity.EntityList()
		self.updatables = px_entity.EntityList()

		self.graphics_manager = px_entity.ComponentManager(game=self)
		self.controller_manager = px_entity.ComponentManager(game=self)
		self.entity_manager = px_entity.EntityManager(game=self)
		self.sound_manager = px_entity.ComponentManager(game=self)
		self.sound_mixer = px_sound.SoundMixer(self)
		self.collision_manager = px_collision.CollisionManager(game=self)

		# By default, every Window is hidden, not shown on the screen right
		# after creation. Thus we need to tell it to be shown now.
		self.window.show()

	########################################################
	# Render Layer interface and methods

	def getColorCast(self, rl):
		return self.render_layers[rl].getColorCast()

	def setColorCast(self, rl, color):
		self.render_layers[rl].setColorCast(color)

	def render(self):
		self.ren.color = self.clear_color.toSDLColor()
		self.ren.clear()

		self.draw()
		# present graphics and actually display
		sdl2.SDL_RenderPresent(self.ren.renderer)
		self.window.refresh()

	# display text on screen - not v sophisticated, but handy
	def message(self,
							text,
							pos,
							color=px_graphics.Color(1, 1, 1, 1),
							duration=-1,	# or forever
							align=px_graphics.eAlign.left,
							fade_speed=0.5
							):
		message = self.requestNewEntity(template='message',
																		name= f"message: {text}",
																		pos=pos,
																		parent=self,
																		data={
																			'ren_layer': self.render_layers['overlay'],
																			'message': text,
																			'font': 0,
																			'color' : color,
																			'duration' : duration,
																			'align' : align,
																			'fade_speed' : fade_speed
																		}
		)
		return message

	def makeFullscreen(self):
		# self.window = sdl2.ext.Window(self.title, size=(self.res_x, self.res_y), flags=sdl2.SDL_WINDOW_FULLSCREEN)

		current_display = sdl2.SDL_GetWindowDisplayIndex(self.window.window)
		current_display_mode = sdl2.SDL_DisplayMode()
		res = sdl2.SDL_GetCurrentDisplayMode(current_display,current_display_mode)
		px_log.log(f"Current display mode: {current_display_mode}")

		display_modes = []
		display_mode_index = 0  # sdl2.SDL_GetWindowDisplayIndex(self.window.window)
		for mode_index in range(current_display, sdl2.SDL_GetNumDisplayModes(display_mode_index)):
			disp_mode = sdl2.SDL_DisplayMode()
			ret = sdl2.SDL_GetDisplayMode(
				display_mode_index,
				mode_index,
				disp_mode
			)
			display_modes.append(disp_mode)
			px_log.log(f"mode:{mode_index} info:{display_modes[mode_index]}")

		# todo: something more clever than this after testing on more monitors
		# prob just make a better guess on the window size as a whole fraction of the native display size
		# without getting too large or too small
		# e.g. for MacBook Pro, 960 is too small; 1280 isn't great and is more fuzzy than 1920 - which looks fine;
		# 2880 looks even sharper than as 1920, but will prob be pushing too many pixels
		# Prob should allow it to be overridden via options/config

		# sdl2.SDL_SetWindowSize(self.window.window,1280,720)
		# sdl2.SDL_SetWindowSize(self.window.window,1440,810)
		# sdl2.SDL_SetWindowSize(self.window.window,1920,1080)
		sdl2.SDL_SetWindowSize(self.window.window,
													 self.res_x*self.zoom,
													 self.res_y*self.zoom)
		sdl2.SDL_SetWindowFullscreen(self.window.window, sdl2.SDL_WINDOW_FULLSCREEN)
		return
		#
		# # choose a good display mode, zoom combination before re-creating the window
		# # look for ideal: 60hz that divides by width precisely and is tall enough
		# for display_mode in display_modes:
		# 	if display_mode.refresh_rate == 60:
		# 		if (display_mode.w / self.res_x).is_integer() and display_mode.w<2000:
		# 			zoom = int(display_mode.w / self.res_x)
		# 			if display_mode.h >= zoom * self.res_y:
		# 				# we have a winner
		# 				# sdl2.SDL_SetWindowFullscreen(self.window.window, sdl2.SDL_WINDOW_FULLSCREEN)
		# 				# display_mode.h=1080
		# 				# self.window = sdl2.ext.Window(self.title, size=(display_mode.w, display_mode.h),flags=sdl2.SDL_WINDOW_FULLSCREEN)
		# 				# self.window = sdl2.ext.Window(self.title, size=(self.res_x * zoom, self.res_y * zoom),flags=sdl2.SDL_WINDOW_FULLSCREEN)
		# 				# res = sdl2.SDL_SetWindowDisplayMode(self.window.window, display_mode)
		# 				print(f"Chose mode:{display_mode}. Zoom factor: {zoom}. Result: {res}")
		# 				return
		# 			else:
		# 				px_log.log(f"Not taller than {self.res_y} after zoomed({self.res_y*zoom}) - Display mode {display_mode}")
		# 		else:
		# 			px_log.log(f"Too big or Not multiple of {self.res_x} - Display mode {display_mode}")
		# 	else:
		# 		px_log.log(f"Not 60hz - Display mode {display_mode}")
		#
		#
		#
		# px_log.log("Couldn't find ideal display mode for full screen - trying to get next best.")


	def toggleFullscreen(self):
		self.fullscreen = not self.fullscreen
		if self.fullscreen:
			self.makeFullscreen()
		else:
			sdl2.SDL_SetWindowSize(self.window.window, self.windowed_width, self.windowed_height)
			sdl2.SDL_SetWindowFullscreen(self.window.window, False)

		sdl2.SDL_RenderSetLogicalSize(self.ren.renderer, self.res_x, self.res_y)	 # to make sure

	# batch creates templates from provided dict data
	def makeTemplates(self, templates_data):
		for name, template in templates_data.items():
			px_log.log(f"Making {name} template.")
			self.entity_manager.makeEntityTemplate(name,
																						 controller=template['controller'](self.controller_manager) if 'controller' in template else None,
																						 collider=template['collider'](self.controller_manager) if 'collider' in template else None,
																						 graphics=self.graphics_manager.makeTemplate(template['graphics']['component'],
																																												 {'RenderLayer': self.render_layers[template['graphics']['render layer']]}) if 'graphics' in template else None
																						 )


	########################################################
	# Entites and Templates interface

	# batch requests entities from provided dict data
	def makeEntities(self, entities_data):
		entities = {}
		for name, entity in entities_data.items():
			init = False
			if 'init' in entity:
				init = entity['init']	# custom initialisation code, not always needed
			data = False
			if 'data' in entity:
				data = entity['data']
			entities['name'] = self.requestNewEntity(template=entity['template'],
																							 name=name,
																							 parent=self,
																							 init=init,
																							 data=data)

	# main method to make a single entity
	def requestNewEntity(self,
											 template,
											 pos=False,
											 parent=False,
											 name=False,
											 init=False,
											 data=False):
		new_entity = self.entity_manager.makeEntity(template=template,
																								name=name,
																								init=init,
																								parent=parent,
																								data=data)
		# position (and anything else) may be set within the code at runtime
		# and passed in as a parameter
		# or it may be set as part of executing the  init routine
		# in the entity's instance method
		if pos:
			new_entity.setPos(copy.deepcopy(pos))

		if new_entity.hasComponent('graphics'):
			self.drawables.append(new_entity)
		if new_entity.hasComponent('sounds'):
			self.audibles.append(new_entity)
		if new_entity.hasComponent('controller') or new_entity.hasComponent('graphics'):
			self.updatables.append(new_entity)
		if new_entity.hasComponent('collider'):
			self.collision_manager.append(new_entity)
		return new_entity
	# end requestNewEntity()

	def getEntityByName(self, name):
		return self.entity_manager.getEntityByName(name)

	def getTemplateByName(self, name):
		return self.entity_manager.getTemplateByName(name)

	########################################################
	# Scenes and Modes interface

	def getScenesData(self, file):
		self.scenes_data = (px_utility.getDataFromFile(file))
		self.current_scene = 0

	def getCurrentScene(self):
		return self.current_scene

	def getCurrentMode(self):
		return self.current_mode

	# ends the scene and by default increments the scene counter for the next scene
	# can change between modes e.g. playing and title
	# next scene can be specified by name
	def nextScene(self, next_scene=-1, mode=False): # kill
		gc.enable()
		gc.collect()

		# clear all the flags
		for flag in self.flags:
			self.flags[flag]=False

		if mode:
			if mode!=self.current_mode:
				px_log.log(f"Switching to mode: {mode}")
				self.current_mode=mode
				self.mode_data = self.game_data['modes'][self.current_mode] # convenience
				# kill old mode
				self.killEntitiesExceptDicts(
					[
						self.game_data['entities'],
					]
				)

				# set up next mode
				px_log.log(f"Making {mode} mode templates.")
				if 'templates' in self.mode_data:
					self.makeTemplates(self.mode_data['templates'])
				px_log.log(f"Making {mode} mode entities.")
				if 'entities' in self.mode_data:
					self.makeEntities(self.mode_data['entities'])
				if next_scene<0:	# no scene specified so revert to 0
					next_scene = 0
				px_log.flushToFile()



		if next_scene>=0:
			# specified scene rather than following pre-defined order
			self.current_scene = next_scene
			specified = "specified "
		else:
			self.current_scene+=1
			if self.current_scene>=len(self.mode_data['scenes']):
				# todo add check for completing the game instead of just looping?
				self.current_scene=0
			specified = ""
		next_scene = self.mode_data['scenes'][self.current_scene]
		px_log.log(
			f"Switching to {specified}scene [{self.current_mode},{self.current_scene}]: {self.mode_data['scenes'][self.current_scene]}")

		# kill old scene
		self.killEntitiesExceptDicts(
			[
				self.game_data['entities'],
			 	self.mode_data['entities'] if 'entities' in self.mode_data else {}
			]
		)

		###################
		# init next scene #
		###################
		self.scene_data = self.scenes_data['scenes'][self.mode_data['scenes'][self.current_scene]]
		# initialise map todo: make another entity instead of special
		# if "Map" in self.scene_data:
		# 	self.level = map.Map(self, self.scene_data, self.templates['tile'])

		if 'templates' in self.scene_data:
			self.makeTemplates(self.scene_data['templates'])
		if 'entities' in self.scene_data:
			self.makeEntities(self.scene_data['entities'])
		px_log.flushToFile()

		gc.collect()
		gc.disable()
		if len(gc.garbage)>0: px_log.log(gc.garbage)

	########################################################
	# Flags interface

	# sets a flag associated with a string identifier
	# that can be checked on by any entity
	def setFlag(self, flag):
		self.flags[flag] = True	# value is arbitrary

	# checks a flag and clears it
	# so trigger only happens once
	def checkFlagAndClear(self, flag):
		if flag in self.flags:
			self.flags.pop(flag)
			return True
		return False

	# checks a flag without clearing it if it's True
	# use if something else may be checking this flag
	def checkFlag(self, flag):
		return flag in self.flags



	########################################################
	# update methods used to make game "go"


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



	def setClearColor(self, color):
		self.clear_color = color

	def getClearColor(self):
		return self.clear_color

	def getGamePad(self, player):
		return self.input.getGamePad(player)

	def __del__(self):
		sdl2.sdlmixer.Mix_CloseAudio()

	def runTests(self):
		result = 0
		fails = px_vector.runTests()
		if len(fails)>0:
			print("Unit tests failed.")
			for fail in fails:
				print(f"Fail in: {fail}")
			return 1
		return result