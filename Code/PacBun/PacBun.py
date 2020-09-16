# import python libs
import sys

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

		# todo: consider moving this into px_game
		px_log.log("Making game scope templates...")
		self.templates = self.makeTemplates(self.game_data['templates'])
		# self.templates.update(self.makeTemplates(overlay_templates_data, self.overlay_renlayer))
		px_log.log("Templates made.")

		px_log.log("Making game scope entities...")
		self.makeEntities(self.game_data['entities'])
		px_log.log("Game scope entities made.")

		px_log.log("Getting scenes...")
		self.getScenesData('PB_scenes.config')

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

	# todo: move

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
