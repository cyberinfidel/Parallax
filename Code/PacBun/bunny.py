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

import path



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
		"Name": "Bunny Animations",
		"Template": graphics.MultiAnim,
		"RenderLayer": renlayer,
		"Anims": [
			{
				"Name": "Bunny Stands",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.stationary],
				"Frames":
					[
						["Graphics/Bunny/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Idle 3.png", 8, 11, 0, 0.2],
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
			self.vel = Vec3(0.0,0.0,0.0)
			self.queued_vel = Vec3(0.0,0.0,0.0)
			self.facing = False
			self.queued_facing = False
			self.health = 3
			common_data.state = entity.eStates.stationary
			self.queued_state = common_data.state
			self.invincible_cooldown = 2
			self.invincible = self.invincible_cooldown


	#####################
	# end data __init__ #
	#####################




	def update(self, data, common_data, dt):
		bunny_speed = 1

		# get input and set up an action
		if data.game_pad:
			# i.e. this bunny is being controlled by a game_pad
			# going left
			if data.game_pad.actions[game_pad.eActions.left]:
				data.queued_facing = entity.eDirections.left
				data.queued_state = entity.eStates.runLeft
				data.queued_vel.x = -bunny_speed
				data.queued_vel.y = 0

			# going right
			elif data.game_pad.actions[game_pad.eActions.right]:
				data.queued_facing = entity.eDirections.right
				data.queued_state = entity.eStates.runRight
				data.queued_vel.x = bunny_speed
				data.queued_vel.y = 0

			# going up
			elif data.game_pad.actions[game_pad.eActions.up]:
				data.queued_facing = entity.eDirections.up
				data.queued_state = entity.eStates.runUp
				data.queued_vel.x = 0
				data.queued_vel.y = bunny_speed

			# going down
			elif data.game_pad.actions[game_pad.eActions.down]:
				data.queued_facing = entity.eDirections.down
				data.queued_state = entity.eStates.runDown
				data.queued_vel.x = 0
				data.queued_vel.y = -bunny_speed



		x, y = data.level.getCoordFromPos(common_data.pos)
		exits = data.level.getExitsFromCoord(x,y)
		x_in_tile = common_data.pos.x%16
		y_in_tile = common_data.pos.y%16

		if (x_in_tile>6 and x_in_tile<10) and (y_in_tile>6 and y_in_tile<10):
			pood = data.level.poo(x,y)
			if pood:
				common_data.game.setGameMode(game.eGameModes.win)


		# data.facing = data.queued_facing
					# data.vel =  copy.deepcopy(data.queued_vel)
					# self.updateState(data, common_data, data.queued_state)
		# print(f"{x_in_tile},{y_in_tile} {exits}")

		if ((
				(data.facing==entity.eDirections.left and data.queued_facing==entity.eDirections.right)
				or (data.facing == entity.eDirections.right and data.queued_facing == entity.eDirections.left)
				or (data.facing == entity.eDirections.up and data.queued_facing == entity.eDirections.down)
				or (data.facing == entity.eDirections.down and data.queued_facing == entity.eDirections.up)
		)
				or (x_in_tile==8 and y_in_tile==8
				and (((data.queued_facing == entity.eDirections.left) and (entity.eDirections.left in exits))
				or ((data.queued_facing == entity.eDirections.right) and (entity.eDirections.right in exits))
				or ((data.queued_facing == entity.eDirections.up) and (entity.eDirections.up in exits))
				or ((data.queued_facing == entity.eDirections.down) and (entity.eDirections.down in exits))))):
				data.facing = data.queued_facing
				self.setState(data, common_data, data.queued_state)

		if data.facing==entity.eDirections.left:
			data.vel.x=-bunny_speed
			data.vel.y=0
		elif data.facing==entity.eDirections.right:
			data.vel.x=bunny_speed
			data.vel.y=0
		elif data.facing == entity.eDirections.up:
			data.vel.y = bunny_speed
			data.vel.x=0
		elif data.facing == entity.eDirections.down:
			data.vel.y = -bunny_speed
			data.vel.x=0


		if x_in_tile == 8 and y_in_tile == 8:
			if ((data.facing == entity.eDirections.left) and not (entity.eDirections.left in exits)) \
				or ((data.facing == entity.eDirections.right) and not (entity.eDirections.right in exits)):
					data.vel.x=0
			if ((data.facing == entity.eDirections.up) and not (entity.eDirections.up in exits)) \
				or ((data.facing == entity.eDirections.down) and not (entity.eDirections.down  in exits)):
					data.vel.y=0



		if data.game_pad.actions[game_pad.eActions.jump]:
			data.vel = Vec3(0,0,0)


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
			self.dim = Vec3(16,16,8)
			self.orig = Vec3(7,7,4)
			self.mass = 10.0
			self.force = 0.0

	def __init__(self, game, data):
		super(Collider, self).__init__(game)
		# global static data to all of HeroCollider components

	def getRadius(self):
		return self.radius

	def getCollisionMessage(self, data, common_data):
		return(collision.Message(source=common_data.entity))


