# import python libs
import sys

import sdl2.mouse

# import Parallax files
# 	add path to Parallax
sys.path.append('../')
# actually import files
from game import Game, eGameModes
from entity import eStates
from collision import CollisionManager
from vector import Vec3, rand_num
import graphics
import sound
from director import DirectorController, Delay, SpawnEntity, EndGame

# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')

#import Knight Fight files
from KnightFight.background import backgroundGraphics, BackgroundController, backLGraphics, backRGraphics
from KnightFight.hero import heroGraphics, heroSounds, HeroController, HeroCollider
from KnightFight.bat import batGraphics, batSounds, BatController, BatCollider
import goblinarcher
from KnightFight.rain import rainGraphics, RainController
from KnightFight.reaper import reaperGraphics, ReaperController, ReaperCollider
from KnightFight.heart import heartGraphics, HeartIndicatorController
from KnightFight.title import titleGraphics, TitleController, eTitleStates
from KFdirector import SpawnEnemies, WaitForNoEnemies


class KnightFight(Game):
	def __init__(self):
		# do bare minimum to set up
		# most set up is in first update
		# this way I can restart the game
		super(KnightFight, self).__init__("Knight Fight", res_x= 320, res_y= 200, zoom = 3, fullscreen= False)
		sdl2.mouse.SDL_ShowCursor(False)

		##########################
		# set up graphics layers #
		##########################
		self.renlayer = graphics.RenderLayer(self.ren)
		self.title_renlayer = graphics.RenderLayer(self.ren)
		self.scroll = False
		self.quit_cooldown = 3

		##########################
		# set up sound           #
		##########################
		self.sound_mixer = sound.SoundMixer(self)
		###############################
		# set up background and title #
		###############################
		back_controller = self.controller_manager.makeTemplate(
					{"Template": BackgroundController, })
		back = self.entity_manager.makeEntity(
			self.entity_manager.makeEntityTemplate(
				graphics=self.graphics_manager.makeTemplate(backgroundGraphics(self.renlayer)),
				controller= back_controller)
		)
		back.setPos(Vec3(0.0, 64.0, 0.0))
		self.drawables.append(back)

		backL = self.entity_manager.makeEntity(
			self.entity_manager.makeEntityTemplate(
				graphics=self.graphics_manager.makeTemplate(backLGraphics(self.renlayer)),
				controller=back_controller)
		)
		backL.setPos(Vec3(0.0, 30.0, 0.0))
		self.drawables.append(backL)

		backR = self.entity_manager.makeEntity(
			self.entity_manager.makeEntityTemplate(
				graphics=self.graphics_manager.makeTemplate(backRGraphics(self.renlayer)),
				controller=back_controller)
		)
		backR.setPos(Vec3(289.0, 30.0, 0.0))
		self.drawables.append(backR)

		title_graphics = self.graphics_manager.makeTemplate(titleGraphics(self.title_renlayer))
		title_controller = self.controller_manager.makeTemplate({"Template": TitleController})
		self.title_t = self.entity_manager.makeEntityTemplate(graphics=title_graphics, controller=title_controller)
		self.title = self.requestNewEntity(entity_template=self.title_t, pos=Vec3(48, 50, 145), parent=self, name="Title")
		self.title.setGamePad(self.input.getGamePad(0))

		self.raining = False

		self.collision_manager = CollisionManager(game=self)  # TODO: should this be a ComponentManager() like the others?

		self.setGameMode(eGameModes.title)


		###################
		# make components #
		###################
		# Graphics Templates
		bat_graphics = self.graphics_manager.makeTemplate(batGraphics(self.renlayer))
		goblin_archer_graphics = self.graphics_manager.makeTemplate(goblinarcher.graphics(self.renlayer))
		reaper_graphics = self.graphics_manager.makeTemplate(reaperGraphics(self.renlayer))
		raingraphics = self.graphics_manager.makeTemplate(rainGraphics(self.renlayer))
		herographics = self.graphics_manager.makeTemplate(heroGraphics(self.renlayer))
		heartgraphics = self.graphics_manager.makeTemplate(heartGraphics(self.title_renlayer))

		# Sound Templates
		hero_sounds = self.sound_manager.makeTemplate(heroSounds(self.sound_mixer))
		bat_sounds = self.sound_manager.makeTemplate(batSounds(self.sound_mixer))

		# Controller Templates
		raincontroller = self.controller_manager.makeTemplate({"Template": RainController})
		herocontroller = self.controller_manager.makeTemplate({"Template": HeroController})
		bat_controller = self.controller_manager.makeTemplate({"Template": BatController})
		goblin_archer_controller = self.controller_manager.makeTemplate({"Template": goblinarcher.Controller})
		reaper_controller = self.controller_manager.makeTemplate({"Template": ReaperController})
		heart_controller = self.controller_manager.makeTemplate({"Template": HeartIndicatorController})

		# Collider Templates
		hero_collider = self.collision_manager.makeTemplate({"Template": HeroCollider})
		bat_collider = self.collision_manager.makeTemplate({"Template": BatCollider})
		goblin_archer_collider = self.collision_manager.makeTemplate({"Template": goblinarcher.Collider})
		reaper_collider = self.collision_manager.makeTemplate({"Template": ReaperCollider})

		#########################################
		# Make entity templates from components #
		#########################################
		self.bat_t = self.entity_manager.makeEntityTemplate(graphics=bat_graphics,
																												sounds = bat_sounds,
																												controller=bat_controller,
																												collider=bat_collider)
		self.goblin_archer_t = self.entity_manager.makeEntityTemplate(graphics=goblin_archer_graphics, controller=goblin_archer_controller,
																												collider=goblin_archer_collider)
		self.reaper_t = self.entity_manager.makeEntityTemplate(graphics=reaper_graphics, controller=reaper_controller,
																													 collider=reaper_collider)
		self.rain_t = self.entity_manager.makeEntityTemplate(graphics=raingraphics, controller=raincontroller)
		self.hero_t = self.entity_manager.makeEntityTemplate(graphics=herographics,
																												 sounds = hero_sounds,
																												 controller=herocontroller,
																												 collider=hero_collider,
																												 )

		# info bar
		self.heart_t = self.entity_manager.makeEntityTemplate(graphics=heartgraphics, controller=heart_controller)

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

			# make hero
			self.hero = self.requestNewEntity(entity_template=self.hero_t, pos=Vec3(160, 60, 0), parent=False, name="Hero")
			self.hero.setGamePad(self.input.getGamePad(0))

			# set up life indicator in top left
			for n in range(1, 6):
				heart = self.entity_manager.makeEntity(self.heart_t, "Heart")
				heart.setPos(Vec3(10 * n, 0, 190))
				self.drawables.append(heart)
				self.updatables.append(heart)
				heart.common_data.parent = self.hero
				heart.common_data.state = eStates.fade
				heart.controller_data.health_num = n

			self.rain_cooldown = 500
			self.setGameMode(eGameModes.play)
		##################################################
		elif self.game_mode==eGameModes.play:
			# rain
			if self.raining:
				if (rand_num(10)==0):
					rain = self.entity_manager.makeEntity(self.rain_t)
					rain.setState(RainController.state_fall)
					rain.setPos(Vec3(rand_num(320), rand_num(64), 200))
					self.drawables.append(rain)
					self.updatables.append(rain)
			self.rain_cooldown -=1
			if self.rain_cooldown<=0:
				self.rain_cooldown=rand_num(500)+500
				self.raining = not self.raining

			if self.hero.getState()==eStates.dead:
				self.setGameMode(eGameModes.game_over)
				self.restart_cooldown=3

			###############
			# scroll view #
			###############
			if self.scroll:
				offset = self.renlayer.getOrigin() - self.hero.common_data.pos + Vec3(160,64,0)
				if offset.magsq()>1000:
					self.renlayer.origin-=offset/40.0
					self.renlayer.origin.z = 0 # make current ground level when can

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
			self.title.setState(eTitleStates.win)
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
		self.cleanUpDead()


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
			SpawnEnemies([
				SpawnEntity(self.bat_t, Vec3(290, 35, 5), False, "Bat 1"),
			]),

			SpawnEnemies([
					SpawnEntity(self.goblin_archer_t, Vec3(290, 35, 0), False, "Goblin Archer"),
				]),
			SpawnEnemies([
					SpawnEntity(self.goblin_archer_t, Vec3(150, 35, 0), False, "Goblin Archer"),
				]),
			# wait a bit
				Delay(0.7),
				SpawnEnemies([
				SpawnEntity(self.reaper_t, Vec3(30, 35, 0), False, "Reaper"),
				]),
				Delay(rand_num(1)+0.5),

				# wait until all monsters destroyed
				WaitForNoEnemies(),
				# wait a bit
				Delay(4),

				# first wave
				SpawnEnemies([
					SpawnEntity(self.reaper_t, Vec3(300, 35, 0), False, "Reaper 2"),
				]),
				Delay(rand_num(1)+0.5),
				SpawnEnemies([
					SpawnEntity(self.reaper_t, Vec3(20, 35, 0), False, "Reaper 2"),
				]),

				# wait until all monsters destroyed
				WaitForNoEnemies(),
				# wait a bit
				Delay(4),

				# second  wave
				SpawnEnemies([
					SpawnEntity(self.bat_t, Vec3(30, 35, 5), False, "Bat 1"),
				]),
				Delay(rand_num(1)+0.5),
				# spawn other half of wave
				SpawnEnemies([
					SpawnEntity(self.bat_t, Vec3(300, 35, 5), False, "Bat 1"),
				]),
				Delay(rand_num(1)+0.5),
				SpawnEnemies([
					SpawnEntity(self.bat_t, Vec3(155, 110, 5), False, "Bat 1"),
				]),
				Delay(rand_num(1)+0.5),
				# spawn other half of wave
				SpawnEnemies([
					SpawnEntity(self.bat_t, Vec3(300, 35, 5), False, "Bat 1"),
				]),
				Delay(rand_num(1)+0.5),
				SpawnEnemies([
					SpawnEntity(self.bat_t, Vec3(30, 35, 5), False, "Bat 1"),
				]),
				Delay(rand_num(1)+0.5),
				# spawn other half of wave
				SpawnEnemies([
					SpawnEntity(self.bat_t, Vec3(155, 110, 5), False, "Bat 1"),
				]),

				# wait until all monsters destroyed
				WaitForNoEnemies(),

				# wait a bit
				Delay(2),

				# ...

				WaitForNoEnemies(),
				# wait a bit
				Delay(2),
				# signal game complete
				EndGame()
			]



def run(tests=False):
	game = KnightFight()
	if tests:
		game.runTests()
	game.run()
	return 0


if __name__ == "__main__":
	sys.exit(run(tests=True))
