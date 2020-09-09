# system
import enum
import copy

# Parallax
import px_entity
import px_controller
import px_collision
from px_vector import Vec3
import px_vector
import px_sound



def makeSounds(manager, mixer):
	return manager.makeTemplate({
		"Name": "Bunny Sounds",
		"Template": px_sound.MultiSound,
		"Mixer": mixer,
		"StateSounds": [
		],
		"EventSounds":
			[
				{
					"Name": "Jump",
					"Type": px_sound.Single,
					"Events": [px_entity.eEvents.jump],
					"Samples":  # one of these will play at random if there's more than one
						[
							"Sounds/Hero/jump.wav"
						]
				}

			]
	})

class eFoxStates(enum.IntEnum):
	cleanLeft = px_entity.eStates.hurtLeft
	cleanRight = px_entity.eStates.hurtRight
	bunnyCaught = px_entity.eStates.idle

class eFoxTypes(enum.IntEnum):
	direct=1
	ahead=2
	axis_swap=3
	cowardly=4

def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(px_controller.Controller):
	def __init__(self, game, data):
		super(Controller, self).__init__(game)
		# values global to all instances






	################
	# end __init__ #
	################

	def initEntity(self, entity, data=False):
			# values for each instance

			entity.cooldown = -1
			entity.pause = 7
			entity.vel = Vec3(0.0,0.0,0.0)
			entity.queued_vel = Vec3(0.0,0.0,0.0)
			entity.facing = False
			entity.queued_facing = 4
			entity.health = 3
			entity.state = px_entity.eStates.stationary
			entity.queued_state = entity.state
			entity.AI_cooldown = 1 + px_vector.rand_num(15) / 5.
			entity.type = 0
			entity.fox_speed = 1


	#####################
	# end data __init__ #
	#####################




	def update(self, entity, dt):
		if entity.state==eFoxStates.bunnyCaught: return

		# pause foxes every so often
		# todo: foxes shouldn't pause if the bunny is in sight
		entity.AI_cooldown -= dt
		if entity.AI_cooldown<=0:
			entity.AI_cooldown= 10 + px_vector.rand_num(10)
			if entity.fox_speed==1:
				entity.fox_speed=0
				entity.AI_cooldown = entity.pause
				if entity.pause>0: entity.pause -=1
				self.setState(entity,
											[px_entity.eStates.stationary, px_entity.eStates.stationary, px_entity.eStates.stationary, px_entity.eStates.stationary, px_entity.eStates.stationary, eFoxStates.cleanRight, eFoxStates.cleanLeft][px_vector.rand_num(7)]
											)
			else:
				entity.fox_speed=1

		if entity.fox_speed==0:
			return
		fox_speed = entity.fox_speed

		bunny_pos = copy.deepcopy(entity.bunny.getPos())

		if entity.type==eFoxTypes.ahead:
			# aim at a position ahead of the bunny
			bunny_pos+= (
				Vec3(0,-96,0),
				Vec3(-96,0, 0),
				Vec3(0, 96, 0),
				Vec3(96, 0, 0),
			)[entity.bunny.facing]

		x, y = entity.level.getCoordFromPos(entity.pos)
		current_tile = entity.level.getTileFromCoord(x, y)
		exits = current_tile.controller.getExits(current_tile)
		x_in_tile = entity.pos.x % 16
		y_in_tile = entity.pos.y % 16

		# work out preferred direction
		if bunny_pos.x>entity.pos.x:
			pref_dir=px_entity.eDirections.right
		else:
			pref_dir = px_entity.eDirections.left
		if bunny_pos.y > entity.pos.y:
			sec_dir = px_entity.eDirections.up
		else:
			sec_dir = px_entity.eDirections.down

		if (abs(bunny_pos.x-entity.pos.x)<abs(bunny_pos.y-entity.pos.y)):
			# choose most optimal axis
			pref_dir, sec_dir = sec_dir, pref_dir

		if entity.type==eFoxTypes.axis_swap:
			# swap to less optimal axis for this fox
			pref_dir, sec_dir = sec_dir, pref_dir
		elif entity.type==eFoxTypes.cowardly:
			# reverse directions so fox runs away
			pref_dir = (
				px_entity.eDirections.up,
				px_entity.eDirections.right,
				px_entity.eDirections.down,
				px_entity.eDirections.left,
			)[pref_dir]
			sec_dir = (
				px_entity.eDirections.up,
				px_entity.eDirections.right,
				px_entity.eDirections.down,
				px_entity.eDirections.left,
			)[sec_dir]


		# try to go that way
		if ((x_in_tile-8)%16==0) and ((y_in_tile-8)%16==0):
			if pref_dir in exits:
				entity.facing = pref_dir
			elif sec_dir in exits:
				entity.facing = sec_dir
			else:
				entity.facing = exits[0]

			entity.vel = (
				Vec3(0,-fox_speed,0),
				Vec3(-fox_speed,0, 0),
				Vec3(0, fox_speed, 0),
				Vec3(fox_speed,0, 0),
			)[entity.facing]

			self.setState(entity,(
				px_entity.eStates.runDown,
				px_entity.eStates.runLeft,
				px_entity.eStates.runUp,
				px_entity.eStates.runRight
			)[entity.facing])

		px_controller.basic_physics(entity.pos, entity.vel)
		entity.pos.clamp(Vec3(0,0,0),Vec3(319,319,0))


	def receiveCollision(self, A, message):
		if message:
			if message.damage_hero>0:
				# caught the bunny
				self.setState(A,eFoxStates.bunnyCaught)
				# print(f"col source{message.source.entity.pos.x},{message.source.entity.pos.y}")
		# 	print(f"Hedge source{message.source.entity.pos.x}{message.source.entity.pos.y}")
			# 	# A.controller_data.vel = Vec3(0,0,0)

def makeCollider(manager):
	return manager.makeTemplate({"Template": Collider})
class Collider(px_collision.Collider):
	def __init__(self, game, data):
		super(Collider, self).__init__(game)

	def initEntity(self, entity, data=False):
			entity.dim = Vec3(4,4,8)
			entity.orig = Vec3(2,2,4)
			entity.mass = 10.0
			entity.force = 0.0

	def getCollisionMessage(self, entity):
		return(px_collision.Message(source=entity, damage=1))


