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

	def initEntity(self, entity, data=False):
		entity.game_pad = False
		entity.cooldown = -1
		entity.vel = Vec3(0.0,0.0,0.0)
		entity.queued_vel = Vec3(0.0,0.0,0.0)
		entity.facing = False
		entity.queued_facing = 4
		entity.state = px_entity.eStates.stationary
		entity.queued_state = entity.state
		entity.score = 0



	#####################
	# end data __init__ #
	#####################




	def update(self, entity, dt):
		bunny_speed = 1

		# get input and set up an action
		if entity.game_pad:
			# i.e. this bunny is being controlled by a game_pad
			# player wants to go left at next opportunity
			if entity.game_pad.actions[px_game_pad.eActions.left]:
				# queue up that direction
				entity.queued_facing = px_entity.eDirections.left
				entity.queued_vel.x = -bunny_speed
				entity.queued_vel.y = 0
				entity.queued_state = px_entity.eStates.runLeft
			#  right
			elif entity.game_pad.actions[px_game_pad.eActions.right]:
				entity.queued_facing = px_entity.eDirections.right
				entity.queued_vel.x = bunny_speed
				entity.queued_vel.y = 0
				entity.queued_state = px_entity.eStates.runRight
			# up
			elif entity.game_pad.actions[px_game_pad.eActions.up]:
				entity.queued_facing = px_entity.eDirections.up
				entity.queued_vel.x = 0
				entity.queued_vel.y = bunny_speed
				entity.queued_state = px_entity.eStates.runUp
			# down
			elif entity.game_pad.actions[px_game_pad.eActions.down]:
				entity.queued_facing = px_entity.eDirections.down
				entity.queued_vel.x = 0
				entity.queued_vel.y = -bunny_speed
				entity.queued_state = px_entity.eStates.runDown

		# what to do if the bunny is moving (i.e. except for the very start)
		if entity.state!=px_entity.eStates.stationary:
			# get some entity to work with
			x, y = entity.level.getCoordFromPos(entity.pos)
			current_tile = entity.level.getTileFromCoord(x,y)
			exits = current_tile.controller.getExits(current_tile.controller_entity)
			x_in_tile = entity.pos.x%16
			y_in_tile = entity.pos.y%16

			# decide if bunny is near middle of tile and if we should do womething special with the tile it's in
			if (6 < x_in_tile < 10) and (6 < y_in_tile <10):
				if current_tile.entity.state == tile.eTileStates.path:
					entity.level.poo(current_tile, entity)	# returns true if count of poos reaches number of empty spaces
					entity.game.reportScore(1)
				elif current_tile.entity.state == tile.eTileStates.hole:
					# gone down a hole so find the next hole for the bunny to exit from
					# and setup the direction for the bunny to run from the entity for that hole
					if self.game.game_mode == PacBun.eGameModes.escape:
						self.game.setGameMode(PacBun.eGameModes.win)
						self.setState(entity, px_entity.eStates.dead)
						entity.blink = True
					hole = entity.level.getNextHole(x,y)
					entity.pos = copy.deepcopy(hole.exit)
					entity.facing = hole.direction
					# avoid any unexpected turns that were already queued
					entity.queued_facing = hole.direction
					entity.queued_state = (
						px_entity.eStates.runDown,
						px_entity.eStates.runLeft,
						px_entity.eStates.runUp,
						px_entity.eStates.runRight
					)[entity.facing]
					# actually set the state
					self.setState(entity, entity.queued_state)

			if ((
					(entity.facing == px_entity.eDirections.left and entity.queued_facing == px_entity.eDirections.right)
					or (entity.facing == px_entity.eDirections.right and entity.queued_facing == px_entity.eDirections.left)
					or (entity.facing == px_entity.eDirections.up and entity.queued_facing == px_entity.eDirections.down)
					or (entity.facing == px_entity.eDirections.down and entity.queued_facing == px_entity.eDirections.up)
			)
					or (x_in_tile==8 and y_in_tile==8
					and (((entity.queued_facing == px_entity.eDirections.left) and (px_entity.eDirections.left in exits))
					or ((entity.queued_facing == px_entity.eDirections.right) and (px_entity.eDirections.right in exits))
					or ((entity.queued_facing == px_entity.eDirections.up) and (px_entity.eDirections.up in exits))
					or ((entity.queued_facing == px_entity.eDirections.down) and (px_entity.eDirections.down in exits))))):
					entity.facing = entity.queued_facing
					self.setState(entity, entity.queued_state)

			if entity.facing==px_entity.eDirections.left:
				entity.vel.x=-bunny_speed
				entity.vel.y=0
			elif entity.facing==px_entity.eDirections.right:
				entity.vel.x=bunny_speed
				entity.vel.y=0
			elif entity.facing == px_entity.eDirections.up:
				entity.vel.y = bunny_speed
				entity.vel.x=0
			elif entity.facing == px_entity.eDirections.down:
				entity.vel.y = -bunny_speed
				entity.vel.x=0

			# if at the centre of a tile then check if there's an exit in the direction the bunny
			# is running - if not stop the bunny
			if x_in_tile == 8 and y_in_tile == 8:
				if ((entity.facing == px_entity.eDirections.left) and not (px_entity.eDirections.left in exits)) \
					or ((entity.facing == px_entity.eDirections.right) and not (px_entity.eDirections.right in exits)):
						entity.vel.x=0
				if ((entity.facing == px_entity.eDirections.up) and not (px_entity.eDirections.up in exits)) \
					or ((entity.facing == px_entity.eDirections.down) and not (px_entity.eDirections.down in exits)):
						entity.vel.y=0



		else:
			# go the (first) queued direction that the player chooses
			self.setState(entity, entity.queued_state)


		px_controller.basic_physics(entity.pos, entity.vel)
		entity.pos.clamp(Vec3(0,0,0),Vec3(319,319,0))


	def receiveCollision(self, A, message):
		if message:
			if message.damage>0:
				A.entity.game.setGameMode(PacBun.eGameModes.game_over)
				A.controller_data.game_pad=False
				A.controller.setState(A.entity, px_entity.eStates.dead)


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

	def getCollisionMessage(self, entity):
		if entity.state!=px_entity.eStates.dead:
			return(px_collision.Message(source=entity.entity, damage_hero=1))
		else:
			return(px_collision.Message(source=entity.entity))



