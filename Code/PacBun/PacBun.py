# import python libs
import sys
import gc

import sdl2.mouse

# import Parallax files
# 	add path to Parallax
sys.path.append('../')
# actually import files
import game
import entity
from collision import CollisionManager
from vector import Vec3
import graphics
import sound
import utility

import log

#import PacBun files
import mode_cont
import map


class eGameModes:
	quit,\
	init,\
	title,\
	start,\
	play,\
	game_over,\
	win,\
	paused,	escape, high_score, new_high_score, numGameModes = range(0,12)

class PacBun(game.Game):

	def __init__(self):
		self.game_data = utility.getDataFromFile('PB_game.config')

		log.log("Setting up window...")
		super(PacBun, self).__init__("PacBun", res_x= self.game_data['game']['res_x'],
																 res_y = self.game_data['game']['res_y'],
																 zoom = self.game_data['game']['zoom'],
																 fullscreen= self.game_data['game']['fullscreen'])
		sdl2.mouse.SDL_ShowCursor(False)
		log.log("Window set up.")

		log.log("Setting up render layers...")

		self.render_layers = {}
		for rl_name,rl_data in self.game_data['game']['render layers'].items():
			rl = graphics.RenderLayer(self.ren)
			self.render_layers[rl_name]=rl
			if 'fonts' in rl_data:
				log.log(f"	Getting fonts in Render Layer {rl_name}...")
				for font_name, font_data in rl_data['fonts'].items():
					# todo keep a handle on the fonts returned
					log.log(f"		Getting font: {font_name}...")
					rl.addFont(font_data['file'],font_data['size'])
		log.log("Render Layers set up.")

		self.scroll = False

		# todo: move these
		self.quit_cooldown = 0.5
		self.title_cooldown_time = 3
		self.title_cooldown = self.title_cooldown_time

		##########################
		# set up sound           #
		##########################
		self.sound_mixer = sound.SoundMixer(self)

		log.log("Making game scope templates...")
		self.templates = self.makeTemplates(self.game_data['game']['templates'])
		# self.templates.update(self.makeTemplates(overlay_templates_data, self.overlay_renlayer))
		log.log("Templates made.")

		log.log("Making game scope entities...")
		self.makeEntities(self.game_data['game']['entities'])
		log.log("Persistent entites made.")

		log.log("Getting scenes...")
		self.scenes_data = (utility.getDataFromFile('PB_scenes.config'))
		self.current_scene = 0

		self.collision_manager = CollisionManager(game=self)

		# put all separate images into texture atlasses for (more) efficient rendering
		log.log("Making texture atlases...")
		for rl_name, rl_instance in self.render_layers.items():
			if 'texture atlas' in self.game_data['game']['render layers'][rl_name]:
				# make texture atlas
				# todo: do stuff with texture atlas files
				if 'size hint' in self.game_data['game']['render layers'][rl_name]:
					rl_instance.makeAtlas(self.game_data['game']['render layers'][rl_name]['size hint'])
				else:
					rl_instance.makeAtlas()
				rl_instance.dumpAtlasToFiles(f"{rl_name}.png",f"{rl_name}.json")

		# self.renlayer.dumpAtlasToFiles("TA.png", "TA.json")
		log.log("### Startup complete ###")
		log.flushToFile()

		self.current_mode=-1
		self.nextScene(next_scene=0, mode=self.game_data['game']['init_mode'])

	# end init()

	def makeTemplates(self, templates_data):
		templates = {}	# to hold the actual handles from the entity manager
		for name, template in templates_data.items():
			templates[name] = self.entity_manager.makeEntityTemplate(name,
				controller=template['controller'](self.controller_manager) if 'controller' in template else None,
				collider=template['collider'](self.controller_manager) if 'collider' in template else None,
				graphics=self.graphics_manager.makeTemplate(template['graphics']['component'],
																										{'RenderLayer': self.render_layers[template['graphics']['render layer']]}) if 'graphics' in template else None
			)
		return templates


	def makeEntities(self, entities_data):
		for name, entity in entities_data.items():
			init = False
			if 'init' in entity:
				init = entity['init']	# custom initialisation code, not always needed
			self.requestNewEntity(template=entity['template'],
														name=name,
														parent=self,
														init=init)


	def updatePlay(self, dt): # kill
		# draw score
		self.renlayer.setColorCast(graphics.Color(1, 1, 1, 1))
		if self.current_score!= self.old_score:
			# update score since it's changed
			self.overlay_renlayer.replaceImageFromString(old_image=self.score_image, string="{0:0=4d}".format(self.current_score), font=self.score_font, color=graphics.Color(1, 1, 1, 1))
			self.old_score = self.current_score


	##################################################

	def updateTitle(self, dt): # kill
		log.log("WARNING: in title game mode.")
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
			bunny.setState(entity.eStates.dead)
		self.restart_cooldown-=dt
		self.title.setState(title.eTitleStates.win)
		if self.restart_cooldown<=0:
			self.current_scene+=1
			if self.current_scene>=len(self.scenes_data['modes'][self.current_mode]['scene list']):
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
		self.renlayer.setColorCast(graphics.Color(0.5, 0.5, 0.5, 1))
		self.setClearColor(graphics.Color(110 / 255, 91 / 255, 43 / 255))
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
				log.log(f"Switching to mode: {mode}")
				self.current_mode=mode
				self.mode_data = self.game_data['game']['modes'][self.current_mode] # convenience
				# kill old mode
				self.killEntitiesExceptDicts(
					[
						self.game_data['game']['entities'],
					]
				)

				# set up next mode
				log.log(f"Making {mode} mode templates.")
				if 'templates' in self.mode_data:
					self.makeTemplates(self.mode_data['templates'])
				log.log(f"Making {mode} mode entities.")
				if 'entities' in self.mode_data:
					self.makeEntities(self.mode_data['entities'])
				if next_scene<0:	# no scene specified so revert to 0
					next_scene = 0
				log.flushToFile()



		if next_scene>=0:
			# specified scene rather than following pre-defined order
			self.current_scene = next_scene
			specified = "specified "
		else:
			self.current_scene+=1
			if self.current_scene>=len(self.game_data['game']['modes'][self.current_mode]['scene list']):
				# todo add check for completing the game instead of just looping?
				self.current_scene=0
			specified = ""
		next_scene = self.game_data['game']['modes'][self.current_mode]['scene list'][self.current_scene]
		log.log(
			f"Switching to {specified}scene [{self.current_mode},{self.current_scene}]: {self.game_data['game']['modes'][self.current_mode]['scene list'][self.current_scene]}")

		# kill old scene
		self.killEntitiesExceptDicts(
			[
				self.game_data['game']['entities'],
			 	self.mode_data['entities'] if 'entities' in self.mode_data else {}
			]
		)

		###################
		# init next scene #
		###################
		self.scene_data = self.scenes_data['scenes'][self.mode_data['scene list'][self.current_scene]]
		# initialise map todo: make another entity instead of special
		if "Map" in self.scene_data:
			self.level = map.Map(self, self.scene_data, self.templates['tile'])

		self.playing = self.scene_data['playing']

		self.bunnies = []

		if self.playing:
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
		log.flushToFile()

		# self.num_bunnies = len(self.level_data['Bunnies'])
		# for bunny, name in enumerate(self.level_data['Bunnies']):
		# 	self.bunnies.append(
		# 		self.requestNewEntity(
		# 			self.templates[name],
		# 			pos=self.level.getBunnyStarts()[bunny % len(self.level.getBunnyStarts())],
		# 			parent=self,
		# 			name=f"Bunny {name}"))

		if "Map" in self.scene_data:
			self.foxes = []
			for fox_start in self.level.getFoxStarts():
				this_fox = self.requestNewEntity(self.templates['fox'], pos=fox_start.pos, parent=self, name="Fox")
				this_fox.controller_data.bunny = self.bunnies[0]
				this_fox.controller_data.level = self.level
				this_fox.controller_data.type = fox_start.type
				self.foxes.append(this_fox)


		gc.collect()
		gc.disable()
		if len(gc.garbage)>0: log.log(gc.garbage)

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
				audible.sounds.play(audible.sounds_data, audible.common_data)

			self.cleanUpDead()


