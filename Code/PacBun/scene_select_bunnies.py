# controller components for scenes of PacBun

# Parallax
import px_controller
import px_game_pad
import px_entity
import px_graphics
from px_vector import Vec3
import px_log

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
			entity.parent = entity.game.getEntityByName(f'bunny choice {0}')
			entity.bun_num= data['bun num']
			bunnies = entity.game.game_data['bunnies']
			entity.message_color = bunnies.index(entity.bun_num).color
			entity.bun_name = data['bun name']
		else:
			px_log.log("*** Warning: Entity {entity.name} with BunnyChooseController component missing data.")

	def update(self, entity, dt):
		# check if currently chosen bunny
		# bunny_choice = entity.game.getEntityByName('bunny choice')
		# if bunny_choice.controller_data.current_bun[0]==0:
		# 	print("Pacbun!")

		if entity.game.current_bun[0]==entity.bun_num:
			if entity.state!=px_entity.eStates.runDown:
				self.setState(entity, px_entity.eStates.runDown)
				entity.message = entity.game.message(text=entity.bun_name,
														pos= entity.pos+Vec3(0,40,0),
														color=entity.message_color,
														duration=-1,
														align=px_graphics.eAlign.centre,
														fade_speed = 0.5)
		else:
			self.setState(entity, px_entity.eStates.stationary)
			if entity.message:
				entity.message.process('fade out',[0.5])
