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
			entity.game.nextScene(mode='play')

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
# controller for play mode
#
# - Stores the selected bunnies for the players
def makeSelectBunniesController(manager):
	return manager.makeTemplate({"Template": SelectBunniesController})
class SelectBunniesController(px_controller.Controller):
	def __init__(self, game, data):
		super(SelectBunniesController, self).__init__(game)
		self.bunnies = ['pacbun','pinkie','blue','bowie']

	# called when an entity is created that contains this component
	def initEntity(self, entity, data=False):
			entity.current_bun = [0,0,0,0]

	def update(self, entity, dt):
		if entity.game_pad.getAndClear(px_game_pad.eActions.left):
			entity.current_bun[0] = (entity.current_bun[0]-1)%4
		elif entity.game_pad.getAndClear(px_game_pad.eActions.right):
			entity.current_bun[0] = (entity.current_bun[0]+1)%4


