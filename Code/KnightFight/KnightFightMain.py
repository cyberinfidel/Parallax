# import python libs
import sys

# import Parallax files
# 	add path to Parallax
sys.path.insert(1, '../')
# actually import files
from game import Game, eGameModes
from entity import eStates
from collision import CollisionManager
from vector import Vec3, Line, rand_num

# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')

#import Knight Fight files
from KnightFight.background import backgroundGraphics, BackgroundController
from KnightFight.hero import heroGraphics, HeroController, HeroCollider
from KnightFight.bat import batGraphics, BatController, BatCollider
from KnightFight.rain import rainGraphics, RainController
from KnightFight.reaper import reaperGraphics, ReaperController, ReaperCollider
from KnightFight.heart import heartGraphics, HeartIndicatorController
from KnightFight.title import titleGraphics, TitleController, eTitleStates
from director import DirectorController, Delay, SpawnEntity, EndGame
from KFdirector import SpawnEnemies, WaitForNoEnemies


class KnightFight(Game):
	def __init__(self):
		# do bare minimum to set up
		# most set up is in first update
		# this way I can restart the game
		super(KnightFight, self).__init__("Knight Fight", res_x= 320, res_y= 200, zoom = 3, fullscreen= False)

		###############################
		# set up background and title #
		###############################
		backgraphics = self.graphics_manager.makeTemplate(backgroundGraphics(self.renlayer))
		backcontroller = self.controller_manager.makeTemplate(
			{"Template": BackgroundController,
			 "Lines":
				 [
					 Line(Vec3(64, 136, 0), Vec3(256, 136, 0)),
					 Line(Vec3(0, 199, 0), Vec3(319, 199, 0)),
					 Line(Vec3(64, 136, 0), Vec3(0, 199, 0)),
					 Line(Vec3(256, 136, 0), Vec3(319, 199, 0)),
				 ],
			 }
		)
		back_t = self.entity_manager.makeEntityTemplate(graphics=backgraphics, controller=backcontroller)
		back = self.entity_manager.makeEntity(back_t)
		back.setPos(Vec3(0.0, 64.0, 0.0))
		self.drawables.append(back)

		title_graphics = self.graphics_manager.makeTemplate(titleGraphics(self.renlayer))
		title_controller = self.controller_manager.makeTemplate({"Template": TitleController})
		self.title_t = self.entity_manager.makeEntityTemplate(graphics=title_graphics, controller=title_controller)
		self.title = self.requestNewEntity(entity_template=self.title_t, pos=Vec3(48, 0, 195), parent=self, name="Title")
		self.title.setGamePad(self.input.getGamePad(0))

		self.raining = False
		self.setGameMode(eGameModes.title)

		self.collision_manager = CollisionManager(game=self)  # TODO: should this be a ComponentManager() like the others?

		###################
		# make components #
		###################
		# Graphics Templates
		bat_graphics = self.graphics_manager.makeTemplate(batGraphics(self.renlayer))
		reaper_graphics = self.graphics_manager.makeTemplate(reaperGraphics(self.renlayer))
		raingraphics = self.graphics_manager.makeTemplate(rainGraphics(self.renlayer))
		herographics = self.graphics_manager.makeTemplate(heroGraphics(self.renlayer))
		heartgraphics = self.graphics_manager.makeTemplate(heartGraphics(self.renlayer))

		# Controller Templates
		raincontroller = self.controller_manager.makeTemplate({"Template": RainController})
		herocontroller = self.controller_manager.makeTemplate({"Template": HeroController})
		bat_controller = self.controller_manager.makeTemplate({"Template": BatController})
		reaper_controller = self.controller_manager.makeTemplate({"Template": ReaperController})
		heart_controller = self.controller_manager.makeTemplate({"Template": HeartIndicatorController})

		# Collider Templates
		hero_collider = self.collision_manager.makeTemplate({"Template": HeroCollider})
		bat_collider = self.collision_manager.makeTemplate({"Template": BatCollider})
		reaper_collider = self.collision_manager.makeTemplate({"Template": ReaperCollider})

		#########################################
		# Make entity templates from components #
		#########################################
		self.bat_t = self.entity_manager.makeEntityTemplate(graphics=bat_graphics, controller=bat_controller,
																												collider=bat_collider)
		self.reaper_t = self.entity_manager.makeEntityTemplate(graphics=reaper_graphics, controller=reaper_controller,
																													 collider=reaper_collider)
		self.rain_t = self.entity_manager.makeEntityTemplate(graphics=raingraphics, controller=raincontroller)
		self.hero_t = self.entity_manager.makeEntityTemplate(graphics=herographics, controller=herocontroller,
																												 collider=hero_collider)

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

		# Always do this, unless paused:
		if self.game_mode!=eGameModes.paused:
			for index, updatable in reversed(list(enumerate(self.updatables))):
				updatable.update(dt)

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
				# first wave
				SpawnEnemies([
					SpawnEntity(self.reaper_t, Vec3(300, 35, 0), False, "Reaper 2"),
					SpawnEntity(self.reaper_t, Vec3(20, 35, 0), False, "Reaper 2"),
				]),
				Delay(1),
				# spawn second wave
				SpawnEnemies([
					SpawnEntity(self.reaper_t, Vec3(300, 35, 0), False, "Reaper 2"),
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
				Delay(0.5),
				# spawn other half of wave
				SpawnEnemies([
					SpawnEntity(self.bat_t, Vec3(300, 35, 5), False, "Bat 1"),
				]),
				Delay(0.5),
				SpawnEnemies([
					SpawnEntity(self.bat_t, Vec3(30, 35, 5), False, "Bat 1"),
				]),
				Delay(0.5),
				# spawn other half of wave
				SpawnEnemies([
					SpawnEntity(self.bat_t, Vec3(300, 35, 5), False, "Bat 1"),
				]),
				Delay(0.5),
				SpawnEnemies([
					SpawnEntity(self.bat_t, Vec3(30, 35, 5), False, "Bat 1"),
				]),
				Delay(0.5),
				# spawn other half of wave
				SpawnEnemies([
					SpawnEntity(self.bat_t, Vec3(300, 35, 5), False, "Bat 1"),
				]),
				Delay(0.5),

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
