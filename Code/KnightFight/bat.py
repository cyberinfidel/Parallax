from controller import *
from collision import *
from graphics import *

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
				"State": eStates.stationary,
				"Frames":
					[
						["Graphics/Bat/Bat1.png", 24, 30, 0.5],
						["Graphics/Bat/Bat2.png", 24, 30, 0.04],
						["Graphics/Bat/Bat3.png", 24, 30, 0.04],
						["Graphics/Bat/Bat4.png", 24, 30, 0.1],
						["Graphics/Bat/Bat3.png", 24, 30, 0.1],
						["Graphics/Bat/Bat2.png", 24, 30, 0.1],
					],
			},
			{
				"Name": "Simple Fall Left",
				"AnimType": AnimLoop,
				"State": eStates.fallLeft,
				"Frames":
					[
						["Graphics/Bat/Bat3.png", 24, 30, 0.04],
					],
			},
			{
				"Name": "Simple Fall Right",
				"AnimType": AnimLoop,
				"State": eStates.fallRight,
				"Frames":
					[
						["Graphics/Bat/Bat3.png", 24, 30, 0.04],
					],
			},
			{
				"Name": "Simple Hurt Left",
				"AnimType": AnimLoop,
				"State": eStates.hurtLeft,
				"Frames":
					[
						["Graphics/Bat/Bat3.png", 24, 30, 0.04],
					],
			},
			{
				"Name": "Simple HurtRight",
				"AnimType": AnimLoop,
				"State": eStates.hurtRight,
				"Frames":
					[
						["Graphics/Bat/Bat3.png", 24, 30, 0.04],
					],
			},
			{
				"Name": "Bat Shadow",
				"AnimType": AnimSingle,
				"State": eStates.shadow,
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
			self.mass = 2

	def __init__(self, data):
		super(BatController, self).__init__()

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
				data.cooldown = rand_num(1) + 2
			else:
				# chase hero
				target = common_data.game.requestTarget(common_data.pos)
				if(target.x<common_data.pos.x):
#					self.setState(data, common_data, eStates.runLeft)
					data.vel = Vec3(-speed, 0, 0)
					data.facing = Directions.left
				else:
#					self.setState(data, common_data, eStates.runRight)
					data.vel = Vec3(speed, 0, 0)
					data.facing = Directions.right
				if(target.y<common_data.pos.y):
					data.vel.y = -speed
				else:
					data.vel.y = speed

				if common_data.pos.distSq(Vec3(target.x,target.y,common_data.pos.z))<1000:
					data.vel.z = -2
				elif common_data.pos.z<(40):
					data.vel.z = 1

				data.cooldown = 0.5


		basic_physics(common_data.pos,data.vel)

		restrictToArena(common_data.pos, data.vel)

		if common_data.pos.z>0:
			friction(data.vel, 0.01)
		else:
			friction(data.vel)


	def receiveCollision(self, data, common_data, message):
		if message:
			# if message.source.common_data.name !="Reaper":
			# 	log("Reaper hit by " + message.source.common_data.name)
			data.vel += message.force/data.mass
			if message.damage>0:
				hurt_cool = 1
				fall_cool = 2
				data.health -= message.damage
				if data.facing == Directions.left:
					if data.health <= 0:
						self.setState(data, common_data, eStates.fallLeft, fall_cool)
					else:
						self.setState(data, common_data, eStates.hurtLeft, hurt_cool)
				else:
					if data.health <= 0:
						self.setState(data, common_data, eStates.fallRight, fall_cool)
					else:
						self.setState(data, common_data, eStates.hurtRight, hurt_cool)

class BatCollider(Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

	def __init__(self, data):
		super(BatCollider, self).__init__()
		# global static data to all of BatCollider components
		self.radius = 10.0
		self.damage = 1.0
		self.dim = Vec3(20,8,16)
		self.orig = Vec3(10,4,0)

	def getRadius(self):
		return self.radius

	def getCollisionMessage(self, data, common_data):
		return(Message(source=common_data.entity, damage=0, damage_hero=1))






