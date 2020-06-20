from entity import eStates
from controller import Controller
from collision import Collider, Message
from vector import Vec3

class Strike(object):
	def __init__(self, cool, delay, range, force, damage, template, hero_damage=0):
		self.cool = cool
		self.delay = delay
		self.range = range
		self.force = force
		self.damage = damage
		self.template = template
		self.hero_damage = hero_damage


#######
# Hit #
#######

class HitController(Controller):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

			self.cooldown = 0.5

	def __init__(self, game, data):
		super(HitController, self).__init__(game)

	def update(self, data, common_data, dt):

		if not self.coolDown(data, dt):
			# finished big hit - otherwise just hang around
			common_data.state = eStates.dead

	def receiveCollision(self, data, common_data, message=False):
		# Could make it so
		# if a hit hits then it lasts only for the remainder of that tick
		# this avoids hitting the same thing multiple times
		# common_data.state = eStates.dead

		# otherwise the damage would need to be spread over multiple ticks
		# The more ticks that the hit collides with an object the more damage
		# if you just tickle it, then you don't do much damage
		pass

class HitCollider(Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

	def __init__(self, game, data):
		super(HitCollider, self).__init__(game)
		# global static data to all of components
		self.dim = Vec3(20,8,16)
		self.orig = Vec3(10,4,0)

	def getCollisionMessage(self, data, common_data):
		return(Message(source=common_data.entity, damage=data.damage, force=data.force))

