# controller components for scenes of PacBun

# Parallax
import px_controller
import px_game_pad
import px_entity
import px_graphics
from px_vector import Vec3
import px_log

########################################
# controller for select bunnies scene
def makeSelectBunniesController(manager):
	return manager.makeTemplate({"Template": SelectBunniesController})
class SelectBunniesController(px_controller.Controller):
	def __init__(self, game, data):
		super(SelectBunniesController, self).__init__(game)

	def update(self, entity, dt):
		if entity.game_pad.getAndClear(px_game_pad.eActions.quit):
			entity.game.nextScene(mode='title')
		elif entity.game_pad.getAndClear(px_game_pad.eActions.fullscreen):
			entity.game.toggleFullscreen()
		elif entity.game_pad.getAndClear(px_game_pad.eActions.jump):
			entity.game.nextScene()


########################################
# controller for a bunny in the bunny select scene
def makeBunnyChooseController(manager):
	return manager.makeTemplate({"Template": BunnyChooseController})
class BunnyChooseController(px_controller.Controller):
	def __init__(self, game, data):
		super(BunnyChooseController, self).__init__(game)

	def initEntity(self, entity, data=False):
		entity.message = False
		if data:
			entity.pos = data['pos']
			entity.parent = entity.game.getEntityByName('bunny choice')
			entity.bun_num= data['bun num']
			entity.message_color = data['message color']
			entity.bun_name = data['bun name']
		else:
			px_log.log("*** Warning: Entity {entity.name} with BunnyChooseController component missing data.")

	def update(self, entity, dt):
		# check if currently chosen bunny
		# bunny_choice = entity.game.getEntityByName('bunny choice')
		# if bunny_choice.controller_data.current_bun[0]==0:
		# 	print("Pacbun!")

		if entity.parent.current_bun[0]==entity.bun_num:
			if entity.state!=px_entity.eStates.runDown:
				self.setState(entity, px_entity.eStates.runDown)
				entity.message = entity.game.message(text=entity.bun_name,
														pos= entity.pos+Vec3(0,40,0),
														color=entity.message_color,
														duration=100,
														align=px_graphics.eAlign.centre,
														fade_speed = 0.5)
		else:
			self.setState(entity, px_entity.eStates.stationary)
			if entity.message:
				entity.message.process('fade out',[0.5])
