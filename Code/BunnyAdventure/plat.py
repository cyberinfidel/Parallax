import graphics
import controller
import collision
from vector import Vec3

def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(controller.Controller):
	def __init__(self, game, data):
		super(Controller, self).__init__(game)

	class Data(object):
		def __init__(self, common_data, init=False):
			self.vel = Vec3(0,0,0.2)

	def update(self, data, common_data, dt):
		return
		if common_data.pos.z>100:
			data.vel.z = -0.2
		elif common_data.pos.z<20:
			data.vel.z = 0.2

		controller.basic_physics(common_data.pos, data.vel)

	def receiveCollision(self, A, B):
		# scenery doesn't react to collisions
		pass



def makeGraphics(graphics_manager, renlayer):
	# return graphics_manager.makeTemplate({
	# 		"Name": "Platform",
	# 		"Template": graphics.SingleImage,
	# 		"RenderLayer": renlayer,
	# 		"Image": ["Graphics/Platform/TestPlatform50x50.png", 25, 35, 0]
	# })

	return graphics_manager.makeTemplate({
			"Name": "Platform",
			"Template": graphics.MultiImage,
			"RenderLayer": renlayer,
			"Images": [
				# ["Graphics/Platform/TestPlatform50x12.png", 25, 39],
				# ["Graphics/Platform/TestPlatform50x12.png", 25, 27],
				# ["Graphics/Platform/TestPlatform50x12.png", 25, 15],
				["Graphics/Platform/TestPlatform50x12.png", 25, 3]
			]
		})


def restrictToArena(pos, vel):
	# stop running through walls at either side
	# if pos on left side of line then force to right side
	# while pos.whichSidePlane(Plane(1, -1, 0, 0)):
	# 	controller.basic_physics(pos, Vec3(0.1, -0.1, 0)) # normal vector to plane

	# stop running through walls at either side
	# if pos on left side of line then force to right side
	# while not pos.whichSidePlane(Plane(1, 1, 0, -1920)):
	# 	controller.basic_physics(pos, Vec3(-0.1, -0.1, 0)) # normal vector to plane

	# stop running off screen bottom, top and sides
	pos.clamp(Vec3(50, 0, 0), Vec3(100, 90, 10))

def makeCollider(manager):
	return manager.makeTemplate({"Template": Collider})
class Collider(collision.Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.dim = Vec3(50,10,30)
			self.orig = Vec3(25,5,20)
			self.impassable = True

	def __init__(self, game, data):
		super(Collider, self).__init__(game)
		# global static data to all of HeroCollider components
		self.mass = 10.0


	def getCollisionMessage(self, data, common_data):
		return(collision.Message(source=common_data.entity,
														 absorb=1000,
														 impassable=True,
														 platform = True))

