# controller components for modes of PacBun

# Parallax
import px_controller
import px_game_pad


########################################
# controller for title screens
def makeTitleController(manager):
	return manager.makeTemplate({"Template": TitleController})
class TitleController(px_controller.Controller):
	class Data(object):
		def __init__(self, entity, init=False):
			pass

	def __init__(self, game, data):
		super(TitleController, self).__init__(game)

	def update(self, data, entity, dt):
		if data.game_pad.getAndClear(px_game_pad.eActions.quit):
			entity.game.nextScene(mode='quit')
		elif data.game_pad.getAndClear(px_game_pad.eActions.fullscreen):
			entity.game.toggleFullscreen()
		elif data.game_pad.getAndClear(px_game_pad.eActions.jump):
			entity.game.nextScene(mode='play')

########################################
# controller for quit screens
def makeQuitController(manager):
	return manager.makeTemplate({"Template": QuitController})
class QuitController(px_controller.Controller):
	class Data(object):
		def __init__(self, entity, init=False):
			pass

	def __init__(self, game, data):
		super(QuitController, self).__init__(game)

	def update(self, data, entity, dt):
		if data.game_pad.getAndClear(px_game_pad.eActions.quit):
			exit(0)	# just end

########################################
# controller for play mode
#
# - Stores the selected bunnies for the players
def makeSelectBunniesController(manager):
	return manager.makeTemplate({"Template": SelectBunniesController})
class SelectBunniesController(px_controller.Controller):
	class Data(object):
		def __init__(self, entity, init=False):
			self.current_bun = [0,0,0,0]

	def __init__(self, game, data):
		super(SelectBunniesController, self).__init__(game)
		self.bunnies = ['pacbun','pinkie','blue','bowie']

	def update(self, data, entity, dt):
		if data.game_pad.getAndClear(px_game_pad.eActions.left):
			data.current_bun[0] = (data.current_bun[0]-1)%4
		elif data.game_pad.getAndClear(px_game_pad.eActions.right):
			data.current_bun[0] = (data.current_bun[0]+1)%4


