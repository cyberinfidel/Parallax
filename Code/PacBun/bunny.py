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
import PacBun

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

def makeGraphicsYellow(manager, renlayer):
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
						["Graphics/Bunny/Yellow/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Yellow/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Yellow/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Yellow/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Yellow/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Yellow/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Yellow/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Yellow/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Yellow/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Yellow/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Yellow/Idle 3.png", 8, 11, 0, 0.2],
					]
			},
			{
				"Name": "Bunny Runs Down",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runDown],
				"Frames":
					[
						["Graphics/Bunny/Yellow/RunDown 2.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Yellow/RunDown 3.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Yellow/RunDown 4.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Yellow/RunDown 1.png", 8, 11, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Up",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runUp],
				"Frames":
					[
						["Graphics/Bunny/Yellow/RunUp 2.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Yellow/RunUp 3.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Yellow/RunUp 4.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Yellow/RunUp 1.png", 8, 11, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Left",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runLeft],
				"Frames":
					[
						["Graphics/Bunny/Yellow/RunLeft 1.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Yellow/RunLeft 2.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Yellow/RunLeft 3.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Yellow/RunLeft 4.png", 8, 14, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Right",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runRight],
				"Frames":
					[
						["Graphics/Bunny/Yellow/RunRight 1.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Yellow/RunRight 2.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Yellow/RunRight 3.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Yellow/RunRight 4.png", 8, 14, 0, 0.075],
					],
			},

		]

	})



def makeGraphicsPink(manager, renlayer):
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
						["Graphics/Bunny/Pink/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Pink/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Pink/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Pink/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Pink/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Pink/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Pink/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Pink/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Pink/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Pink/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Pink/Idle 3.png", 8, 11, 0, 0.2],
					]
			},
			{
				"Name": "Bunny Runs Down",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runDown],
				"Frames":
					[
						["Graphics/Bunny/Pink/RunDown 2.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Pink/RunDown 3.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Pink/RunDown 4.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Pink/RunDown 1.png", 8, 11, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Up",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runUp],
				"Frames":
					[
						["Graphics/Bunny/Pink/RunUp 2.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Pink/RunUp 3.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Pink/RunUp 4.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Pink/RunUp 1.png", 8, 11, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Left",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runLeft],
				"Frames":
					[
						["Graphics/Bunny/Pink/RunLeft 1.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Pink/RunLeft 2.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Pink/RunLeft 3.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Pink/RunLeft 4.png", 8, 14, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Right",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runRight],
				"Frames":
					[
						["Graphics/Bunny/Pink/RunRight 1.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Pink/RunRight 2.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Pink/RunRight 3.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Pink/RunRight 4.png", 8, 14, 0, 0.075],
					],
			},

		]

	})

def makeGraphicsBlue(manager, renlayer):
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
						["Graphics/Bunny/Blue/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Blue/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Blue/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Blue/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Blue/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Blue/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Blue/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Blue/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Blue/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Blue/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Blue/Idle 3.png", 8, 11, 0, 0.2],
					]
			},
			{
				"Name": "Bunny Runs Down",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runDown],
				"Frames":
					[
						["Graphics/Bunny/Blue/RunDown 2.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Blue/RunDown 3.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Blue/RunDown 4.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Blue/RunDown 1.png", 8, 11, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Up",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runUp],
				"Frames":
					[
						["Graphics/Bunny/Blue/RunUp 2.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Blue/RunUp 3.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Blue/RunUp 4.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Blue/RunUp 1.png", 8, 11, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Left",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runLeft],
				"Frames":
					[
						["Graphics/Bunny/Blue/RunLeft 1.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Blue/RunLeft 2.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Blue/RunLeft 3.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Blue/RunLeft 4.png", 8, 14, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Right",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runRight],
				"Frames":
					[
						["Graphics/Bunny/Blue/RunRight 1.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Blue/RunRight 2.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Blue/RunRight 3.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/Blue/RunRight 4.png", 8, 14, 0, 0.075],
					],
			},

		]

	})

def makeGraphicsWhite(manager, renlayer):
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
						["Graphics/Bunny/White/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/White/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/White/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/White/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/White/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/White/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/White/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/White/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/White/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/White/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/White/Idle 3.png", 8, 11, 0, 0.2],
					]
			},
			{
				"Name": "Bunny Runs Down",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runDown],
				"Frames":
					[
						["Graphics/Bunny/White/RunDown 2.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/White/RunDown 3.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/White/RunDown 4.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/White/RunDown 1.png", 8, 11, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Up",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runUp],
				"Frames":
					[
						["Graphics/Bunny/White/RunUp 2.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/White/RunUp 3.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/White/RunUp 4.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/White/RunUp 1.png", 8, 11, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Left",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runLeft],
				"Frames":
					[
						["Graphics/Bunny/White/RunLeft 1.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/White/RunLeft 2.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/White/RunLeft 3.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/White/RunLeft 4.png", 8, 14, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Right",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runRight],
				"Frames":
					[
						["Graphics/Bunny/White/RunRight 1.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/White/RunRight 2.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/White/RunRight 3.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/White/RunRight 4.png", 8, 14, 0, 0.075],
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
			self.queued_facing = 4
			common_data.state = entity.eStates.stationary
			self.queued_state = common_data.state
			self.score = 0




	#####################
	# end data __init__ #
	#####################




	def update(self, data, common_data, dt):
		bunny_speed = 1

		# get input and set up an action
		if data.game_pad:
			# i.e. this bunny is being controlled by a game_pad
			# player wants to go left at next opportunity
			if data.game_pad.actions[game_pad.eActions.left]:
				# queue up that direction
				data.queued_facing = entity.eDirections.left
				data.queued_vel.x = -bunny_speed
				data.queued_vel.y = 0
				data.queued_state = entity.eStates.runLeft
			#  right
			elif data.game_pad.actions[game_pad.eActions.right]:
				data.queued_facing = entity.eDirections.right
				data.queued_vel.x = bunny_speed
				data.queued_vel.y = 0
				data.queued_state = entity.eStates.runRight
			# up
			elif data.game_pad.actions[game_pad.eActions.up]:
				data.queued_facing = entity.eDirections.up
				data.queued_vel.x = 0
				data.queued_vel.y = bunny_speed
				data.queued_state = entity.eStates.runUp
			# down
			elif data.game_pad.actions[game_pad.eActions.down]:
				data.queued_facing = entity.eDirections.down
				data.queued_vel.x = 0
				data.queued_vel.y = -bunny_speed
				data.queued_state = entity.eStates.runDown

		# what to do if the bunny is moving (i.e. except for the very start)
		if common_data.state!=entity.eStates.stationary:
			# get some data to work with
			x, y = data.level.getCoordFromPos(common_data.pos)
			current_tile = data.level.getTileFromCoord(x,y)
			exits = current_tile.controller.getExits(current_tile.controller_data)
			x_in_tile = common_data.pos.x%16
			y_in_tile = common_data.pos.y%16

			# decide if bunny is near middle of tile and if we should do womething special with the tile it's in
			if (6 < x_in_tile < 10) and (6 < y_in_tile <10):
				if current_tile.common_data.state == tile.eTileStates.clear:
					data.level.poo(current_tile, data)	# returns true if count of poos reaches number of empty spaces
					common_data.game.reportScore(1)
				elif current_tile.common_data.state == tile.eTileStates.hole:
					# gone down a hole so find the next hole for the bunny to exit from
					# and setup the direction for the bunny to run from the data for that hole
					if self.game.game_mode == PacBun.eGameModes.escape:
						self.game.setGameMode(PacBun.eGameModes.win)
						self.setState(data, common_data, entity.eStates.dead)
						common_data.blink = True
					hole = data.level.getNextHole(x,y)
					common_data.pos = copy.deepcopy(hole.exit)
					data.facing = hole.direction
					# avoid any unexpected turns that were already queued
					data.queued_facing = hole.direction
					data.queued_state = (
						entity.eStates.runDown,
						entity.eStates.runLeft,
						entity.eStates.runUp,
						entity.eStates.runRight
					)[data.facing]
					# actually set the state
					self.setState(data, common_data, data.queued_state)

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

			# if at the centre of a tile then check if there's an exit in the direction the bunny
			# is running - if not stop the bunny
			if x_in_tile == 8 and y_in_tile == 8:
				if ((data.facing == entity.eDirections.left) and not (entity.eDirections.left in exits)) \
					or ((data.facing == entity.eDirections.right) and not (entity.eDirections.right in exits)):
						data.vel.x=0
				if ((data.facing == entity.eDirections.up) and not (entity.eDirections.up in exits)) \
					or ((data.facing == entity.eDirections.down) and not (entity.eDirections.down  in exits)):
						data.vel.y=0



		else:
			# go the (first) queued direction that the player chooses
			self.setState(data, common_data, data.queued_state)


		controller.basic_physics(common_data.pos, data.vel)
		common_data.pos.clamp(Vec3(0,0,0),Vec3(319,319,0))


	def receiveCollision(self, A, message):
		if message:
			if message.damage>0:
				A.common_data.game.setGameMode(game.eGameModes.game_over)
				A.controller_data.game_pad=False
				A.controller.setState(A.controller_data,A.common_data,entity.eStates.dead)

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
			self.dim = Vec3(8,8,8)
			self.orig = Vec3(4,4,4)
			self.mass = 10.0
			self.force = 0.0

	def __init__(self, game, data):
		super(Collider, self).__init__(game)
		# global static data to all of HeroCollider components

	def getRadius(self):
		return self.radius

	def getCollisionMessage(self, data, common_data):
		if common_data.state!=entity.eStates.dead:
			return(collision.Message(source=common_data.entity, damage_hero=1))
		else:
			return(collision.Message(source=common_data.entity))

