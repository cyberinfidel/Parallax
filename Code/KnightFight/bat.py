from controller import *
from collision import *
from graphics import *

def batGraphics(renlayer):
	return {
			"Name": "Simple Bat Flapping",
			"Template": MultiAnim,
			"RenderLayer": renlayer,
			"Anims": [{
				"Name": "Simple Bat Flapping",
				"AnimType": AnimLoop,
				"State": eStates.stationary,
				"Frames":
					[
						["Graphics/Bat/Bat1.png", 24, 30, 0.5],
						["Graphics/Bat/Bat2.png", 24, 30, 0.04],
						["Graphics/Bat/Bat3.png", 24, 30, 0.04],
						["Graphics/Bat/Bat4.png", 24, 30, 0.1],
						["Graphics/Bat/Bat3.png", 24, 30, 0.1],
						["Graphics/Bat/Bat2.png", 24, 30, 0.1],
					],
			},
			{
				"Name": "Bat Shadow",
				"AnimType": AnimSingle,
				"State": eStates.shadow,
				"Frames":
					[
						["Graphics/shadow.png", 16, 4, 0.3],
					],
			},
			]
		}

class BatController(Controller):

	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.cooldown = 0
			self.health = 50
			self.vel = Vec3(0,0,0)

	def __init__(self, data):
		super(BatController, self).__init__()

	def update(self, data, common_data, dt):
		# if doing something that can't be interrupted then countdown to end of it
		if not self.coolDown(data, dt):
			pass

		basic_physics(common_data.pos,data.vel)

		restrictToArena(common_data.pos, data.vel)

		friction(data.vel)


	def receiveCollision(self, data, common_data, collision_message):
		pass

class BatCollider(Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

	def __init__(self, data):
		super(BatCollider, self).__init__()
		# global static data to all of BatCollider components
		self.radius = 10.0
		self.damage = 1.0
		self.dim = Vec3(20,8,16)
		self.orig = Vec3(10,4,0)

	def getRadius(self):
		return self.radius

	def getCollisionMessage(self, data, common_data):
		return(Message(source=common_data.entity, damage=0, damage_hero=1))






