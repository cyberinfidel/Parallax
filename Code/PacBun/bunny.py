# system
import copy

# Parallax
import px_entity
import px_game_pad
import px_controller
import px_collision
from px_vector import Vec3
import px_sound
import PacBun

import tile

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

			self.cooldown = -1
			self.vel = Vec3(0.0,0.0,0.0)
			self.queued_vel = Vec3(0.0,0.0,0.0)
			self.facing = False
			self.queued_facing = 4
			entity.state = px_entity.eStates.stationary
			self.queued_state = entity.state
			self.score = 0




	#####################
	# end data __init__ #
	#####################




	def update(self, data, entity, dt):
		bunny_speed = 1

		# get input and set up an action
		if data.game_pad:
			# i.e. this bunny is being controlled by a game_pad
			# player wants to go left at next opportunity
			if data.game_pad.actions[px_game_pad.eActions.left]:
				# queue up that direction
				data.queued_facing = px_entity.eDirections.left
				data.queued_vel.x = -bunny_speed
				data.queued_vel.y = 0
				data.queued_state = px_entity.eStates.runLeft
			#  right
			elif data.game_pad.actions[px_game_pad.eActions.right]:
				data.queued_facing = px_entity.eDirections.right
				data.queued_vel.x = bunny_speed
				data.queued_vel.y = 0
				data.queued_state = px_entity.eStates.runRight
			# up
			elif data.game_pad.actions[px_game_pad.eActions.up]:
				data.queued_facing = px_entity.eDirections.up
				data.queued_vel.x = 0
				data.queued_vel.y = bunny_speed
				data.queued_state = px_entity.eStates.runUp
			# down
			elif data.game_pad.actions[px_game_pad.eActions.down]:
				data.queued_facing = px_entity.eDirections.down
				data.queued_vel.x = 0
				data.queued_vel.y = -bunny_speed
				data.queued_state = px_entity.eStates.runDown

		# what to do if the bunny is moving (i.e. except for the very start)
		if entity.state!=px_entity.eStates.stationary:
			# get some data to work with
			x, y = data.level.getCoordFromPos(entity.pos)
			current_tile = data.level.getTileFromCoord(x,y)
			exits = current_tile.controller.getExits(current_tile.controller_data)
			x_in_tile = entity.pos.x%16
			y_in_tile = entity.pos.y%16

			# decide if bunny is near middle of tile and if we should do womething special with the tile it's in
			if (6 < x_in_tile < 10) and (6 < y_in_tile <10):
				if current_tile.entity.state == tile.eTileStates.path:
					data.level.poo(current_tile, data)	# returns true if count of poos reaches number of empty spaces
					entity.game.reportScore(1)
				elif current_tile.entity.state == tile.eTileStates.hole:
					# gone down a hole so find the next hole for the bunny to exit from
					# and setup the direction for the bunny to run from the data for that hole
					if self.game.game_mode == PacBun.eGameModes.escape:
						self.game.setGameMode(PacBun.eGameModes.win)
						self.setState(data, entity, px_entity.eStates.dead)
						entity.blink = True
					hole = data.level.getNextHole(x,y)
					entity.pos = copy.deepcopy(hole.exit)
					data.facing = hole.direction
					# avoid any unexpected turns that were already queued
					data.queued_facing = hole.direction
					data.queued_state = (
						px_entity.eStates.runDown,
						px_entity.eStates.runLeft,
						px_entity.eStates.runUp,
						px_entity.eStates.runRight
					)[data.facing]
					# actually set the state
					self.setState(data, entity, data.queued_state)

			if ((
					(data.facing == px_entity.eDirections.left and data.queued_facing == px_entity.eDirections.right)
					or (data.facing == px_entity.eDirections.right and data.queued_facing == px_entity.eDirections.left)
					or (data.facing == px_entity.eDirections.up and data.queued_facing == px_entity.eDirections.down)
					or (data.facing == px_entity.eDirections.down and data.queued_facing == px_entity.eDirections.up)
			)
					or (x_in_tile==8 and y_in_tile==8
					and (((data.queued_facing == px_entity.eDirections.left) and (px_entity.eDirections.left in exits))
					or ((data.queued_facing == px_entity.eDirections.right) and (px_entity.eDirections.right in exits))
					or ((data.queued_facing == px_entity.eDirections.up) and (px_entity.eDirections.up in exits))
					or ((data.queued_facing == px_entity.eDirections.down) and (px_entity.eDirections.down in exits))))):
					data.facing = data.queued_facing
					self.setState(data, entity, data.queued_state)

			if data.facing==px_entity.eDirections.left:
				data.vel.x=-bunny_speed
				data.vel.y=0
			elif data.facing==px_entity.eDirections.right:
				data.vel.x=bunny_speed
				data.vel.y=0
			elif data.facing == px_entity.eDirections.up:
				data.vel.y = bunny_speed
				data.vel.x=0
			elif data.facing == px_entity.eDirections.down:
				data.vel.y = -bunny_speed
				data.vel.x=0

			# if at the centre of a tile then check if there's an exit in the direction the bunny
			# is running - if not stop the bunny
			if x_in_tile == 8 and y_in_tile == 8:
				if ((data.facing == px_entity.eDirections.left) and not (px_entity.eDirections.left in exits)) \
					or ((data.facing == px_entity.eDirections.right) and not (px_entity.eDirections.right in exits)):
						data.vel.x=0
				if ((data.facing == px_entity.eDirections.up) and not (px_entity.eDirections.up in exits)) \
					or ((data.facing == px_entity.eDirections.down) and not (px_entity.eDirections.down in exits)):
						data.vel.y=0



		else:
			# go the (first) queued direction that the player chooses
			self.setState(data, entity, data.queued_state)


		px_controller.basic_physics(entity.pos, data.vel)
		entity.pos.clamp(Vec3(0,0,0),Vec3(319,319,0))


	def receiveCollision(self, A, message):
		if message:
			if message.damage>0:
				A.entity.game.setGameMode(PacBun.eGameModes.game_over)
				A.controller_data.game_pad=False
				A.controller.setState(A.controller_data, A.entity, px_entity.eStates.dead)

			# print(f"col source{message.source.entity.pos.x},{message.source.entity.pos.y}")
		# 	print(f"Hedge source{message.source.entity.pos.x}{message.source.entity.pos.y}")
			# 	# A.controller_data.vel = Vec3(0,0,0)

def makeCollider(manager):
	return manager.makeTemplate({"Template": Collider})
class Collider(px_collision.Collider):
	class Data(object):
		def __init__(self, entity, init=False):
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

	def getCollisionMessage(self, data, entity):
		if entity.state!=px_entity.eStates.dead:
			return(px_collision.Message(source=entity.entity, damage_hero=1))
		else:
			return(px_collision.Message(source=entity.entity))



