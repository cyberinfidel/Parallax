# controller components for scenes of PacBun

# Parallax
import controller
import game_pad
import px_entity
import graphics
from vector import Vec3

########################################
# controller for select bunnies scene
def makeSelectBunniesController(manager):
	return manager.makeTemplate({"Template": SelectBunniesController})
class SelectBunniesController(controller.Controller):
	class Data(object):
		def __init__(self, entity, init=False):
			pass

	def __init__(self, game, data):
		super(SelectBunniesController, self).__init__(game)

	def update(self, data, entity, dt):
		if data.game_pad.getAndClear(game_pad.eActions.quit):
			entity.game.nextScene(mode='title')
		elif data.game_pad.getAndClear(game_pad.eActions.fullscreen):
			entity.game.toggleFullscreen()
		elif data.game_pad.getAndClear(game_pad.eActions.jump):
			entity.game.nextScene()


########################################
# controller for a bunny in the bunny select scene
def makeBunnyChooseController(manager):
	return manager.makeTemplate({"Template": BunnyChooseController})
class BunnyChooseController(controller.Controller):
	class Data(object):
		def __init__(self, entity, data):
			self.data = data

	def __init__(self, game, data):
		super(BunnyChooseController, self).__init__(game)

	def update(self, data, entity, dt):
		# check if currently chosen bunny
		# bunny_choice = entity.game.getEntityByName('bunny choice')
		# if bunny_choice.controller_data.current_bun[0]==0:
		# 	print("Pacbun!")

		if entity.parent.controller_data.current_bun[0]==data.bun:
			if entity.state!=px_entity.eStates.runDown:
				self.setState(data, entity, px_entity.eStates.runDown)
				entity.game.message(text=data.bun_name,
															 pos= entity.pos+Vec3(0,40,0),
															 color=data.bun_color,
															 duration=2,
															 align=graphics.eAlign.centre,
																 fade_speed = 0.3)
			# print(f"Color:{data.bun_color}")
		else:
			self.setState(data, entity, px_entity.eStates.stationary)
