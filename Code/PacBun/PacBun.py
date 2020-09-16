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

class eStates(px_entity.eStates):
	runDown,runLeft, runUp, runRight,\
		cleanLeft, cleanRight,\
		caughtPacBun, caughtPinkie, caughtBlue, caughtBowie,\
		=range(px_entity.eStates.numStates+1,px_entity.eStates.numStates+11)

# class eGameModes:
# 	quit,\
# 	init,\
# 	title,\
# 	start,\
# 	play,\
# 	game_over,\
# 	win,\
# 	paused,	escape, high_score, new_high_score, numGameModes = range(0,12)

class PacBun(px_game.Game):

	def __init__(self):
		super(PacBun, self).__init__()
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
		self.flags={}

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
	##################################################

	def getCurrentBunnyData(self, player):
		return self.game_data['bunnies'].index(self.current_bun[player])
	##################################################

	def getNumBunnies(self):
		return 1
	##################################################

	def pause(self):
		self.game_mode=eGameModes.paused
	##################################################

	def reportCaught(self, bunny):
		pass

	##################################################


	def updatePlay(self, dt): # kill
		# draw score
		self.renlayer.setColorCast(px_graphics.Color(1, 1, 1, 1))
		if self.current_score!= self.old_score:
			# update score since it's changed
			self.overlay_renlayer.replaceImageFromString(old_image=self.score_image, string="{0:0=4d}".format(self.current_score), font=self.score_font, color=px_graphics.Color(1, 1, 1, 1))
			self.old_score = self.current_score

	##################################################

	def quit(self): # kill the program
			self.running=False
			return
	####################################################

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

	###########
	#  update #
	###########
	def update(self, dt):

		if True:#self.game_mode!=eGameModes.paused:
			# for bunny in self.bunnies:
				# self.collision_manager.doCollisionsWithSingleEntity(bunny)  # collisions between monsters
			self.collision_manager.doCollisions()  # collisions between monsters
			for updatable in self.updatables:
				updatable.update(dt)
			for audible in self.audibles:
				audible.sounds.play(audible.sounds_data, audible)

			self.cleanUpDead()


# end update() #################################################################

	def cleanUpDead(self):
		self.updatables[:] = [x for x in self.updatables if x.getState() != eStates.dead]
		self.collision_manager.cleanUpDead()
		self.drawables[:] = [x for x in self.drawables if x.getState() != eStates.dead]
		self.audibles[:] = [x for x in self.audibles if x.getState() != eStates.dead]
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

	def registerFlag(self, flag):
		self.flags[flag]=False

	def setFlag(self, flag):
		self.flags[flag] = True

	def checkFlagAndClear(self, flag):
		if self.flags[flag]:
			self.flags[flag]=False
			return True
		return False

	# todo: move
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
		self.render_layers['overlay'].render()


# end draw()

	# todo: move to data
	def addNewHighScore(self, initials):
		self.high_score.controller.updateScores(score_data=self.high_score.controller_data.scores_data, initials=initials, new_score=self.current_score)
		self.high_score.graphics.updateScores(self.high_score)
		self.new_high_score.state = eStates.dead
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
