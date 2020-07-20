from entity import eStates
import controller
import collision

class Strike(object):
	def __init__(self, cool, delay, duration, range, dim, orig, force, absorb, damage, template, hero_damage=0):
		self.cool = cool
		self.delay = delay
		self.duration = duration
		self.range = range
		self.dim = dim
		self.orig = orig
		self.force = force
		self.absorb = absorb
		self.damage = damage
		self.template = template
		self.hero_damage = hero_damage


#######
# Hit #
#######
def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(controller.Controller):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

	def __init__(self, game, data):
		super(Controller, self).__init__(game)

	def update(self, data, common_data, dt):

		if not self.coolDown(data, dt):
			# finished big hit - otherwise just hang around
			common_data.state = eStates.dead

	def receiveCollision(self, data, common_data, message=False):
		# Could make it so
		# if a hit hits then it lasts only for the remainder of that tick
		# this avoids hitting the same thing multiple times
		# common_data.state = eStates.dead

		# otherwise the damage would be spread over multiple ticks
		# The more ticks that the hit collides with an object the more damage
		# if you just tickle it, then you don't do much damage
		pass

def makeCollider(manager):
	return manager.makeTemplate({"Template": Collider})
class Collider(collision.Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

	def __init__(self, game, data):
		super(Collider, self).__init__(game)
		# global static data to all of components


