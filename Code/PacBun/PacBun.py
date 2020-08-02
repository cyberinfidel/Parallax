# import python libs
import sys

import sdl2.mouse

# import Parallax files
# 	add path to Parallax
sys.path.append('../')
# actually import files
from game import Game, eGameModes
from entity import eStates
import entity
from collision import CollisionManager
from vector import Vec3, rand_num
import graphics
import sound
import director
import enum
import gc


# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')

#import PacBun files
import title
import heart
import bunny
import fox
import tile
import level


class PacBun(Game):
	def __init__(self):
		# do bare minimum to set up
		# most set up is in first update
		# this way I can restart the game
		super(PacBun, self).__init__("PacBun", res_x= 320, res_y= 320, zoom = 3, fullscreen= False)
		sdl2.mouse.SDL_ShowCursor(False)

		##########################
		# set up graphics layers #
		##########################
		self.renlayer = graphics.RenderLayer(self.ren)
		self.overlay_renlayer = graphics.RenderLayer(self.ren)
		self.scroll = False
		self.quit_cooldown = 0.5

		##########################
		# set up sound           #
		##########################
		self.sound_mixer = sound.SoundMixer(self)
		###############################
		# set up background and title #
		###############################
		# back_controller = background.makeController(self.controller_manager)
		# back = self.entity_manager.makeEntity(
		# 	self.entity_manager.makeEntityTemplate(
		# 		graphics=self.graphics_manager.makeTemplate(background.makeGraphics(self.renlayer)),
		# 		controller= back_controller)
		# )
		# back.setPos(Vec3(0.0, 0.0, 64.0))


		self.title_t = self.entity_manager.makeEntityTemplate(graphics=title.makeGraphics(self.graphics_manager, self.overlay_renlayer), controller=title.makeController(self.controller_manager))
		self.title = self.requestNewEntity(entity_template=self.title_t, pos=Vec3(36, 250, 50), parent=self, name="Title")
		self.title.setGamePad(self.input.getGamePad(0))

		self.collision_manager = CollisionManager(game=self)  # TODO: should this be a ComponentManager() like the others?

		self.setGameMode(eGameModes.title)
		self.current_level = 0


		###################
		# make components #
		###################


		# info bar
		self.heart_t = self.entity_manager.makeEntityTemplate(graphics=heart.makeGraphics(self.graphics_manager, self.overlay_renlayer), controller=heart.makeController(self.controller_manager))

		self.bunny_t = self.entity_manager.makeEntityTemplate(graphics=bunny.makeGraphics(self.graphics_manager, self.renlayer), controller = bunny.makeController(self.controller_manager), collider=bunny.makeCollider(self.collision_manager))

		self.fox_t = self.entity_manager.makeEntityTemplate(graphics=fox.makeGraphics(self.graphics_manager, self.renlayer), controller = fox.makeController(self.controller_manager), collider=fox.makeCollider(self.collision_manager))

		self.tile_t = self.entity_manager.makeEntityTemplate(graphics=tile.makeGraphics(self.graphics_manager, self.renlayer), controller = tile.makeController(self.controller_manager) )

	# define level maps
		self.levels = [
			{
				"Map":[
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHH B HHHHHHHHH",
				"HHHHHHHH   HHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
				"HHHHHHHHHHHHHHHHHHHH",
			]
			},{
			"Map":[
			"HHHHHHHHHHHHHHHHHHHH",
			"H1                 H",
			"H HHHH HHHHHH HHHH H",
			"H oHHH HH          H",
			"H HHHH HH HHHoH HHHH",
			"H HHHH HH HHHHH HHHH",
			"H                  H",
			"H HH HHHHHH HHHHHH H",
			"H HH HHH    HHHHHH H",
			"H HH HHH HHHHHHHHH H",
			"H 3H           BoH H",
			"HH H HHHHHHHHHH HH H",
			"HH H HHHHHHH    HH H",
			"H            HH HH H",
			"H HH HHHHHHH HH HH H",
			"H HH HHHHHHH HH HH H",
			"H Ho            HH H",
			"H HHHHHHHHHHHHHHHH H",
			"H                 2H",
			"HHHHHHHHHHHHHHHHHHHH",
			]
			}, {
			"Map": [
			"HHHHHHHHHHHHHHHHHHHH",
			"H1                 H",
			"H HoHH HHHHHH HHHH H",
			"H HHHH HH          H",
			"H      HH HHHoH HHHH",
			"H HHHH HH HHHHH HHHH",
			"H                  H",
			"H HH H HHHH HH HHH H",
			"H HH H      HH     H",
			"H HH H HHHHHHH HHH H",
			"H H            BoH H",
			"H H  HH HH HHHH HH H",
			"H H  HH HH H    HH H",
			"H            HH HH H",
			"H HH H HH HH HH HH H",
			"H HH H HH HH HH HH H",
			"H Ho            HH H",
			"H HHHH HHHHHH HHHH H",
			"H                 2H",
			"HHHHHHHHHHHHHHHHHHHH",
		]},
		]

	# end init()


	###########
	#  update #
	###########

	def update(self, dt):

		if self.game_mode==eGameModes.init:

			pass

