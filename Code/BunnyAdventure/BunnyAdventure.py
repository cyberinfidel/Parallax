# import python libs
import sys

import sdl2.mouse

# import Parallax files
# 	add path to Parallax
sys.path.insert(1, '../')
# actually import files
from game import Game, eGameModes
from entity import eStates
from collision import CollisionManager
from vector import Vec3, rand_num
import controller
import graphics
import sound
from director import DirectorController, Delay, SpawnEntity, EndGame


# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')

#import BunnyAdventure files
import Macaroon as macaroon
import Oreo as oreo
import background as back
import plat
from title import titleGraphics, TitleController, eTitleStates
from rain import rainGraphics, RainController
import butterfly as butterfly

class BunnyAdventure(Game):
	def __init__(self):
		# do bare minimum to set up
		# most set up is in first update
		# this way I can restart the game
		super(BunnyAdventure, self).__init__("Bunny Adventure", res_x= 640, res_y= 360, zoom = 2, fullscreen=False)
		# sdl2.mouse.SDL_ShowCursor(False)
		self.logical_size_x = self.res_x
		self.logical_size_y = self.res_y

		self.collision_manager = CollisionManager(game=self)  # TODO: should this be a ComponentManager() like the others?

		##########################
		# set up graphics layers #
		##########################
		self.renlayer = graphics.RenderLayer(self.ren)
		self.title_renlayer = graphics.RenderLayer(self.ren)
		self.scroll = True
		self.quit_cooldown = 0.5

		##########################
		# set up sound           #
		##########################
		self.sound_mixer = sound.SoundMixer(self)
		###############################
		# set up background and title #
		###############################

		title_graphics = self.graphics_manager.makeTemplate(titleGraphics(self.title_renlayer))
		title_controller = self.controller_manager.makeTemplate({"Template": TitleController})
		self.title_t = self.entity_manager.makeEntityTemplate(graphics=title_graphics, controller=title_controller)
		self.title = self.requestNewEntity(entity_template=self.title_t, pos=Vec3(80, 400, -50), parent=self, name="Title")
		self.title.setGamePad(self.input.getGamePad(0))

		self.raining = False
		self.setGameMode(eGameModes.title)

		self.back_t = self.entity_manager.makeEntityTemplate(graphics=back.getGraphics(self.graphics_manager,self.renlayer))
		self.platform_t = self.entity_manager.makeEntityTemplate(graphics=plat.getGraphics(self.graphics_manager,self.renlayer),
																												 controller=plat.getController(self.controller_manager),
																												 collider=plat.getCollider(self.collision_manager)
																												 )



		###################
		# make components #
		###################
		# Graphics Templates
		raingraphics = self.graphics_manager.makeTemplate(rainGraphics(self.renlayer))
		macaroon_graphics = self.graphics_manager.makeTemplate(macaroon.graphics(self.renlayer))
		oreo_graphics = self.graphics_manager.makeTemplate(oreo.graphics(self.renlayer))

		# Sound Templates
		macaroon_sounds = False #self.sound_manager.makeTemplate(heroSounds(self.sound_mixer))
		oreo_sounds = False #self.sound_manager.makeTemplate(heroSounds(self.sound_mixer))

		# Controller Templates
		raincontroller = self.controller_manager.makeTemplate({"Template": RainController})
		macaroon_controller = self.controller_manager.makeTemplate({"Template": macaroon.Controller})
		oreo_controller = self.controller_manager.makeTemplate({"Template": oreo.Controller})
		bfly_controller = self.controller_manager.makeTemplate({"Template": butterfly.Controller})

		# Collider Templates
		macaroon_collider = self.collision_manager.makeTemplate({"Template": macaroon.Collider})
		oreo_collider = self.collision_manager.makeTemplate({"Template": oreo.Collider})

		#########################################
		# Make entity templates from components #
		#########################################
		self.rain_t = self.entity_manager.makeEntityTemplate(graphics=raingraphics, controller=raincontroller)
		self.bfly_templates =[]
		for bfly_graphics in [butterfly.graphics, butterfly.graphics2, butterfly.graphics3]:
			self.bfly_templates.append(self.entity_manager.makeEntityTemplate(graphics=self.graphics_manager.makeTemplate(bfly_graphics(self.renlayer)), controller=bfly_controller))

		self.macaroon_t = self.entity_manager.makeEntityTemplate(graphics=macaroon_graphics,
																												 sounds = macaroon_sounds,
																												 controller=macaroon_controller,
																												 collider=macaroon_collider,
																												 )
		
		self.oreo_t = self.entity_manager.makeEntityTemplate(graphics=oreo_graphics,
																												 sounds = oreo_sounds,
																												 controller=oreo_controller,
																												 collider=oreo_collider,
																												 )

		# director
		director_controller = self.controller_manager.makeTemplate({"Template":DirectorController})
		self.director_t = self.entity_manager.makeEntityTemplate(controller=director_controller)
	# end init()


	###########
	#  update #
	###########

	def update(self, dt):

		if self.game_mode==eGameModes.init:

			pass

