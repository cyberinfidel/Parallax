# controller components for modes of PacBun

# Parallax
import px_controller
import px_game_pad


########################################
# controller for title screens
def makeTitleController(manager):
	return manager.makeTemplate({"Template": TitleController})
class TitleController(px_controller.Controller):
	def __init__(self, game, data):
		super(TitleController, self).__init__(game)

	def update(self, entity, dt):
		if entity.game_pad.getAndClear(px_game_pad.eActions.quit):
			entity.game.nextScene(mode='quit')
		elif entity.game_pad.getAndClear(px_game_pad.eActions.fullscreen):
			entity.game.toggleFullscreen()
		elif entity.game_pad.getAndClear(px_game_pad.eActions.jump):
			entity.game.nextScene(mode='bunny select')

########################################
# controller for quit screens
def makeQuitController(manager):
	return manager.makeTemplate({"Template": QuitController})
class QuitController(px_controller.Controller):
	def __init__(self, game, data):
		super(QuitController, self).__init__(game)

	def update(self, entity, dt):
		if entity.game_pad.getAndClear(px_game_pad.eActions.quit):
			exit(0)	# just end

########################################
# controller for bunny selected
#
# - Stores the selected bunnies for the players in the game object
# todo: consider a less ugly solution for storing persistent data
def makeBunnyChoiceController(manager):
	return manager.makeTemplate({"Template": BunnyChoiceController})
class BunnyChoiceController(px_controller.Controller):
	def __init__(self, game, data):
		super(BunnyChoiceController, self).__init__(game)
		self.bunnies = ['pacbun','pinkie','blue','bowie']
		game.current_bun = [0,1,2,3]

	# called when an entity is created that contains this component
	def initEntity(self, entity, data=False):
		entity.this_bun = data['this bun']

	def update(self, entity, dt):
		if entity.game_pad.getAndClear(px_game_pad.eActions.left):
			entity.game.current_bun[0] = (entity.game.current_bun[0]-1)%4
		elif entity.game_pad.getAndClear(px_game_pad.eActions.right):
			entity.game.current_bun[0] = (entity.game.current_bun[0]+1)%4

		if entity.game_pad.getAndClear(px_game_pad.eActions.quit):
			entity.game.nextScene(mode='title')
		elif entity.game_pad.getAndClear(px_game_pad.eActions.fullscreen):
			entity.game.toggleFullscreen()
		elif entity.game_pad.getAndClear(px_game_pad.eActions.jump):
			entity.game.nextScene(mode='play')

########################################
# controller for play
def makePlayController(manager):
	return manager.makeTemplate({"Template": PlayController})
class PlayController(px_controller.Controller):
	def __init__(self, game, data):
		super(PlayController, self).__init__(game)

	def update(self, entity, dt):
		if entity.game_pad.getAndClear(px_game_pad.eActions.quit):
			print('todo: implement pause') # todo: implement pause instead of quitting
			entity.game.nextScene(mode='title')


