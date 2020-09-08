from px_entity import eStates
import px_controller
import px_graphics
from px_vector import Vec3

def makeGraphics(manager, renlayer):
	return manager.makeTemplate( {
		"Name": "Rain",
		"Template": px_graphics.MultiAnim,
		"RenderLayer": renlayer,
		"Anims": [
			{
				"Name": "Rain Drop Falls",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [Controller.state_fall],
				"Frames":
					[
#						["Graphics/Rain/RainVert1.png", 1, 8, 0, 0.1],
						["Graphics/Rain/RainVert2.png", 1, 8, 0, 0.1],
					]
			},
			{
				"Name": "Rain Drop Pool",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [Controller.state_pool],
				"Frames":
					[
						["Graphics/Rain/RainPool 1.png", 8, 0, 0, 0.1],
						["Graphics/Rain/RainPool 2.png", 8, 0, 0, 0.1],
						["Graphics/Rain/RainPool 1.png", 8, 0, 0, 0.1],
						["Graphics/Rain/RainPool 2.png", 8, 0, 0, 0.1],
						["Graphics/Rain/RainPool 1.png", 8, 0, 0, 0.1],
						["Graphics/Rain/RainPool 2.png", 8, 0, 0, 0.1],
						["Graphics/Rain/RainPool 3.png", 8, 0, 0, 0.1],
						["Graphics/Rain/RainPool 4.png", 8, 0, 0, 0.1],
						["Graphics/Rain/RainPool 5.png", 8, 0, 0, 0.1],

					]
			},
		]
	})

def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(px_controller.Controller):
	# note custom states
	state_fall = 2
	state_pool = 3
	pool_cooldown = 0.7

	# define data necessary for every instance of the class
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				self.game_pad = init.game_pad
			else:
				self.game_pad = False

			self.vel = Vec3(0.0,-3.0,0.0)
			self.cooldown = -1
			common_data.state = Controller.state_fall
			common_data.new_state = False

	def __init__(self, game, data):
		super(Controller, self).__init__(game)

	def update(self, data, common_data, dt):
		# deal with things that can interrupt actions e.g. landing
		if common_data.pos.y <= 0:
			# on the ground
			self.setState(data, common_data, self.state_pool, self.pool_cooldown)
			data.vel = Vec3(0, 0, 0)
		else:
			# falling
			pass

		# deal with things that can't interrupt actions that are already happening
		if not self.coolDown(data, dt):
			if common_data.state == Controller.state_pool:
				self.setState(data, common_data, eStates.dead)

		px_controller.basic_physics(common_data.pos, data.vel)


