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
						["Graphics/Fox/Pant/Pant_000.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_001.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_002.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_003.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_004.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_005.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_006.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_007.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_008.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_009.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_010.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_011.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_012.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_013.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_014.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_015.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_016.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_017.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_018.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_019.png", 11, 15, 0, 0.02],
					]
			},
			{
				"Name": "Fox Cleans L",
				"AnimType": graphics.AnimLoop,
				"States": [eFoxStates.cleanLeft],
				"Frames":
					[
						["Graphics/Fox/CleanL/CleanL_000.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_001.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_002.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_003.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_004.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_005.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_006.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_007.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_008.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_009.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_010.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_011.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_012.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_013.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_005.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_006.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_007.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_008.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_009.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_010.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_011.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_012.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_013.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_005.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_006.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_007.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_008.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_009.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_010.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_011.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_012.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_013.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_005.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_006.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_007.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_008.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_009.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_010.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_011.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_012.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_013.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_014.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_015.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_016.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_017.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_018.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_019.png", 15, 15, 0, 0.02],
					]
			},
			{
				"Name": "Fox Cleans L",
				"AnimType": graphics.AnimLoop,
				"States": [eFoxStates.cleanRight],
				"Frames":
					[
						["Graphics/Fox/CleanR/CleanR_000.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_001.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_002.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_003.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_004.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_005.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_006.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_007.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_008.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_009.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_010.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_011.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_012.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_013.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_005.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_006.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_007.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_008.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_009.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_010.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_011.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_012.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_013.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_005.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_006.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_007.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_008.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_009.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_010.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_011.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_012.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_013.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_014.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_015.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_016.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_017.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_018.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_019.png", 15, 15, 0, 0.02],
					]
			},
			{
				"Name": "Bunny Runs Down",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runDown],
				"Frames":
					[
						["Graphics/Fox/RunD_000.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_001.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_002.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_003.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_004.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_005.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_006.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_007.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_008.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_009.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_010.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_011.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_012.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_013.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_014.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_015.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_016.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_017.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_018.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_019.png", 6, 20, 0, 0.02],
					],
			},
			{
				"Name": "Bunny Runs Up",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runUp],
				"Frames":
					[
						["Graphics/Fox/RunU_000.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_001.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_002.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_003.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_004.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_005.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_006.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_007.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_008.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_009.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_010.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_011.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_012.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_013.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_014.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_015.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_016.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_017.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_018.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_019.png", 6, 20, 0, 0.02],
					],
			},
			{
				"Name": "Bunny Runs Left",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runLeft],
				"Frames":
					[
						["Graphics/Fox/Left/Run_000.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_001.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_002.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_003.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_004.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_005.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_006.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_007.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_008.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_009.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_010.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_011.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_012.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_013.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_014.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_015.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_016.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_017.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_018.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_019.png", 20, 11, 0, 0.02],
					],
			},
			{
				"Name": "Bunny Runs Right",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runRight],
				"Frames":
					[
						["Graphics/Fox/Run_000.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_001.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_002.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_003.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_004.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_005.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_006.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_007.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_008.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_009.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_010.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_011.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_012.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_013.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_014.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_015.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_016.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_017.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_018.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_019.png", 20, 11, 0, 0.02],
					],
			},
			{
				"Name": "Bunny Caught",
				"AnimType": graphics.AnimLoop,
				"States": [eFoxStates.bunnyCaught],
				"Frames":
					[
						["Graphics/Fox/FoxCaught.png", 11, 15, 0, 0.02],
					],
			},
		]

	})


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
			self.pause = 10
			self.vel = Vec3(0.0,0.0,0.0)
			self.queued_vel = Vec3(0.0,0.0,0.0)
			self.facing = False
			self.queued_facing = 4
			self.health = 3
			common_data.state = entity.eStates.stationary
			self.queued_state = common_data.state
			self.AI_cooldown = 3+vector.rand_num(10)/5
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
											[entity.eStates.stationary,eFoxStates.cleanLeft,eFoxStates.cleanRight][vector.rand_num(3)]
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