##################################################
		elif self.game_mode==eGameModes.title:
			pass
##################################################
		elif self.game_mode==eGameModes.start:
			# set up new game and clean up anything from last game
			self.num_monsters = 0
			self.killPlayEntities()
			self.cleanUpDead()
			self.director = self.requestNewEntity(entity_template=self.director_t)
			self.director.controller_data.events = self.KFEvents()

			self.back = self.requestNewEntity(entity_template=self.back_t, pos=Vec3(0, 500, -500), parent=self, name="back")
			for n in (0,100,200,300,400):
				self.platform = self.requestNewEntity(entity_template=self.platform_t, pos=Vec3(300+n/2, 50, n/10), parent=self, name="platform")

			# make bunnies
			self.macaroon = self.requestNewEntity(entity_template=self.macaroon_t, pos=Vec3(190, 60, 50), parent=False, name="Macaroon")
			self.macaroon.setGamePad(self.input.getGamePad(0))
			self.oreo = self.requestNewEntity(entity_template=self.oreo_t, pos=Vec3(500, 60, 0), parent=False, name="Oreo")
			self.oreo.setGamePad(self.input.getGamePad(1))


			self.rain_cooldown = 500
			self.restart_cooldown=60
			self.setGameMode(eGameModes.play)
		##################################################
		elif self.game_mode==eGameModes.play:

			if (rand_num(10) == 0 and len(self.drawables)<5):
				bfly = self.entity_manager.makeEntity(self.bfly_templates[rand_num(3)])
				bfly.setPos(Vec3(rand_num(self.res_x), rand_num(self.res_y), 500))
				self.drawables.append(bfly)
				self.updatables.append(bfly)

			# rain
			if False:#self.raining:
				if (rand_num(20)==0):
					rain = self.entity_manager.makeEntity(self.rain_t)
					rain.setState(RainController.state_fall)
					rain.setPos(Vec3(rand_num(1920), rand_num(270), 500))
					self.drawables.append(rain)
					self.updatables.append(rain)
			self.rain_cooldown -=1
			if self.rain_cooldown<=0:
				self.rain_cooldown=rand_num(500)+500
				self.raining = not self.raining

			# if self.hero.getState()==eStates.dead:
			# 	self.setGameMode(eGameModes.game_over)
			# 	self.restart_cooldown=3



		####################################################

		elif self.game_mode==eGameModes.game_over:
			self.director.setState(eStates.dead)
			self.restart_cooldown-=dt
			self.title.setState(eTitleStates.game_over)
			if self.restart_cooldown<=0:
				self.setGameMode(eGameModes.title)
				self.cleanUpDead()

		####################################################

		elif self.game_mode==eGameModes.win:
			self.restart_cooldown-=dt
			if self.restart_cooldown<=0:
				self.setGameMode(eGameModes.title)
				self.cleanUpDead()

		####################################################

		elif self.game_mode==eGameModes.quit:
			self.quit_cooldown-=dt
			self.title.setState(eTitleStates.quit)
			if self.quit_cooldown<=0:
				self.running=False
				return

		# Always do this, unless paused:
		if self.game_mode!=eGameModes.paused:
			for index, updatable in reversed(list(enumerate(self.updatables))):
				updatable.update(dt)
			for audible in self.audibles:
				audible.sounds.play(audible.sounds_data, audible.common_data)

			self.collision_manager.doCollisions() # collisions between monsters
			# clean up dead entities
			self.cleanUpDead()

		else:
			self.title.update(dt)

