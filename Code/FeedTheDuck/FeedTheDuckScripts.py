from controller import *
from collision import *
from graphics import *
from entity import eActions


class DuckStates(enum.IntEnum):
	stationary = 1
	swimLeft = 2
	swimRight = 3
	feedLeft = 4
	feedRight = 5

def DuckGraphics(renlayer):
	return{
			"Name": "Duck Animations",
		"Template": MultiAnim,
		"RenderLayer": renlayer,
		"Anims": [
			{
				"Name": "Duck Stationary",
				"AnimType": AnimLoop,
				"State": DuckStates.stationary,
				"Frames":
					[
						["Graphics/Duck/DuckL1.png", 13, 15, 2.0],
					]
			},
			{
				"Name": "Duck Swims Left",
				"AnimType": AnimLoop,
				"State": DuckStates.swimLeft,
				"Frames":
					[
						["Graphics/Duck/DuckL1.png", 13, 15, 2.0],
					]
			},
			{
				"Name": "Duck Swims Right",
				"AnimType": AnimLoop,
					"State": DuckStates.swimRight,
					"Frames":
						[
							["Graphics/Duck/DuckR1.png", 13, 15, 2.0],
						]
				},
				{
					"Name": "Duck Feeds Left",
					"AnimType": AnimNoLoop,
					"State": DuckStates.feedLeft,
					"Frames":
						[
							["Graphics/Duck/DuckL1.png", 13, 15, 0.1],
							["Graphics/Duck/DuckL2.png", 13, 15, 0.5],
						],
				},
				{
					"Name": "Duck Feeds Right",
					"AnimType": AnimNoLoop,
					"State": DuckStates.feedRight,
					"Frames":
						[
							["Graphics/Duck/DuckR1.png", 13, 15, 0.1],
							["Graphics/Duck/DuckR2.png", 13, 15, 0.5],
						],
				},
			]

		}


class DuckController(Controller):
	speed = 1.0

	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				self.game_pad = init.game_pad
			else:
				self.game_pad = False

			self.vel = Vec3(0.0,0.0,0.0)
			self.feed = False
			self.cooldown = 0
			self.faceleft = False

			common_data.state = DuckStates.stationary


	def __init__(self, init_data=False):
		super(Controller, self).__init__()
		if init_data:
			self.data = init_data


	def update(self, data, common_data, dt):
		if data.game_pad.actions[eActions.left]:
			self.updateState(data, common_data, DuckStates.swimLeft)
			data.faceleft = True
			data.vel.x = -DuckController.speed

		elif data.game_pad.actions[eActions.right]:
			self.updateState(data, common_data, DuckStates.swimRight)
			data.faceleft = False
			data.vel.x = DuckController.speed

		if data.game_pad.actions[eActions.up]:
			data.vel.y = DuckController.speed

		elif data.game_pad.actions[eActions.down]:
			data.vel.y = -DuckController.speed

		basic_physics(common_data.pos, data.vel)
		friction(data.vel)

	def receiveCollision(self,data, common_data, collision_message):
		common_data.pos.x -= data.vel.x *1.1
		common_data.pos.y -= data.vel.y *1.1
		common_data.pos.z -= data.vel.z *1.1
		data.vel = Vec3(0,0,0)

class DuckCollider(Collider):

	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

	def __init__(self, data):
		super(DuckCollider, self).__init__()
		# global static data to all of HeroCollider components
		self.radius = 10.0
		self.mass = 10.0
		self.dim = Vec3(20,12,12)
		self.orig = Vec3(10,6,6)

	def getRadius(self):
		return self.radius

	def getCollisionMessage(self, data, common_data):
		pass
