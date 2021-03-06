# system

# Parallax
from px_collision import Collider, eShapes
from px_graphics import SingleImage
from px_vector import Vec3

# FeedTheDuck


def RockGraphics(renlayer):
	return {
			"Name": "Background",
			"Template": SingleImage,
			"RenderLayer": renlayer,
			"Image": ["Graphics/Background/Rock.png", 24, 24, 0, 0]
		}

class RockCollider(Collider):

	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.orig = Vec3(12,16,4)
			self.dim = Vec3(24,32,12)

	def __init__(self, game, data):
		super(RockCollider, self).__init__(game)
		# global static data to all of this class's components
		self.radius = 15.0
		self.mass = 10.0

	def getRadius(self):
		return self.radius

	def getCollisionShapesList(self):
		# return a list of the shapes that need to be tested against
		# in this case two circles = 2x position from origin and radii
		# these approximate the shape of the rock
		return ((eShapes.sphere,Vec3(16,16,16),16),(eShapes.sphere,Vec3(32,16,16),16))

	def getCollisionMessage(self, data, common_data):
		pass

