import enum

from entity import eStates, eDirections
from vector import Vec3, rand_num
from controller import Controller, basic_gravity, basic_physics, restrictToArena, friction
from collision import Collider, Message
from graphics import AnimLoop, AnimNoLoop, MultiAnim, AnimSingle
import sound

class eEvents(enum.IntEnum):
	flap = 0
	num_events = 1

def batSounds(mixer):
	return {
		"Name": "Bat Sounds",
		"Template": sound.MultiSound,
		"Mixer": mixer,
		"StateSounds": [
		],
		"EventSounds":
			[
				{
					"Name": "Jump",
					"Type": sound.Single,
					"Events": [eEvents.flap],
					"Samples":  # one of these will play at random if there's more than one
						[
							"Sounds/Bat/flap.wav"
						]
				}

			]
	}


def batGraphics(renlayer):
	return {
			"Name": "Bat",
			"Template": MultiAnim,
			"RenderLayer": renlayer,
			"Anims":
				[
			{
				"Name": "Bat Flapping",
				"AnimType": AnimLoop,
				"States": [eStates.stationary],
				"Frames":
					[
						["Graphics/Bat/Bat2.png", 24, 30, 0.04],
						["Graphics/Bat/Bat3.png", 24, 30, 0.04],
						["Graphics/Bat/Bat4.png", 24, 30, 0.1],
						["Graphics/Bat/Bat3.png", 24, 30, 0.1],
						["Graphics/Bat/Bat2.png", 24, 30, 0.1],
						["Graphics/Bat/Bat1.png", 24, 30, 0.5],
					],
			},
			{
				"Name": "Simple Fall Left",
				"AnimType": AnimNoLoop,
				"States": [eStates.fallLeft],
				"Frames":
					[
						["Graphics/Bat/BatHurt 1.png", 24, 30, 0.04],
						["Graphics/Bat/BatHurt 2.png", 24, 30, 0.04],
						["Graphics/Bat/BatHurt 3.png", 24, 30, 0.04],
						["Graphics/Bat/BatFallLeft.png", 24, 20, 0.04],
					],
			},
			{
				"Name": "Simple Fall Right",
				"AnimType": AnimNoLoop,
				"States": [eStates.fallRight],
				"Frames":
					[
						["Graphics/Bat/BatHurt 1.png", 24, 30, 0.04],
						["Graphics/Bat/BatHurt 2.png", 24, 30, 0.04],
						["Graphics/Bat/BatHurt 3.png", 24, 30, 0.04],
						["Graphics/Bat/BatFallRight.png", 24, 20, 0.04],
					],
			},
			{
				"Name": "Hurt Left",
				"AnimType": AnimLoop,
				"States": [eStates.hurtLeft, eStates.hurtRight],
				"Frames":
				[
					["Graphics/Bat/BatHurt 1.png", 24, 30, 0.04],
					["Graphics/Bat/BatHurt 2.png", 24, 30, 0.04],
					["Graphics/Bat/BatHurt 3.png", 24, 30, 0.04],
					["Graphics/Bat/BatHurt 2.png", 24, 30, 0.04],
					["Graphics/Bat/BatHurt 1.png", 24, 30, 0.04],
				],
			},
			{
				"Name": "Bat Shadow",
				"AnimType": AnimSingle,
				"States": [eStates.shadow],
				"Frames":
					[
						["Graphics/shadow.png", 16, 4, 0.3],
					],
			},
			]
		}

class BatController(Controller):

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
			self.facing = eDirections.left

	def __init__(self, game, data):
		super(BatController, self).__init__(game)

	def update(self, data, common_data, dt):
		speed = 0.3
		# if doing something that can't be interrupted then countdown to end of it

		if self.coolDown(data, dt):
			pass
		else:
			if data.health <= 0:
				self.setState(data, common_data, eStates.dead)
				return
			self.setState(data, common_data, eStates.stationary)
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
					data.facing = eDirections.left
				else:
#					self.setState(data, common_data, eStates.runRight)
					data.vel = Vec3(speed, 0, 0)
					data.facing = eDirections.right
				if(target.y<common_data.pos.y):
					data.vel.y = -speed
				else:
					data.vel.y = speed

				if common_data.pos.distSq(Vec3(target.x,target.y,common_data.pos.z))<800:
					data.vel.z = 0 # drop on target
				elif (common_data.pos.z<80) and (data.vel.z<3):
					data.vel.z += 2 # otherwise flap
					common_data.entity.graphics.startAnim(data = common_data.entity.graphics_data)
					common_data.entity.sounds.playEvent(data, common_data, eEvents.flap)

				data.cooldown = 0.2

		if common_data.pos.z>0:
			friction(data.vel, 0.01)
		else:
			friction(data.vel, 0.1)

		basic_gravity(data.vel)
		basic_physics(common_data.pos,data.vel)

		restrictToArena(common_data.pos, data.vel)



	def receiveCollision(self, data, common_data, message):
		if message:
			# if message.source.common_data.name !="Reaper":
			# 	log("Reaper hit by " + message.source.common_data.name)
			data.vel += message.force/data.mass
			if message.damage>0 and data.health>0:
				hurt_cool = 1
				fall_cool = 3
				data.health -= message.damage
				if data.facing == eDirections.left:
					if data.health <= 0:
						self.setState(data, common_data, eStates.fallLeft, fall_cool)
						common_data.game.reportMonsterDeath()
					else:
						self.setState(data, common_data, eStates.hurtLeft, hurt_cool)
				else:
					if data.health <= 0:
						self.setState(data, common_data, eStates.fallRight, fall_cool)
						common_data.game.reportMonsterDeath()
					else:
						self.setState(data, common_data, eStates.hurtRight, hurt_cool)

class BatCollider(Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.dim = Vec3(20,8,16)
			self.orig = Vec3(10,4,0)

	def __init__(self, game, data):
		super(BatCollider, self).__init__(game)
		# global static data to all of BatCollider components
		self.radius = 10.0
		self.damage = 1.0

	def getRadius(self):
		return self.radius

	def getCollisionMessage(self, data, common_data):
		return(Message(source=common_data.entity, damage=0, damage_hero=1))






