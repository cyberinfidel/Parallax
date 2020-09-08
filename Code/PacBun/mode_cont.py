# controller for title mode of PacBun

# Parallax
import controller
import game_pad

import PacBun

# controller for title screens
def makeTitleController(manager):
	return manager.makeTemplate({"Template": TitleController})
class TitleController(controller.Controller):
	class Data(object):
		def __init__(self, common_data, init=False):
			pass

	def __init__(self, game, data):
		super(TitleController, self).__init__(game)

	def update(self, data, common_data, dt):
		if data.game_pad.getAndClear(game_pad.eActions.quit):
			common_data.game.nextScene(mode='quit')
		elif data.game_pad.getAndClear(game_pad.eActions.fullscreen):
			common_data.game.toggleFullscreen()
		elif data.game_pad.getAndClear(game_pad.eActions.jump):
			common_data.game.nextScene(mode='select bunnies')

# controller for select bunnies screen
def makeSelectBunniesController(manager):
	return manager.makeTemplate({"Template": SelectBunniesController})
class SelectBunniesController(controller.Controller):
	class Data(object):
		def __init__(self, common_data, init=False):
			pass

	def __init__(self, game, data):
		super(SelectBunniesController, self).__init__(game)

	def update(self, data, common_data, dt):
		if data.game_pad.getAndClear(game_pad.eActions.quit):
			common_data.game.nextScene(mode='title')
		elif data.game_pad.getAndClear(game_pad.eActions.fullscreen):
			common_data.game.toggleFullscreen()
		if data.game_pad.getAndClear(game_pad.eActions.jump):
			common_data.game.nextScene(mode='play')




