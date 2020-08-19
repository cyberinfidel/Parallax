# import python libs
import sys
import gc

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
import utility

import log

#import PacBun files
import title
import level
import text
import high_score
import new_high_score
import message_box


class eGameModes(game.eGameModes):
	escape, high_score, new_high_score, numGameModes = range(game.eGameModes.numGameModes,game.eGameModes.numGameModes+4)

class PacBun(Game):

	def __init__(self):
		# do bare minimum to set up
		# most set up is in first update
		# this way I can restart the game
		super(PacBun, self).__init__("PacBun", res_x= 320, res_y= 288, zoom = 4, fullscreen= False)
		sdl2.mouse.SDL_ShowCursor(False)

		##########################
		# set up graphics layers #
		##########################
		self.renlayer = graphics.RenderLayer(self.ren)
		self.overlay_renlayer = graphics.RenderLayer(self.ren)
		self.setClearColor(graphics.Color(102 / 255, 129 / 255, 73 / 255))

		self.scroll = False
		self.quit_cooldown = 0.5
		self.title_cooldown_time = 3
		self.title_cooldown = self.title_cooldown_time

		self.score_font = self.overlay_renlayer.addFont("Fonts/PacBun/PacBun.ttf", 15)
		self.current_score = 0
		self.old_score = -1
		self.score_image = self.overlay_renlayer.addImageFromString(string="{0:0=4d}".format(self.current_score), font=self.score_font, color=graphics.Color(1, 1, 1, 1))

		##########################
		# set up sound           #
		##########################
		self.sound_mixer = sound.SoundMixer(self)
		#################
		# set up titles #
		#################

		####################################
		# get templates from config file   #
		####################################

		templates_data = utility.getDictDataFromFile('PB_templates.config',"templates")
		self.templates = self.makeTemplates(templates_data, self.renlayer)

		overlay_templates_data = utility.getDictDataFromFile('PB_templates.config','title_templates')
		self.templates.update(self.makeTemplates(overlay_templates_data, self.overlay_renlayer))

		self.levels = utility.getListDataFromFile("PB_levels.config", "levels")

		self.title = self.requestNewEntity(entity_template=self.templates['title'], pos=Vec3(36, 250, 50), parent=self, name="Title")
		self.title.setGamePad(self.input.getGamePad(0))

		# high score table
		self.high_score = self.requestNewEntity(self.templates['high_score'], parent=self, name="High Scores")
		self.high_score.graphics.initScore(self.high_score.common_data)


		# these are the entities that survive a game over
		# i.e. between games
		self.persistent_entities = [self.title, self.high_score]

		self.collision_manager = CollisionManager(game=self)

		self.setGameMode(eGameModes.title)
		self.current_level = 0





		# put all separate images into a texture atlas for (more) efficient rendering
		self.renlayer.makeAtlas(320)
		# self.renlayer.dumpAtlasToFiles("TA.png", "TA.json")

	# end init()

	def makeTemplates(self, templates_data, render_layer):
		templates = {}	# to hold the actual handles from the entity manager
		for template in templates_data:
			templates[template] = self.entity_manager.makeEntityTemplate(
				controller=templates_data[template]['controller'](self.controller_manager),
				collider=templates_data[template]['collider'](self.controller_manager),
				graphics=self.graphics_manager.makeTemplate(templates_data[template]['graphics'],
																										{'RenderLayer': render_layer})
			)
		return templates

	def updatePlay(self, dt):
		# draw score
		self.renlayer.setColorCast(graphics.Color(1, 1, 1, 1))
		self.setClearColor(graphics.Color(219 / 255, 182 / 255, 85 / 255))
		if self.current_score!= self.old_score:
			self.overlay_renlayer.replaceImageFromString(old_image=self.score_image, string="{0:0=4d}".format(self.current_score), font=self.score_font, color=graphics.Color(1, 1, 1, 1))
			self.old_score = self.current_score


		self.collision_manager.doCollisionsWithSingleEntity(self.bunny)  # collisions between monsters

	##################################################

	def updateTitle(self, dt):


		self.title.setState(title.eTitleStates.title)
		gc.enable()
		self.current_level = 0
		self.current_score = 0
		self.setClearColor(graphics.Color(102 / 255, 129 / 255, 73 / 255))
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

		# initialise map
		self.level = level.Level(self,self.levels[self.current_level], self.templates['tile'])

		# initialise creatures
		self.bunny = self.requestNewEntity(self.templates['pacbun'], pos=self.level.getBunnyStart(), parent=self, name="Bunny")
		game_pad = self.input.getGamePad(0)
		if game_pad:
			self.bunny.setGamePad(game_pad)
		self.bunny.controller_data.level = self.level

		self.foxes = []
		for fox_start in self.level.getFoxStarts():
			this_fox = self.requestNewEntity(self.templates['fox'], pos=fox_start[0], parent=self, name="Fox")
			this_fox.controller_data.bunny = self.bunny
			this_fox.controller_data.level = self.level
			this_fox.controller_data.type = fox_start[1]
			self.foxes.append(this_fox)

		self.message(self.level.message, Vec3(20,20,0), duration=10, color=graphics.Color(1,1,1))

		gc.collect()
		gc.disable()
		self.setGameMode(eGameModes.play)
		self.updatePlay(dt)
		####################################################

	def updateGameOver(self, dt):
		self.restart_cooldown-=dt

		# fade to black
		self.title.setState(title.eTitleStates.game_over)
		fade_factor = max(0,min(1,self.restart_cooldown-0.5))
		self.renlayer.setColorCast(graphics.Color(fade_factor,
																							fade_factor,
																							fade_factor,
																							fade_factor))
		self.setClearColor(graphics.Color((220 / 255) * fade_factor,
																			(182/255) * fade_factor,
																			(85/255) * fade_factor))

		if self.restart_cooldown<=0:
			self.killPlayEntities()
			self.cleanUpDead()

			# do high scoreness
			if self.high_score.controller.isHighScore(self.high_score, self.current_score):
				self.new_high_score = self.requestNewEntity(self.templates['new_high_score'], parent=self, name="New High Score")
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
			self.running=False
			return
		####################################################

	def updateInit(self, dt):
		pass
		####################################################

	def updatePaused(self, dt):
		self.renlayer.setColorCast(graphics.Color(0.5, 0.5, 0.5, 1))
		self.setClearColor(graphics.Color(110 / 255, 91 / 255, 43 / 255))
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
			for updatable in self.updatables:
				updatable.update(dt)
			for audible in self.audibles:
				audible.sounds.play(audible.sounds_data, audible.common_data)

			self.cleanUpDead()


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

	def message(self, text, pos, color=graphics.Color(1, 1, 1, 1), duration=0):
		message = self.requestNewEntity(entity_template=self.templates['message'],
													pos=pos,
													parent=self,
													name= f"message: {text}"
		)
		message.graphics.init(data = message.graphics_data,
													ren_layer = self.overlay_renlayer,
													message=text,
													font=0,
													color = color,
													duration=duration
													)

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
