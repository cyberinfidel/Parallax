import px_graphics
import px_controller
import px_collision
from px_vector import Vec3

def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(px_controller.Controller):
	def __init__(self, game, data):
		super(Controller, self).__init__(game)

	class Data(object):
		def __init__(self, common_data, init=False):
			self.vel = Vec3(0,0,0)

	def update(self, data, common_data, dt):
		return
		if common_data.pos.y>100:
			data.vel.y = -0.2
		elif common_data.pos.y<20:
			data.vel.y = 0.2

		px_controller.basic_physics(common_data.pos, data.vel)

	def receiveCollision(self, A, message):
		# scenery doesn't react to collisions
		pass



def makeGraphics(manager, renlayer):
	return manager.makeTemplate({
			"Name": "Platform",
			"Template": px_graphics.SingleImage,
			"RenderLayer": renlayer,
			"Image":
				["Graphics/Platform/TestPlatform50x12.png", 25, 3, 0]
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
	pos.clamp(Vec3(50, 0, 0), Vec3(100, 10, 90))

def makeCollider(manager):
	return manager.makeTemplate({"Template": Collider})
class Collider(px_collision.Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.dim = Vec3(50,30,10)
			self.orig = Vec3(25,20,5)

	def __init__(self, game, data):
		super(Collider, self).__init__(game)
		# global static data to all of HeroCollider components
		self.mass = 10.0


	def getCollisionMessage(self, data, common_data):
		return(px_collision.Message(source=common_data.entity,
																impassable=True))