# end update() #################################################################

	def cleanUpDead(self):
		self.updatables[:] = [x for x in self.updatables if x.getState() != entity.eStates.dead]
		self.collision_manager.cleanUpDead()
		self.drawables[:] = [x for x in self.drawables if x.getState() != entity.eStates.dead]
		self.audibles[:] = [x for x in self.audibles if x.getState() != entity.eStates.dead]
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
		return self.bunny.common_data.pos

	# todo: move to data
	def reportScore(self, increment):
		self.current_score+=increment

	# todo: move
	def message(self, text, pos, color=graphics.Color(1, 1, 1, 1), duration=0, align=graphics.eAlign.left):
		message = self.requestNewEntity(template='message',
													name= f"message: {text}",
													pos=pos,
													parent=self,
		)
		# todo: use the init parameter of requestNewEntity rather than two step init
		message.graphics.init(data = message.graphics_data,
													ren_layer = self.render_layers['overlay'],
													message=text,
													font=0,
													color = color,
													duration=duration,
													align=align
													)

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
			if not drawable.common_data.blink:
				drawable.graphics.draw(drawable.graphics_data, drawable.common_data)

		self.render_layers['game'].renderSortedByZThenY()

		if self.game_mode==eGameModes.play:
			self.render_layers['overlay'].queueImage(self.score_image, 99, 318, 0)
		self.render_layers['overlay'].render()


# end draw()

	# todo: move to data
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
	log.log("Exiting...")
	log.flushToFile()
	return 0


if __name__ == "__main__":
	sys.exit(run(tests=True))
