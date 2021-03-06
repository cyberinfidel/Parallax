import enum

import px_entity
import px_vector
from px_vector import Vec3, rand_num
import px_controller
import px_collision
import px_graphics
import px_sound
import background

class eEvents(enum.IntEnum):
	flap = 0
	num_events = 1

def makeSounds(manager, mixer):
	return manager.makeTemplate( {
		"Name": "Bat Sounds",
		"Template": px_sound.MultiSound,
		"Mixer": mixer,
		"StateSounds": [
		],
		"EventSounds":
			[
				{
					"Name": "Jump",
					"Type": px_sound.Single,
					"Events": [eEvents.flap],
					"Samples":  # one of these will play at random if there's more than one
						[
							"Sounds/Bat/flap.wav"
						]
				}

			]
	})


def makeGraphics(manager, renlayer):
	return manager.makeTemplate({
			"Name": "Bat",
			"Template": px_graphics.MultiAnim,
			"RenderLayer": renlayer,
			"Anims":
				[
			{
				"Name": "Bat Flapping",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [px_entity.eStates.stationary],
				"Frames":
					[
						["Graphics/Bat/Bat2.png", 24, 30, 0, 0.04],
						["Graphics/Bat/Bat3.png", 24, 30, 0, 0.04],
						["Graphics/Bat/Bat4.png", 24, 30, 0, 0.1],
						["Graphics/Bat/Bat3.png", 24, 30, 0, 0.1],
						["Graphics/Bat/Bat2.png", 24, 30, 0, 0.1],
						["Graphics/Bat/Bat1.png", 24, 30, 0, 0.5],
					],
			},
			{
				"Name": "Simple Fall Left",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [px_entity.eStates.fallLeft],
				"Frames":
					[
						["Graphics/Bat/BatHurt 1.png", 24, 30, 0, 0.04],
						["Graphics/Bat/BatHurt 2.png", 24, 30, 0, 0.04],
						["Graphics/Bat/BatHurt 3.png", 24, 30, 0, 0.04],
						["Graphics/Bat/BatFallLeft.png", 24, 0, 20, 0.04],
					],
			},
			{
				"Name": "Simple Fall Right",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [px_entity.eStates.fallRight],
				"Frames":
					[
						["Graphics/Bat/BatHurt 1.png", 24, 30, 0, 0.04],
						["Graphics/Bat/BatHurt 2.png", 24, 30, 0, 0.04],
						["Graphics/Bat/BatHurt 3.png", 24, 30, 0, 0.04],
						["Graphics/Bat/BatFallRight.png", 24, 0, 20, 0.04],
					],
			},
			{
				"Name": "Hurt Left",
				"AnimType": px_graphics.AnimLoop,
				"States": [px_entity.eStates.hurtLeft, px_entity.eStates.hurtRight],
				"Frames":
				[
					["Graphics/Bat/BatHurt 1.png", 24, 30, 0, 0.04],
					["Graphics/Bat/BatHurt 2.png", 24, 30, 0, 0.04],
					["Graphics/Bat/BatHurt 3.png", 24, 30, 0, 0.04],
					["Graphics/Bat/BatHurt 2.png", 24, 30, 0, 0.04],
					["Graphics/Bat/BatHurt 1.png", 24, 30, 0, 0.04],
				],
			},
			{
				"Name": "Bat Shadow",
				"AnimType": px_graphics.AnimSingle,
				"States": [px_entity.eStates.shadow],
				"Frames":
					[
						["Graphics/shadow.png", 16, 4, 0, 0.3],
					],
			},
			]
		})

def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(px_controller.Controller):

	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.cooldown = 0
			self.health = 5
			self.vel = Vec3(0,0,0)
			self.mass = 4
			self.facing = px_entity.eDirections.left

	def __init__(self, game, data):
		super(Controller, self).__init__(game)

	def update(self, data, common_data, dt):
		speed = 0.3
		# if doing something that can't be interrupted then countdown to end of it

		if self.coolDown(data, dt):
			pass
		else:
			if data.health <= 0:
				self.setState(data, common_data, px_entity.eStates.dead)
				return
			self.setState(data, common_data, px_entity.eStates.stationary)
			if rand_num(10)==0:
#				self.setState(data, common_data, eStates.stationary)
				data.vel = Vec3(0,0,0)
				data.cooldown = rand_num(10)/8.0+0.3
			else:
				# chase hero
				target = common_data.game.requestTarget(common_data.pos)
				if(target.x<common_data.pos.x):
#					self.setState(data, common_data, eStates.runLeft)
					data.vel = Vec3(-speed, 0, 0)
					data.facing = px_entity.eDirections.left
				else:
#					self.setState(data, common_data, eStates.runRight)
					data.vel = Vec3(speed, 0, 0)
					data.facing = px_entity.eDirections.right
				if(target.z<common_data.pos.z):
					data.vel.z = -speed
				else:
					data.vel.z = speed

				if common_data.pos.distSq(Vec3(target.x,target.y,common_data.pos.y))<800:
					data.vel.y = 0 # drop on target
				elif (common_data.pos.z<80) and (data.vel.z<3):
					data.vel.y += 2 # otherwise flap
					# common_data.entity.graphics.startAnim(data = common_data.entity.graphics_data)
					self.setState(data, common_data, px_entity.eStates.stationary, force_new_state=True)
					common_data.entity.sounds.playEvent(data, common_data, eEvents.flap)

				data.cooldown = 0.2

		if common_data.pos.y>0:
			px_controller.friction(data.vel, 0.01)
		else:
			px_controller.friction(data.vel, 0.1)

		px_controller.basic_gravity(data.vel)
		px_controller.basic_physics(common_data.pos, data.vel)

		background.restrictToArena(common_data.pos, data.vel)



	def receiveCollision(self, this_entity, message):
		data = this_entity.controller_data
		common_data = this_entity.common_data
		if message:
			data.vel += message.force/data.mass
			if message.damage>0 and data.health>0:
				hurt_cool = 1
				fall_cool = 3
				data.health -= message.damage
				if data.facing == px_entity.eDirections.left:
					if data.health <= 0:
						self.setState(data, common_data, px_entity.eStates.fallLeft, fall_cool)
						common_data.game.reportMonsterDeath()
					else:
						self.setState(data, common_data, px_entity.eStates.hurtLeft, hurt_cool)
				else:
					if data.health <= 0:
						self.setState(data, common_data, px_entity.eStates.fallRight, fall_cool)
						common_data.game.reportMonsterDeath()
					else:
						self.setState(data, common_data, px_entity.eStates.hurtRight, hurt_cool)

def makeCollider(manager):
	return manager.makeTemplate({"Template": Collider})
class Collider(px_collision.Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.dim = Vec3(20,16,8)
			self.orig = Vec3(10,0,4)
			self.damage = 1
			self.damage_hero = 1
			self.force = Vec3(0,0,0)

	def __init__(self, game, data):
		super(Collider, self).__init__(game)
		# global static data to all of BatCollider components

	def getCollisionMessage(self, data, common_data):
		return(px_collision.Message(source=common_data.entity, damage=0, damage_hero=1))







