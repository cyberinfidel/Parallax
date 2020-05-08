from controller import *
from collision import *
from graphics import *

def batGraphics(renlayer):
	return {
			"Name": "Simple Bat Flapping",
			"Template": SingleAnim,
			"RenderLayer": renlayer,
			"Anims": [{
				"Name": "Simple Bat Flapping",
				"AnimType": AnimLoop,
				"Frames":
					[
						["Graphics/Bat/Bat1.png", 24, 30, 0.5],
						["Graphics/Bat/Bat2.png", 24, 30, 0.04],
						["Graphics/Bat/Bat3.png", 24, 30, 0.04],
						["Graphics/Bat/Bat4.png", 24, 30, 0.1],
						["Graphics/Bat/Bat3.png", 24, 30, 0.1],
						["Graphics/Bat/Bat2.png", 24, 30, 0.1],
					],
			}]
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

	def __init__(self, data):
		super(BatController, self).__init__()

	def update(self, data, common_data, dt):
		# if doing something that can't be interrupted then countdown to end of it
		if not self.coolDown(data, dt):
			pass

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

	def getRadius(self):
		return self.radius

	def getCollisionMessage(self, data, common_data):
		pass






