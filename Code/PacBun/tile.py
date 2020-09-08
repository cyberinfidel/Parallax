# Parallax
import px_controller
import px_collision
from px_vector import Vec3


# exits map to binary values
# tile.eTileStates.tunnel_no_exit,  # 0000
# tile.eTileStates.tunnel_up,  # 0001
# tile.eTileStates.tunnel_down,  # 0010, 2
# tile.eTileStates.tunnel_up_down,  # 0011, 3
# tile.eTileStates.tunnel_left,  # 0100, 4
# tile.eTileStates.tunnel_up_left,  # 0101, 5
# tile.eTileStates.tunnel_down_left,  # 0110, 6
# tile.eTileStates.tunnel_up_down_left,  # 0111, 7
# tile.eTileStates.tunnel_right,  # 1000, 8
# tile.eTileStates.tunnel_up_right,  # 1001, 9
# tile.eTileStates.tunnel_down_right,  # 1010,10
# tile.eTileStates.tunnel_up_down_right,  # 1011,11
# tile.eTileStates.tunnel_left_right,  # 1100,12
# tile.eTileStates.tunnel_up_left_right,  # 1101,13
# tile.eTileStates.tunnel_down_left_right,  # 1110,14
# tile.eTileStates.tunnel_up_down_left_right,  # 1111,15

class eTileStates:
	poo, \
	hedge, \
	path, \
	hole, \
	void, \
	tunnel_no_exit, \
	tunnel_up, \
	tunnel_down, \
	tunnel_up_down, \
	tunnel_left, \
	tunnel_up_left, \
	tunnel_down_left, \
	tunnel_up_down_left, \
	tunnel_right, \
	tunnel_up_right, \
	tunnel_down_right, \
	tunnel_up_down_right, \
	tunnel_left_right, \
	tunnel_up_left_right, \
	tunnel_down_left_right, \
	tunnel_up_down_left_right, \
	cutscene_hole, \
	= range(2,24)




def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(px_controller.Controller):
	def __init__(self, game, data):
		super(Controller, self).__init__(game)
		# values global to all instances

	################
	# end __init__ #
	################

	class Data(object):
		def __init__(self, entity, init=False):
			if init:
				self.game_pad = init.game_pad
			else:
				self.game_pad = False

			# values for each instance
			self.types = []
			self.exits = []


	#####################
	# end data __init__ #
	#####################

	def addExit(self, data, exit):
		data.exits.append(exit)

	def getExits(self, data):
		return data.exits

	def addType(self, data, type):
		data.types.append(type)

	def getTypes(self, data):
		return data.types

	def update(self, data, entity, dt):
		pass



	def receiveCollision(self, A, message):
		# log("Hero hit: "+message["name"])
		if message:
			pass

def makeCollider(manager):
	return manager.makeTemplate({"Template": Collider})
class Collider(px_collision.Collider):
	class Data(object):
		def __init__(self, entity, init=False):
			if init:
				pass
			else:
				pass
			self.dim = Vec3(16,16,1)
			self.orig = Vec3(0,0,0)

	def __init__(self, game, data):
		super(Collider, self).__init__(game)
		# global static data to all of HeroCollider components

	def getCollisionMessage(self, data, entity):
		message = px_collision.Message(source=entity)
		if entity.state==eTileStates.hedge:
			message.impassable = True
			message.poo = False
		else:
			message.impassable = False
		return message



