# import python libs
import sys

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

#import Meadow files
import Meadow.bunny as bunny
import Meadow.background as back
from Meadow.title import titleGraphics, TitleController, eTitleStates
from Meadow.rain import rainGraphics, RainController
import Meadow.present as present
import Meadow.butterfly as butterfly

class Meadow(Game):
	def __init__(self):
		# do bare minimum to set up
		# most set up is in first update
		# this way I can restart the game
		super(Meadow, self).__init__("Meadow", res_x= 640, res_y= 400, zoom = 3, fullscreen= False)
		self.collision_manager = CollisionManager(game=self)  # TODO: should this be a ComponentManager() like the others?

		##########################
		# set up graphics layers #
		##########################
		self.renlayer = graphics.RenderLayer(self.ren)
		self.title_renlayer = graphics.RenderLayer(self.ren)
		self.scroll = False

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

		back_graphics = self.graphics_manager.makeTemplate(back.backgroundGraphics(self.renlayer))
		back_controller = self.controller_manager.makeTemplate({"Template": back.BackgroundController})
		self.back_t = self.entity_manager.makeEntityTemplate(graphics=back_graphics, controller=False)
		self.back = self.requestNewEntity(entity_template=self.back_t, pos=Vec3(0, 270, 0), parent=self, name="back")

		self.present_t = self.entity_manager.makeEntityTemplate(
			graphics=self.graphics_manager.makeTemplate(present.graphics(self.renlayer)),
			controller=self.controller_manager.makeTemplate({"Template": present.Controller}),
			collider=self.collision_manager.makeTemplate({"Template": present.Collider})
			)


		###################
		# make components #
		###################
		# Graphics Templates
		raingraphics = self.graphics_manager.makeTemplate(rainGraphics(self.renlayer))
		bunny_graphics = self.graphics_manager.makeTemplate(bunny.bunnyGraphics(self.renlayer))

		# Sound Templates
		bunny_sounds = False #self.sound_manager.makeTemplate(heroSounds(self.sound_mixer))

		# Controller Templates
		raincontroller = self.controller_manager.makeTemplate({"Template": RainController})
		bunny_controller = self.controller_manager.makeTemplate({"Template": bunny.BunnyController})
		bfly_controller = self.controller_manager.makeTemplate({"Template": butterfly.Controller})

		# Collider Templates
		bunny_collider = self.collision_manager.makeTemplate({"Template": bunny.BunnyCollider})

		#########################################
		# Make entity templates from components #
		#########################################
		self.rain_t = self.entity_manager.makeEntityTemplate(graphics=raingraphics, controller=raincontroller)
		self.bfly_templates =[]
		for bfly_graphics in [butterfly.graphics, butterfly.graphics2, butterfly.graphics3]:
			self.bfly_templates.append(self.entity_manager.makeEntityTemplate(graphics=self.graphics_manager.makeTemplate(bfly_graphics(self.renlayer)), controller=bfly_controller))

		self.bunny_t = self.entity_manager.makeEntityTemplate(graphics=bunny_graphics,
																												 sounds = bunny_sounds,
																												 controller=bunny_controller,
																												 collider=bunny_collider,
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

			# make bunny
			self.bunny = self.requestNewEntity(entity_template=self.bunny_t, pos=Vec3(160, 60, 0), parent=False, name="Bunny")
			self.bunny.setGamePad(self.input.getGamePad(0))

			# self.present = self.requestNewEntity(entity_template=self.present_t, pos=Vec3(400, 60, 0), parent=self, name="present")
			# self.present.controller.setButterflyTemplates(self.bfly_templates)

			self.rain_cooldown = 500
			self.restart_cooldown=60
			self.setGameMode(eGameModes.play)
		##################################################
		elif self.game_mode==eGameModes.play:

			if (rand_num(10) == 0 and len(self.drawables)<5):
				bfly = self.entity_manager.makeEntity(self.bfly_templates[rand_num(3)])
				bfly.setPos(Vec3(rand_num(640), rand_num(270), 500))
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

			###############
			# scroll view #
			###############
			if self.scroll:
				offset = self.renlayer.getOrigin() - self.bunny.common_data.pos + Vec3(160,64,0)
				if offset.magsq()>100:
					self.renlayer.origin-=offset/40.0
					self.renlayer.origin.z = 0 # make current ground level when can
					if self.renlayer.origin.y<0:
						self.renlayer.origin.y=0

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

		for drawable in self.drawables:
			# draw shadows first
			if drawable.graphics.hasShadow():
				drawable.graphics.drawShadow(drawable.graphics_data, drawable.common_data)
			# draw actual things
			if not drawable.common_data.blink:
				drawable.graphics.draw(drawable.graphics_data, drawable.common_data)

		self.renlayer.renderSorted()
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


	def KFEvents(self):
		return[
				# wait a bit
				Delay(2),
			# wait a bit
				Delay(0.7),
				# EndGame()
			]



def run(tests=False):
	game = Meadow()
	if tests:
		game.runTests()
	game.run()
	return 0


if __name__ == "__main__":
	sys.exit(run(tests=True))