##################################################
		elif self.game_mode==eGameModes.title:
			self.current_level = 0
			self.setClearColour(sdl2.ext.Color(20,90,10))
			gc.collect()
		##################################################
		elif self.game_mode==eGameModes.start:
			gc.enable()
			gc.collect()
			if len(gc.garbage)>0: print(gc.garbage)
			# set up new game and clean up anything from last game
			self.num_monsters = 0
			self.killPlayEntities()
			self.cleanUpDead()
			self.restart_cooldown = 2
			self.setClearColour(sdl2.ext.Color(219, 182, 85))

			# initialise map
			self.level = level.Level(self,self.levels[self.current_level])

			self.bunny = self.requestNewEntity(self.bunny_t, pos=self.level.getBunnyStart(), parent=self, name="Bunny")
			self.foxes = []
			for fox_start in self.level.getFoxStarts():
				this_fox = self.requestNewEntity(self.fox_t, pos=fox_start[0], parent=self, name="Fox")
				this_fox.controller_data.bunny = self.bunny
				this_fox.controller_data.level = self.level
				this_fox.controller_data.type = fox_start[1]
				self.foxes.append(this_fox)


			# make hero 2
			game_pad = self.input.getGamePad(0)
			if game_pad:
				self.bunny.setGamePad(game_pad)
			self.bunny.controller_data.level = self.level



			# # set up life indicator in top left
			# for n in range(1, 6):
			# 	heart = self.entity_manager.makeEntity(self.heart_t, "Heart")
			# 	heart.setPos(Vec3(10 * n, 190, 0))
			# 	self.drawables.append(heart)
			# 	self.updatables.append(heart)
			# 	heart.common_data.parent = self.bunny
			# 	heart.common_data.state = eStates.fade
			# 	heart.controller_data.health_num = n

			gc.collect()
			gc.disable()
			self.setGameMode(eGameModes.play)
		##################################################
		elif self.game_mode==eGameModes.play:
			pass

		####################################################

		elif self.game_mode==eGameModes.game_over:

			self.restart_cooldown-=dt
			self.title.setState(title.eTitleStates.game_over)
			if self.restart_cooldown<=0:
				self.setGameMode(eGameModes.title)
				self.cleanUpDead()
		####################################################

		elif self.game_mode==eGameModes.win:
			self.restart_cooldown-=dt
			self.title.setState(title.eTitleStates.win)
			if self.restart_cooldown<=0:
				self.current_level+=1
				if self.current_level>=len(self.levels):
					self.setGameMode(eGameModes.game_over)
				else:
					self.setGameMode(eGameModes.start)
				self.cleanUpDead()


		####################################################

		elif self.game_mode==eGameModes.quit:
			self.quit_cooldown-=dt
			self.title.setState(title.eTitleStates.quit)
			if self.quit_cooldown<=0:
				self.running=False
				return


		# Always do this, unless paused:
		if self.game_mode!=eGameModes.paused:
			for index, updatable in reversed(list(enumerate(self.updatables))):
				updatable.update(dt)
			for audible in self.audibles:
				audible.sounds.play(audible.sounds_data, audible.common_data)

			if self.game_mode==eGameModes.play:
				self.collision_manager.doCollisionsWithSingleEntity(self.bunny) # collisions between monsters
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
		return self.bunny.common_data.pos

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
			# draw actual things
			if not drawable.common_data.blink:
				drawable.graphics.draw(drawable.graphics_data, drawable.common_data)

		self.renlayer.renderSortedByZThenY()
		self.overlay_renlayer.render()


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






def run(tests=False):
	game = PacBun()
	if tests:
		game.runTests()
	game.run()
	return 0


if __name__ == "__main__":
	sys.exit(run(tests=True))
