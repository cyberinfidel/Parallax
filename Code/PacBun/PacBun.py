# import python libs
import sys

import sdl2.mouse

# import Parallax files
# 	add path to Parallax
sys.path.append('../')
# actually import files
from game import Game, eGameModes
import game
from entity import eStates
import entity
from collision import CollisionManager
from vector import Vec3
import graphics
import sound
import gc


# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')

#import PacBun files
import title
import bunny
import fox
import tile
import level
import text
import high_score
import new_high_score


class eGameModes(game.eGameModes):
	escape, high_score, new_high_score, numGameModes = range(game.eGameModes.numGameModes,game.eGameModes.numGameModes+4)

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
		self.title_cooldown_time = 3
		self.title_cooldown = self.title_cooldown_time

		self.font_manager = text.FontManager(self.ren)
		self.score_font = self.font_manager.addFontFromFile("Fonts/Silom/Silom.ttf", 11)
		self.current_score = 0
		self.old_score = -1
		self.score_image = self.overlay_renlayer.addImageFromString(font_manager=self.font_manager, string="{0:0=4d}".format(self.current_score), font=self.score_font, color=sdl2.SDL_Color(255,255,255,255))

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

		# high score table
		self.high_score_t = self.entity_manager.makeEntityTemplate(
			controller=high_score.makeController(self.controller_manager),
			graphics=high_score.makeGraphics(manager=self.graphics_manager,
																	render_layer=self.overlay_renlayer,
																	font_manager=self.font_manager)
		)
		self.high_score = self.requestNewEntity(self.high_score_t, parent=self, name="High Scores")
		self.high_score.graphics.initScore(self.high_score.common_data)

		# entity for getting initials on a new high score
		self.new_high_score_t = self.entity_manager.makeEntityTemplate(
			controller=new_high_score.makeController(self.controller_manager),
			graphics=new_high_score.makeGraphics(manager=self.graphics_manager,
																	render_layer=self.overlay_renlayer,
																	font_manager=self.font_manager)
		)


		# these are the entities that survive a game over
		# i.e. between games
		self.persistent_entities = [self.title, self.high_score]

		self.collision_manager = CollisionManager(game=self)

		self.setGameMode(eGameModes.title)
		self.current_level = 0
		self.setClearColour(sdl2.ext.Color(102,129,73))



		############################
		# make ingame components   #
		############################


		# info bar
		# self.heart_t = self.entity_manager.makeEntityTemplate(graphics=heart.makeGraphics(self.graphics_manager, self.overlay_renlayer), controller=heart.makeController(self.controller_manager))

		self.bunny_t = self.entity_manager.makeEntityTemplate(graphics=bunny.makeGraphics(self.graphics_manager, self.renlayer), controller = bunny.makeController(self.controller_manager), collider=bunny.makeCollider(self.collision_manager))

		self.fox_t = self.entity_manager.makeEntityTemplate(graphics=fox.makeGraphics(self.graphics_manager, self.renlayer), controller = fox.makeController(self.controller_manager), collider=fox.makeCollider(self.collision_manager))

		self.tile_t = self.entity_manager.makeEntityTemplate(graphics=tile.makeGraphics(self.graphics_manager, self.renlayer), controller = tile.makeController(self.controller_manager) )

		self.renlayer.makeAtlas()
		self.renlayer.dumpAtlasToFiles("TA_images.png","TA_data")

	# define level maps
		self.levels = [
			{
				"Message":"Poo on every path!",
				"Map": [
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HH   HHHHHHHHHH   HH",
					"HH H HHHHHHHHHH H HH",
					"HH 1oHHHHHHHHHHo  HH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHH  B  HHHHHHHH",
					"HHHHHHHH   HHHHHHHHH",
					"HHHHHHHHH HHHHHHHHHH",
					"HHHHHHHHH HHHHHHHHHH",
					"HHHoHHHHH HHHHHHoHHH",
					"HHH HHHHH HHHHHH HHH",
					"HHH              HHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
				]
			}, {
				"Message":"Avoid the fox!",
				"Map": [
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHB   oHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHH        oHHHHHH",
					"HHHHH HHHHHH HHHHHHH",
					"HHHH            HHHH",
					"HHHH H HHHHH HH HHHH",
					"HHHH HoHHHHH HH HHHH",
					"HHHH HHHHHHH HH HHHH",
					"HHHH          1 HHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
					"HHHHHHHHHHHHHHHHHHHH",
				]
			}, {
				"Message":"Not all foxes think the same way...",
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
			"Message": "Poo on every path",
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

		self.message_x = 0

	# end init()

	def updatePlay(self, dt):
		# draw score
		if self.current_score!= self.old_score:
			self.overlay_renlayer.replaceImageFromString(old_image=self.score_image, font_manager=self.font_manager, string="{0:0=4d}".format(self.current_score), font=self.score_font, color=sdl2.SDL_Color(255,255,255,255))
			self.old_score = self.current_score


		self.collision_manager.doCollisionsWithSingleEntity(self.bunny)  # collisions between monsters
		# clean up dead entities
		self.cleanUpDead()

	##################################################

	def updateTitle(self, dt):

		self.title.setState(title.eTitleStates.title)
		gc.enable()
		self.current_level = 0
		self.current_score = 0
		self.setClearColour(sdl2.ext.Color(102,129,73))
		gc.collect()
		self.title_cooldown-=dt
		if self.title_cooldown<0:
			self.title_cooldown = self.title_cooldown_time
			self.setGameMode(eGameModes.high_score)
		# log("switching to high score")
	##################################################

	def updateStart(self, dt):

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

		# initialise creatures
		self.bunny = self.requestNewEntity(self.bunny_t, pos=self.level.getBunnyStart(), parent=self, name="Bunny")
		game_pad = self.input.getGamePad(0)
		if game_pad:
			self.bunny.setGamePad(game_pad)
		self.bunny.controller_data.level = self.level

		self.foxes = []
		for fox_start in self.level.getFoxStarts():
			this_fox = self.requestNewEntity(self.fox_t, pos=fox_start[0], parent=self, name="Fox")
			this_fox.controller_data.bunny = self.bunny
			this_fox.controller_data.level = self.level
			this_fox.controller_data.type = fox_start[1]
			self.foxes.append(this_fox)


		gc.collect()
		gc.disable()
		self.setGameMode(eGameModes.play)
		self.updatePlay(dt)
		####################################################

	def updateGameOver(self, dt):
		self.restart_cooldown-=dt
		self.title.setState(title.eTitleStates.game_over)
		if self.restart_cooldown<=0:
			self.killPlayEntities()
			self.cleanUpDead()

			# do high scoreness
			if self.high_score.controller.isHighScore(self.high_score, self.current_score):
				self.new_high_score = self.requestNewEntity(self.new_high_score_t, parent=self, name="New High Score")
				self.new_high_score.graphics.updateInitials(self.new_high_score)
				game_pad = self.input.getGamePad(0)
				if game_pad:
					self.new_high_score.setGamePad(game_pad)

				self.setGameMode(eGameModes.new_high_score)
				self.title.setState(title.eTitleStates.new_high_score)
				return

			self.setGameMode(eGameModes.title)
		####################################################

	def updateEscape(self, dt):
		self.title.setState(title.eTitleStates.escape)

		####################################################
	def updateNewHighScore(self, dt):


		pass

	####################################################

	def updateWin(self, dt):
		self.bunny.setState(entity.eStates.dead)
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

	def updateQuit(self, dt):
		self.quit_cooldown-=dt
		self.title.setState(title.eTitleStates.quit)
		if self.quit_cooldown<=0:
			gc.enable()
			self.font_manager.delete()
			self.running=False
			return
		####################################################

	def updateInit(self, dt):
		pass
		####################################################

	def updatePaused(self, dt):
		self.title.update(dt)
		####################################################

	def updateHighScore(self, dt):
		self.title_cooldown-=dt
		if self.title_cooldown<0:
			self.title_cooldown = self.title_cooldown_time
			self.setGameMode(eGameModes.title)
			# log("switching to title")
		####################################################

	###########
	#  update #
	###########
	def update(self, dt):
		(
			self.updateQuit,
			self.updateInit,
			self.updateTitle,
			self.updateStart,
			self.updatePlay,
			self.updateGameOver,
			self.updateWin,
			self.updatePaused,
			self.updateEscape,
			self.updateHighScore,
			self.updateNewHighScore
		)[self.game_mode](dt)

		# Always do this, unless paused:
		if self.game_mode!=eGameModes.paused:
			for index, updatable in reversed(list(enumerate(self.updatables))):
				updatable.update(dt)
			for audible in self.audibles:
				audible.sounds.play(audible.sounds_data, audible.common_data)


# end update() #################################################################

	def cleanUpDead(self):
		self.updatables[:] = [x for x in self.updatables if x.getState() != eStates.dead]
		self.collision_manager.cleanUpDead()
		self.drawables[:] = [x for x in self.drawables if x.getState() != eStates.dead]
		self.audibles[:] = [x for x in self.audibles if x.getState() != eStates.dead]
		self.entity_manager.deleteDead()

	def killPlayEntities(self):
		for updatable in self.updatables:
			if not (updatable in self.persistent_entities):
				updatable.common_data.state = eStates.dead
		self.cleanUpDead()


	def requestTarget(self,pos):
		return self.bunny.common_data.pos

	def reportScore(self, increment):
		self.current_score+=increment

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

		if self.game_mode==eGameModes.play:
			self.overlay_renlayer.queueImage(self.score_image, 99, 318, 0)
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

	def addNewHighScore(self, initials):
		self.high_score.controller.updateScores(score_data=self.high_score.controller_data.scores_data, initials=initials, new_score=self.current_score)
		self.high_score.graphics.updateScores(self.high_score)
		self.new_high_score.common_data.state = entity.eStates.dead
		self.setGameMode(eGameModes.title)


def run(tests=False):
	game = PacBun()
	if tests:
		game.runTests()
	game.run()
	return 0


if __name__ == "__main__":
	sys.exit(run(tests=True))
