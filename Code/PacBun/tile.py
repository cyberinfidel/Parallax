# system
import enum

# Parallax
import entity
import game_pad
import controller
import collision
import graphics
from vector import Vec3
import sound
import background



class eTileStates(enum.IntEnum):
	poo = 3
	hedge = 4
	clear = 6
	hole = 5


def makeGraphics(manager, renlayer):
	return manager.makeTemplate({
		"Name": "Path Graphics",
		"Template": graphics.MultiAnim,
		"RenderLayer": renlayer,
		"Anims": [
			{
				"Name": "Path without Poo",
				"AnimType": graphics.AnimSingle,
				"States": [eTileStates.clear],
				"Frames":
						[["Graphics/Path/Path.png", 8, 8, 0, 0.8]],
			},
			{
				"Name": "Path with Poo",
				"AnimType": graphics.AnimSingle,
				"States": [eTileStates.poo],
				"Frames":
						[["Graphics/Path/Path Poo.png", 8, 8, 0, 0.8]],
			},
			{
				"Name": "Path with Hole",
				"AnimType": graphics.AnimSingle,
				"States": [eTileStates.hole],
				"Frames":
						[["Graphics/Path/Path Hole.png", 8, 8, 0, 0.8]],
			},
			{
				"Name": "Hedge",
				"AnimType": graphics.AnimSingle,
				"States": [eTileStates.hedge],
				"Frames":
					[["Graphics/Hedge/Hedge.png", 10, 12, -1, 0.8]],
			},

		]

	})


def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(controller.Controller):
	def __init__(self, game, data):
		super(Controller, self).__init__(game)
		# values global to all instances

	################
	# end __init__ #
	################

	class Data(object):
		def __init__(self, common_data, init=False):
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

	def update(self, data, common_data, dt):
		pass



	def receiveCollision(self, A, message):
		# log("Hero hit: "+message["name"])
		if message:
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
			self.dim = Vec3(16,16,1)
			self.orig = Vec3(0,0,0)

	def __init__(self, game, data):
		super(Collider, self).__init__(game)
		# global static data to all of HeroCollider components

	def getCollisionMessage(self, data, common_data):
		message = collision.Message(source=common_data.entity)
		if common_data.state==eTileStates.hedge:
			message.impassable = True
			message.poo = False
		else:
			message.impassable = False
		return message



