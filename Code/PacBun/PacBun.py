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
import path


class Level(object):

	def __init__(self, map):
		self.map = map

		# flip since we draw from bottom left
		for i in range(0, 10):
			swap = self.map[i]
			self.map[i] = self.map[19 - i]
			self.map[19 - i] = swap

		self.data = [None]*20
		for i in range(0,20):
			self.data[i] = [None]*20

		self.entities = [None]*20
		for i in range(0,20):
			self.entities[i] = [None]*20

		self.num_spaces=0
		self.num_poos=0
		for y in range(0,20):
			for x in range(0,20):
				if self.map[y][x]!="H":
					self.num_spaces+=1
					self.data[y][x]=[]
					# work out ways out of the blank space
					if self.map[y+1][x]!="H":
						self.data[y][x].append(entity.eDirections.up)
					if self.map[y-1][x]!="H":
						self.data[y][x].append(entity.eDirections.down)
					if self.map[y][x-1]!="H":
						self.data[y][x].append(entity.eDirections.left)
					if self.map[y][x+1]!="H":
						self.data[y][x].append(entity.eDirections.right)



	def getLocFromCoord(self,x,y):
		return self.map[y][x]

	def getCoordFromPos(self, pos):
		return int(pos.x/16),int(pos.y/16)

	def getExitsFromCoord(self, x, y):
		return self.data[y][x]


	def setEntityForCoord(self, entity, x, y):
		if (self.data[y][x]):
			entity.setState(path.ePathStates.clear)
		else:
			entity.setState(path.ePathStates.hedge)
		# entity.collider_data.exits=self.data[y][x]
		self.entities[y][x]=entity

	def poo(self,x,y):
		entity = self.entities[y][x]
		if entity.getState()!=path.ePathStates.poo:
			entity.controller.setState(entity.controller_data, entity.common_data,path.ePathStates.poo)
			self.num_poos+=1
			if self.num_poos>= self.num_spaces:
				return True	# signal win
		return False


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
		self.title_renlayer = graphics.RenderLayer(self.ren)
		self.scroll = False
		self.quit_cooldown = 0.5
		self.restart_cooldown = 2

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


		self.title_t = self.entity_manager.makeEntityTemplate(graphics=title.makeGraphics(self.graphics_manager, self.title_renlayer), controller=title.makeController(self.controller_manager))
		self.title = self.requestNewEntity(entity_template=self.title_t, pos=Vec3(36, 250, 50), parent=self, name="Title")
		self.title.setGamePad(self.input.getGamePad(0))

		self.collision_manager = CollisionManager(game=self)  # TODO: should this be a ComponentManager() like the others?

		self.setGameMode(eGameModes.title)


		###################
		# make components #
		###################


		# info bar
		self.heart_t = self.entity_manager.makeEntityTemplate(graphics=heart.makeGraphics(self.graphics_manager,self.title_renlayer), controller=heart.makeController(self.controller_manager))

		self.bunny_t = self.entity_manager.makeEntityTemplate(graphics=bunny.makeGraphics(self.graphics_manager, self.renlayer), controller = bunny.makeController(self.controller_manager), collider=bunny.makeCollider(self.collision_manager))

		self.path_t = self.entity_manager.makeEntityTemplate(graphics=path.makeGraphics(self.graphics_manager, self.renlayer), controller = path.makeController(self.controller_manager) )

		self.level = Level([
			"HHHHHHHHHHHHHHHHHHHH",
			"H          HHHHHHHHH",
			"H HHHH HHHHHHHHHHHHH",
			"H HHHH HHHHHH HHHHHH",
			"H HHHH HH HHHHH HHHH",
			"H HHHH HH HHHHH HHHH",
			"H                  H",
			"HH H        HHHHH HH",
			"HH HHHHH        H HH",
			"H                  H",
			"H                  H",
			"HH H        HHHHH HH",
			"HH HHHHH        H HH",
			"H         HHHHHHH  H",
			"H  HHHHHHHHHHHHHH  H",
			"HH H        HHHHH HH",
			"HH HHHHH        H HH",
			"H                  H",
			"HHHH HH        HHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
		])

		self.level = Level([
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHH   HHHHHHHHH",
			"HHHHHHHO   OHHHHHHHH",
			"HHHHHHHH   HHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
			"HHHHHHHHHHHHHHHHHHHH",
		])

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

			self.bunny = self.requestNewEntity(self.bunny_t, pos=Vec3(16*10+8,16*10+8,0), parent=self, name="Bunny")

			# make hero 2
			game_pad = self.input.getGamePad(0)
			if game_pad:
				self.bunny.setGamePad(game_pad)
			self.bunny.controller_data.level = self.level

			# initialise map
			for y in range(0,20):
				for x in range(0,20):
					back = self.requestNewEntity(self.path_t,pos=Vec3(8+ x*16,8+y*16,1),parent=self,name=f"back{x},{y}")
					self.level.setEntityForCoord(back,x,y)

			# # set up life indicator in top left
			# for n in range(1, 6):
			# 	heart = self.entity_manager.makeEntity(self.heart_t, "Heart")
			# 	heart.setPos(Vec3(10 * n, 190, 0))
			# 	self.drawables.append(heart)
			# 	self.updatables.append(heart)
			# 	heart.common_data.parent = self.bunny
			# 	heart.common_data.state = eStates.fade
			# 	heart.controller_data.health_num = n

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
				self.setGameMode(eGameModes.title)
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






def run(tests=False):
	game = PacBun()
	if tests:
		game.runTests()
	game.run()
	return 0


if __name__ == "__main__":
	sys.exit(run(tests=True))
