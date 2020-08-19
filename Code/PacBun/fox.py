# system
import enum
import copy

# Parallax
import entity
import game_pad
import controller
import collision
import graphics
from vector import Vec3
import vector
import sound
import game
import tile



def makeSounds(manager, mixer):
	return manager.makeTemplate({
		"Name": "Bunny Sounds",
		"Template": sound.MultiSound,
		"Mixer": mixer,
		"StateSounds": [
		],
		"EventSounds":
			[
				{
					"Name": "Jump",
					"Type": sound.Single,
					"Events": [entity.eEvents.jump],
					"Samples":  # one of these will play at random if there's more than one
						[
							"Sounds/Hero/jump.wav"
						]
				}

			]
	})

class eFoxStates(enum.IntEnum):
	cleanLeft = entity.eStates.hurtLeft
	cleanRight = entity.eStates.hurtRight
	bunnyCaught = entity.eStates.idle

class eFoxTypes(enum.IntEnum):
	direct=1
	ahead=2
	axis_swap=3
	cowardly=4

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

			self.cooldown = -1
			self.pause = 7
			self.vel = Vec3(0.0,0.0,0.0)
			self.queued_vel = Vec3(0.0,0.0,0.0)
			self.facing = False
			self.queued_facing = 4
			self.health = 3
			common_data.state = entity.eStates.stationary
			self.queued_state = common_data.state
			self.AI_cooldown = 1+vector.rand_num(15)/5.
			self.type = 0
			self.fox_speed = 1


	#####################
	# end data __init__ #
	#####################




	def update(self, data, common_data, dt):
		if common_data.state==eFoxStates.bunnyCaught: return

		# pause foxes every so often
		# todo: foxes shouldn't pause if the bunny is in sight
		data.AI_cooldown -= dt
		if data.AI_cooldown<=0:
			data.AI_cooldown=10+vector.rand_num(10)
			if data.fox_speed==1:
				data.fox_speed=0
				data.AI_cooldown = data.pause
				if data.pause>0: data.pause -=1
				self.setState(data, common_data,
											[entity.eStates.stationary,entity.eStates.stationary,entity.eStates.stationary,entity.eStates.stationary,entity.eStates.stationary,eFoxStates.cleanRight,eFoxStates.cleanLeft][vector.rand_num(7)]
											)
			else:
				data.fox_speed=1

		if data.fox_speed==0:
			return
		fox_speed = data.fox_speed

		bunny_pos = copy.deepcopy(data.bunny.getPos())
		bunny_coords = Vec3(int(bunny_pos.x/16),int(bunny_pos.y/16),0)

		if data.type==eFoxTypes.ahead:
			# aim at a position ahead of the bunny
			bunny_pos+= (
				Vec3(0,-96,0),
				Vec3(-96,0, 0),
				Vec3(0, 96, 0),
				Vec3(96, 0, 0),
			)[data.bunny.controller_data.facing]

		x, y = data.level.getCoordFromPos(common_data.pos)
		current_tile = data.level.getTileFromCoord(x, y)
		exits = current_tile.controller.getExits(current_tile.controller_data)
		x_in_tile = common_data.pos.x % 16
		y_in_tile = common_data.pos.y % 16

		# work out preferred direction
		if bunny_pos.x>common_data.pos.x:
			pref_dir=entity.eDirections.right
		else:
			pref_dir = entity.eDirections.left
		if bunny_pos.y > common_data.pos.y:
			sec_dir = entity.eDirections.up
		else:
			sec_dir = entity.eDirections.down

		if (abs(bunny_pos.x-common_data.pos.x)<abs(bunny_pos.y-common_data.pos.y)):
			# choose most optimal axis
			pref_dir, sec_dir = sec_dir, pref_dir

		if data.type==eFoxTypes.axis_swap:
			# swap to less optimal axis for this fox
			pref_dir, sec_dir = sec_dir, pref_dir
		elif data.type==eFoxTypes.cowardly:
			# reverse directions so fox runs away
			pref_dir = (
				entity.eDirections.up,
				entity.eDirections.right,
				entity.eDirections.down,
				entity.eDirections.left,
			)[pref_dir]
			sec_dir = (
				entity.eDirections.up,
				entity.eDirections.right,
				entity.eDirections.down,
				entity.eDirections.left,
			)[sec_dir]


		# try to go that way
		if ((x_in_tile-8)%16==0) and ((y_in_tile-8)%16==0):
			if pref_dir in exits:
				data.facing = pref_dir
			elif sec_dir in exits:
				data.facing = sec_dir
			else:
				data.facing = exits[0]

			data.vel = (
				Vec3(0,-fox_speed,0),
				Vec3(-fox_speed,0, 0),
				Vec3(0, fox_speed, 0),
				Vec3(fox_speed,0, 0),
			)[data.facing]

			self.setState(data, common_data,(
				entity.eStates.runDown,
				entity.eStates.runLeft,
				entity.eStates.runUp,
				entity.eStates.runRight
			)[data.facing])

		controller.basic_physics(common_data.pos, data.vel)
		common_data.pos.clamp(Vec3(0,0,0),Vec3(319,319,0))


	def receiveCollision(self, A, message):
		if message:
			if message.damage_hero>0:
				# caught the bunny
				self.setState(A.controller_data,A.common_data,eFoxStates.bunnyCaught)
				# print(f"col source{message.source.common_data.pos.x},{message.source.common_data.pos.y}")
		# 	print(f"Hedge source{message.source.common_data.pos.x}{message.source.common_data.pos.y}")
			# 	# A.controller_data.vel = Vec3(0,0,0)

def makeCollider(manager):
	return manager.makeTemplate({"Template": Collider})
class Collider(collision.Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.dim = Vec3(4,4,8)
			self.orig = Vec3(2,2,4)
			self.mass = 10.0
			self.force = 0.0

	def __init__(self, game, data):
		super(Collider, self).__init__(game)
		# global static data to all of HeroCollider components

	def getRadius(self):
		return self.radius

	def getCollisionMessage(self, data, common_data):
		return(collision.Message(source=common_data.entity,damage=1))


