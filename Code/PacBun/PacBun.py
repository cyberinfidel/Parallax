# import python libs
import sys
import gc

import sdl2.mouse

# import Parallax files
# 	add path to Parallax
sys.path.append('../')
# actually import files
import px_game
import px_entity
from px_collision import CollisionManager
from px_vector import Vec3
import px_graphics
import px_sound
import px_utility

import px_log

#import PacBun files
import mode_cont
import PB_map


class eGameModes:
	quit,\
	init,\
	title,\
	start,\
	play,\
	game_over,\
	win,\
	paused,	escape, high_score, new_high_score, numGameModes = range(0,12)

class PacBun(px_game.Game):

	def __init__(self):
		self.game_data = px_utility.getDataFromFile('PB_game.config')['game']

		px_log.log("Setting up window...")
		super(PacBun, self).__init__("PacBun", res_x= self.game_data['res_x'],
																 res_y = self.game_data['res_y'],
																 zoom = self.game_data['zoom'],
																 fullscreen= self.game_data['fullscreen'])
		sdl2.mouse.SDL_ShowCursor(False)
		px_log.log("Window set up.")

		px_log.log("Setting up render layers...")

		self.render_layers = {}
		for rl_name,rl_data in self.game_data['render layers'].items():
			rl = px_graphics.RenderLayer(self.ren)
			self.render_layers[rl_name]=rl
			if 'fonts' in rl_data:
				px_log.log(f"	Getting fonts in Render Layer {rl_name}...")
				for font_name, font_data in rl_data['fonts'].items():
					# todo keep a handle on the fonts returned
					px_log.log(f"		Getting font: {font_name}...")
					rl.addFont(font_data['file'],font_data['size'])
		px_log.log("Render Layers set up.")

		px_log.log("Setting up misc game settings...")
		self.scroll = False
		self.sound_mixer = px_sound.SoundMixer(self)
		self.collision_manager = CollisionManager(game=self)

		px_log.log("Making game scope templates...")
		self.templates = self.makeTemplates(self.game_data['templates'])
		# self.templates.update(self.makeTemplates(overlay_templates_data, self.overlay_renlayer))
		px_log.log("Templates made.")

		px_log.log("Making game scope entities...")
		self.makeEntities(self.game_data['entities'])
		px_log.log("Game scope entities made.")

		px_log.log("Getting scenes...")
		self.scenes_data = (px_utility.getDataFromFile('PB_scenes.config'))
		self.current_scene = 0


		# put all separate images into texture atlasses for (more) efficient rendering
		px_log.log("Making texture atlases...")
		for rl_name, rl_instance in self.render_layers.items():
			if 'texture atlas' in self.game_data['render layers'][rl_name]:
				# make texture atlas
				# todo: do stuff with texture atlas files
				if 'size hint' in self.game_data['render layers'][rl_name]:
					rl_instance.makeAtlas(self.game_data['render layers'][rl_name]['size hint'])
				else:
					rl_instance.makeAtlas()
				rl_instance.dumpAtlasToFiles(f"{rl_name}.png",f"{rl_name}.json")

		# self.renlayer.dumpAtlasToFiles("TA.png", "TA.json")
		px_log.log("### Startup complete ###")
		px_log.flushToFile()

		self.current_mode=-1
		self.nextScene(next_scene=0, mode=self.game_data['init_mode'])

	########################################
	# end init()
	########################################

	def getBunnyData(self):
		return self.game_data['bunnies']

	def getCurrentBunnyData(self, player):
		return self.game_data['bunnies'].index(self.current_bun[player])

	def getNumBunnies(self):
		return 4

	def pause(self):
		self.game_mode=eGameModes.paused

	def updatePlay(self, dt): # kill
		# draw score
		self.renlayer.setColorCast(px_graphics.Color(1, 1, 1, 1))
		if self.current_score!= self.old_score:
			# update score since it's changed
			self.overlay_renlayer.replaceImageFromString(old_image=self.score_image, string="{0:0=4d}".format(self.current_score), font=self.score_font, color=px_graphics.Color(1, 1, 1, 1))
			self.old_score = self.current_score


	##################################################

	def updateTitle(self, dt): # kill
		px_log.log("WARNING: in title game mode.")
	##################################################

	def updateStart(self, dt): # kill

		gc.collect()
		if len(gc.garbage)>0: print(gc.garbage)
		# set up new game and clean up anything from last game
		self.num_monsters = 0
		self.killPlayEntities()
		self.cleanUpDead()
		self.restart_cooldown = 2

		gc.collect()
		gc.disable()
		self.setGameMode(eGameModes.play)
		self.updatePlay(dt)
		####################################################

	def updateGameOver(self, dt): # kill
		self.restart_cooldown-=dt

		# fade to black
		self.title.setState(title.eTitleStates.game_over)
		fade_factor = max(0,min(1,self.restart_cooldown-0.5))
		self.renlayer.setColorCast(px_graphics.Color(fade_factor,
																								 fade_factor,
																								 fade_factor,
																								 fade_factor))
		self.setClearColor(px_graphics.Color((220 / 255) * fade_factor,
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

	def updateEscape(self, dt): # kill
		self.title.setState(title.eTitleStates.escape)
		for bunny in self.bunnies:
			self.collision_manager.doCollisionsWithSingleEntity(bunny)  # collisions between monsters

		####################################################
	def updateNewHighScore(self, dt): # kill


		pass

	####################################################

	def updateWin(self, dt): # kill
		for bunny in self.bunnies:
			bunny.setState(px_entity.eStates.dead)
		self.restart_cooldown-=dt
		self.title.setState(title.eTitleStates.win)
		if self.restart_cooldown<=0:
			self.current_scene+=1
			if self.current_scene>=len(self.scenes_data['modes'][self.current_mode]['scenes']):
				self.setGameMode(eGameModes.game_over)
			else:
				self.setGameMode(eGameModes.start)
			self.cleanUpDead()
		####################################################

	def quit(self): # kill the program
			self.running=False
			return
		####################################################

	def updateInit(self, dt): # kill
		pass
		####################################################

	def updatePaused(self, dt): # kill
		self.renlayer.setColorCast(px_graphics.Color(0.5, 0.5, 0.5, 1))
		self.setClearColor(px_graphics.Color(110 / 255, 91 / 255, 43 / 255))
		self.title.update(dt)
		####################################################

	def updateHighScore(self, dt): # kill
		self.title_cooldown-=dt
		if self.title_cooldown<0:
			self.title_cooldown = self.title_cooldown_time
			self.setGameMode(eGameModes.title)
			# log("switching to title")
		####################################################

	# ends the scene and by default increments the scene counter for the next scene
	# can change between modes e.g. playing and title
	# next scene can be specified by name
	def nextScene(self, next_scene=-1, mode=False): # kill
		gc.enable()
		gc.collect()

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

		self.playing = self.scene_data['playing']

		self.bunnies = []

		if False:#self.playing:
		# initialise creatures todo: make less bespoke (and work)
			for bunny in range(0,self.num_bunnies):
				name = ['blue','pinkie','pacbun','bowie'][bunny]
				self.bunnies.append(
					self.requestNewEntity(
						self.templates[name],
						pos=self.level.getBunnyStarts()[bunny%len(self.level.getBunnyStarts())],
						parent=self,
						name=name))
				game_pad = self.input.getGamePad(bunny)
				self.bunnies[bunny].controller_data.level = self.level
				if game_pad:
					self.bunnies[bunny].setGamePad(game_pad)
		if 'templates' in self.scene_data:
			self.makeTemplates(self.scene_data['templates'])
		if 'entities' in self.scene_data:
			self.makeEntities(self.scene_data['entities'])
		px_log.flushToFile()

		# self.num_bunnies = len(self.level_data['Bunnies'])
		# for bunny, name in enumerate(self.level_data['Bunnies']):
		# 	self.bunnies.append(
		# 		self.requestNewEntity(
		# 			self.templates[name],
		# 			pos=self.level.getBunnyStarts()[bunny % len(self.level.getBunnyStarts())],
		# 			parent=self,
		# 			name=f"Bunny {name}"))

		# if "Map" in self.scene_data:
		# 	self.foxes = []
		# 	for fox_start in self.level.getFoxStarts():
		# 		this_fox = self.requestNewEntity(self.templates['fox'], pos=fox_start.pos, parent=self, name="Fox")
		# 		this_fox.controller_data.bunny = self.bunnies[0]
		# 		this_fox.controller_data.level = self.level
		# 		this_fox.controller_data.type = fox_start.type
		# 		self.foxes.append(this_fox)


		gc.collect()
		gc.disable()
		if len(gc.garbage)>0: px_log.log(gc.garbage)

	###########
	#  update #
	###########
	def update(self, dt):
		# (
		# 	self.updateQuit,
		# 	self.updateInit,
		# 	self.updateTitle,
		# 	self.updateStart,
		# 	self.updatePlay,
		# 	self.updateGameOver,
		# 	self.updateWin,
		# 	self.updatePaused,
		# 	self.updateEscape,
		# 	self.updateHighScore,
		# 	self.updateNewHighScore
		# )[self.game_mode](dt)

		# Always do this, unless paused:
		if self.game_mode!=eGameModes.paused:
			for bunny in self.bunnies:
				self.collision_manager.doCollisionsWithSingleEntity(bunny)  # collisions between monsters
			for updatable in self.updatables:
				updatable.update(dt)
			for audible in self.audibles:
				audible.sounds.play(audible.sounds_data, audible)

			self.cleanUpDead()


# end update() #################################################################

	def cleanUpDead(self):
		self.updatables[:] = [x for x in self.updatables if x.getState() != px_entity.eStates.dead]
		self.collision_manager.cleanUpDead()
		self.drawables[:] = [x for x in self.drawables if x.getState() != px_entity.eStates.dead]
		self.audibles[:] = [x for x in self.audibles if x.getState() != px_entity.eStates.dead]
		self.entity_manager.deleteDead()

	# This kills everything in the entity manager that isn't listed in the whitelist
	# used by nextScene via killEntitiesExceptLists
	def killEntitiesExcept(self, white_list):
		self.updatables.killEntitiesNotInList(white_list)
		self.drawables.killEntitiesNotInList(white_list)
		self.cleanUpDead()

	# takes a list of lists and kills everything except those entities
	def killEntitiesExceptDicts(self, lists):
		white_list = []
		for l in lists:
			white_list.extend(l)
		self.killEntitiesExcept(white_list)

	# todo: move to data
	def requestTarget(self,pos):
		return self.bunny.pos

	# todo: move to data
	def reportScore(self, increment):
		self.current_score+=increment

	# todo: move
	def message(self, text, pos, color=px_graphics.Color(1, 1, 1, 1), duration=0, align=px_graphics.eAlign.left, fade_speed=0.5):
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

	###########
	#  interp #
	###########

	def interp(self, alpha):
		pass

	###########
	#  draw		#
	###########

	# todo: make more generic/configurable
	def draw(self):
		for drawable in self.drawables:
			# draw actual things
			if not drawable.blink:
				drawable.draw()

		self.render_layers['game'].renderSortedByZThenY()

		if self.game_mode==eGameModes.play:
			self.render_layers['overlay'].queueImage(self.score_image, 99, 318, 0)
		self.render_layers['overlay'].render()


# end draw()

	# todo: move to data
	def addNewHighScore(self, initials):
		self.high_score.controller.updateScores(score_data=self.high_score.controller_data.scores_data, initials=initials, new_score=self.current_score)
		self.high_score.graphics.updateScores(self.high_score)
		self.new_high_score.state = px_entity.eStates.dead
		self.setGameMode(eGameModes.title)


def run(tests=False):
	game = PacBun()
	if tests:
		game.runTests()
	game.run()
	px_log.log("Exiting...")
	px_log.flushToFile()
	return 0


if __name__ == "__main__":
	sys.exit(run(tests=True))