# end update() #################################################################

	def cleanUpDead(self):
		self.updatables[:] = [x for x in self.updatables if x.getState() != eStates.dead]
		self.collision_manager.cleanUpDead()
		self.drawables[:] = [x for x in self.drawables if x.getState() != eStates.dead]
		self.audibles[:] = [x for x in self.audibles if x.getState() != eStates.dead]

	def killPlayEntities(self):
		for updatable in self.updatables:
			if not (updatable is self.title):
				updatable.common_data.state = eStates.dead


	def requestTarget(self,pos):
		return self.hero.common_data.pos

	###########
	#  interp #
	###########

	def interp(self, alpha):
		pass

	###########
	#  draw		#
	###########

	def draw(self):

		if self.game_mode==eGameModes.play:
			#########################
			# scroll and scale view #
			# Here be Dragons...    #
			#########################
			if self.scroll:
				# scale on distance between O & M, if bigger than will fit on the default res and if changed more than tolerance
				separation = abs(self.macaroon.common_data.pos - self.oreo.common_data.pos)
				new_screen_size_x = max((separation.x) * 2, self.res_x)
				new_screen_size_y = max((separation.y + separation.z) * 2, self.res_y)
				# force 16:9 ratio
				if (new_screen_size_x * 9.0) < (new_screen_size_y * 16.0):  # too tall
					new_screen_size_x = (new_screen_size_y * (16.0 / 9.0))
				else:  # too wide
					new_screen_size_y = (new_screen_size_x * 9.0 / 16.0)

				delta_x = self.logical_size_x - new_screen_size_x
				delta_y = self.logical_size_y - new_screen_size_y
				if (delta_x * delta_x + delta_y * delta_y) > 1000:  # tolerance for zooming (arbitrary)
					new_screen_size_x = self.logical_size_x - ((self.logical_size_x - new_screen_size_x) / 40.0)
					new_screen_size_y = self.logical_size_y - ((self.logical_size_y - new_screen_size_y) / 40.0)
					self.logical_size_x = new_screen_size_x
					self.logical_size_y = new_screen_size_y

				sdl2.SDL_RenderSetLogicalSize(self.ren.sdlrenderer, int(self.logical_size_x), int(self.logical_size_y))

				# scroll screen based on point midway between O & M
				offset = self.renlayer.getOrigin() - (self.macaroon.common_data.pos + self.oreo.common_data.pos) / 2.0 + Vec3(
					self.logical_size_x / 2.0, self.logical_size_y / 2.0, 0.0)
				if offset.magsq() > 100:  # tolerance for scrolling (arbitrary)
					self.renlayer.origin -= offset / 20.0

		for drawable in self.drawables:
			# draw shadows first
			if drawable.graphics.hasShadow():
				drawable.graphics.drawShadow(drawable.graphics_data, drawable.common_data)
			# draw actual things
			if not drawable.common_data.blink:
				drawable.graphics.draw(drawable.graphics_data, drawable.common_data)

		self.renlayer.renderSorted()

		sdl2.SDL_RenderSetLogicalSize(self.ren.sdlrenderer, int(self.res_x), int(self.res_y))
		self.title_renlayer.render()


# end draw()

	def reportMonsterDeath(self):
		self.num_monsters-=1
		# if self.num_monsters<=0:
		# 	self.setGameMode(eGameModes.win)
		# 	self.restart_cooldown = 6

	def requestNewEnemy(self,
											 entity_template,
											 pos=Vec3(0,0,0),
											 parent=False,
											 name=False):
		self.num_monsters+=1
		self.requestNewEntity(entity_template,pos,parent,name)

	def getDistanceBelow(self, pos):
		# ask collision manager
		self.collision_manager.getDistanceBelow(pos)

	def KFEvents(self):
		return[
				# wait a bit
				Delay(2),
			# wait a bit
				Delay(0.7),
				# EndGame()
			]



def run(tests=False):
	game = BunnyAdventure()
	if tests:
		game.runTests()
	game.run()
	return 0


if __name__ == "__main__":
	sys.exit(run(tests=True))
