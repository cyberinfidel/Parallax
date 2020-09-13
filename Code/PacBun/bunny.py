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

	def initEntity(self, entity, data=False):
		if entity.data:
			entity.game_pad = entity.data['game_pad']
		else:
			entity.game_pad=False
		entity.cooldown = -1
		entity.vel = Vec3(0.0,0.0,0.0)
		entity.queued_vel = Vec3(0.0,0.0,0.0)
		entity.facing = False
		entity.queued_facing = 4
		entity.state = PacBun.eStates.idle
		entity.queued_state = entity.state
		entity.score = 0

	def update(self, entity, dt):
		bunny_speed = 1
		map_entity = entity.parent
		map_controller = map_entity.getComponent('controller')
		# get input and set up an action
		if entity.game_pad:
			# i.e. this bunny is being controlled by a player with a game_pad
			# player wants to go left at next opportunity
			if entity.game_pad.actions[px_game_pad.eActions.left]:
				# queue up that direction
				entity.queued_facing = px_entity.eDirections.left
				entity.queued_vel.x = -bunny_speed
				entity.queued_vel.y = 0
				entity.queued_state = PacBun.eStates.runLeft
			#  right
			elif entity.game_pad.actions[px_game_pad.eActions.right]:
				entity.queued_facing = px_entity.eDirections.right
				entity.queued_vel.x = bunny_speed
				entity.queued_vel.y = 0
				entity.queued_state = PacBun.eStates.runRight
			# up
			elif entity.game_pad.actions[px_game_pad.eActions.up]:
				entity.queued_facing = px_entity.eDirections.up
				entity.queued_vel.x = 0
				entity.queued_vel.y = bunny_speed
				entity.queued_state = PacBun.eStates.runUp
			# down
			elif entity.game_pad.actions[px_game_pad.eActions.down]:
				entity.queued_facing = px_entity.eDirections.down
				entity.queued_vel.x = 0
				entity.queued_vel.y = -bunny_speed
				entity.queued_state = PacBun.eStates.runDown

		x, y = map_controller.getCoordFromPos(entity.pos)
		current_tile = map_controller.getTileFromCoord(map_entity,x,y)
		exits = current_tile.process('getExits')
		x_in_tile = entity.pos.x%16
		y_in_tile = entity.pos.y%16

		# decide if bunny is near middle of tile and if we should do womething special with the tile it's in
		if (6 < x_in_tile < 10) and (6 < y_in_tile <10):
			if current_tile.state == tile.eTileStates.path:
				map_controller.poo(map_entity, current_tile, entity)	# returns true if count of poos reaches number of empty spaces
				entity.game.reportScore(1)
			elif current_tile.state == tile.eTileStates.hole:
				# gone down a hole so find the next hole for the bunny to exit from
				# and setup the direction for the bunny to run from the entity for that hole
				if self.game.game_mode == PacBun.eGameModes.escape:
					self.game.setGameMode(PacBun.eGameModes.win)
					self.setState(entity, PacBun.eStates.dead)
					entity.blink = True
				hole = map_controller.getNextHole(map_entity,x,y)
				entity.pos = copy.deepcopy(hole.exit)
				entity.facing = hole.direction
				# avoid any unexpected turns that were already queued
				entity.queued_facing = hole.direction
				entity.queued_state = (
					PacBun.eStates.runDown,
					PacBun.eStates.runLeft,
					PacBun.eStates.runUp,
					PacBun.eStates.runRight
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

			if entity.vel.x==0 and entity.vel.y==0:
				entity.setState(PacBun.eStates.idle)





		px_controller.basic_physics(entity.pos, entity.vel)
		entity.pos.clamp(Vec3(0,0,0),Vec3(319,319,0))


	def receiveCollision(self, A, message):
		if message:
			if message.damage>0:
				A.game.setGameMode(PacBun.eGameModes.game_over)
				A.game_pad=False
				A.setState(PacBun.eStates.dead)


def makeCollider(manager):
	return manager.makeTemplate({"Template": Collider})
class Collider(px_collision.Collider):
	def __init__(self, game, data):
		super(Collider, self).__init__(game)
		# global static data to all of HeroCollider components

	def initEntity(self, entity, data=False):
			entity.dim = Vec3(8,8,8)
			entity.orig = Vec3(4,4,4)

	def getCollisionMessage(self, entity):
		if entity.state!=PacBun.eStates.dead:
			return(px_collision.Message(source=entity, damage_hero=1))
		else:
			return(px_collision.Message(source=entity))



