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

def makeGraphics(manager, renlayer):
	return manager.makeTemplate({
		"Name": "Fox Animations",
		"Template": graphics.MultiAnim,
		"RenderLayer": renlayer,
		"Anims": [
			{
				"Name": "Fox Stands",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.stationary],
				"Frames":
					[
						["Graphics/Fox/Fox.png", 9, 12, 0, 0.8],
					]
			},
			{
				"Name": "Bunny Runs Down",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runDown],
				"Frames":
					[
						["Graphics/Bunny/RunDown 2.png", 8, 11, 0, 0.1],
						["Graphics/Bunny/RunDown 3.png", 8, 11, 0, 0.1],
						["Graphics/Bunny/RunDown 4.png", 8, 11, 0, 0.1],
						["Graphics/Bunny/RunDown 1.png", 8, 11, 0, 0.15],
					],
			},
			{
				"Name": "Bunny Runs Up",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runUp],
				"Frames":
					[
						["Graphics/Bunny/RunUp 2.png", 8, 11, 0, 0.1],
						["Graphics/Bunny/RunUp 3.png", 8, 11, 0, 0.1],
						["Graphics/Bunny/RunUp 4.png", 8, 11, 0, 0.1],
						["Graphics/Bunny/RunUp 1.png", 8, 11, 0, 0.15],
					],
			},
			{
				"Name": "Bunny Runs Left",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runLeft],
				"Frames":
					[
						["Graphics/Bunny/Run 1.png", 8, 11, 0, 0.1],
						["Graphics/Bunny/Run 2.png", 8, 11, 0, 0.1],
						["Graphics/Bunny/Run 3.png", 8, 11, 0, 0.1],
						["Graphics/Bunny/Run 4.png", 8, 11, 0, 0.15],
					],
			},
			{
				"Name": "Bunny Runs Right",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runRight],
				"Frames":
					[
						["Graphics/Bunny/Right/Run 1.png", 8, 11, 0, 0.1],
						["Graphics/Bunny/Right/Run 2.png", 8, 11, 0, 0.1],
						["Graphics/Bunny/Right/Run 3.png", 8, 11, 0, 0.1],
						["Graphics/Bunny/Right/Run 4.png", 8, 11, 0, 0.15],
					],
			},

		]

	})


class eFoxTypes(enum.IntEnum):
	direct=1
	ahead=3
	dimension_swap=2

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

			self.cooldown = 100
			self.pause = 100
			self.vel = Vec3(0.0,0.0,0.0)
			self.queued_vel = Vec3(0.0,0.0,0.0)
			self.facing = False
			self.queued_facing = 4
			self.health = 3
			common_data.state = entity.eStates.stationary
			self.queued_state = common_data.state
			self.invincible_cooldown = 2
			self.invincible = self.invincible_cooldown
			self.type = 0
			self.fox_speed = 1


	#####################
	# end data __init__ #
	#####################




	def update(self, data, common_data, dt):
		data.cooldown-=1
		if data.cooldown<=0:
			data.cooldown=300+vector.rand_num(200)
			if data.fox_speed==1:
				data.fox_speed=0
				data.cooldown = data.pause
				data.pause -=10
			else:
				data.fox_speed=1
		fox_speed = data.fox_speed

		bunny_pos = data.bunny.getPos()
		bunny_coords = Vec3(int(bunny_pos.x/16),int(bunny_pos.y/16),0)

		if data.type==eFoxTypes.ahead:
			bunny_pos+= [
				Vec3(0,-64,0),
				Vec3(-64,0, 0),
				Vec3(0, 64, 0),
				Vec3(64, 0, 0),
			][data.bunny.controller_data.facing]

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

		if (abs(bunny_pos.x-common_data.pos.x)<abs(bunny_pos.y-common_data.pos.y))and data.type!=eFoxTypes.dimension_swap:
			swap = sec_dir
			sec_dir = pref_dir
			pref_dir = swap

		# try to go that way
		if ((x_in_tile-8)%16==0) and ((y_in_tile-8)%16==0):
			if pref_dir in exits:
				data.facing = pref_dir
			elif sec_dir in exits:
				data.facing = sec_dir
			else:
				data.facing = exits[0]

			data.vel = [
				Vec3(0,-fox_speed,0),
				Vec3(-fox_speed,0, 0),
				Vec3(0, fox_speed, 0),
				Vec3(fox_speed,0, 0),
			][data.facing]

		controller.basic_physics(common_data.pos, data.vel)
		common_data.pos.clamp(Vec3(0,0,0),Vec3(319,319,0))


	def receiveCollision(self, A, message):
		if message:
			if message.impassable:
				pass
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


