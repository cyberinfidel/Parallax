# Reaper
from controller import Controller, basic_physics, restrictToArena, friction
from collision import Collider, Message
from graphics import MultiAnim, AnimLoop, AnimSingle
from entity import eDirections, eStates
from vector import Vec3, rand_num

def reaperGraphics(renlayer):
	return {
			"Name": "Reaper",
			"Template": MultiAnim,
			"RenderLayer": renlayer,
			"Anims": [
				{
					"Name": "Simple Reaper Stationary",
					"AnimType": AnimLoop,
					"State": eStates.stationary,
					"Frames":
						[
							["Graphics/Reaper/ReaperR1.png", 16, 38, 0.1],
						],
				},
				{
				"Name": "Simple Reaper Shuffling Left",
				"AnimType": AnimLoop,
				"State":eStates.runLeft,
				"Frames":
					[
						["Graphics/Reaper/ReaperRunL01.png", 16, 38, 0.1],
						["Graphics/Reaper/ReaperRunL02.png", 16, 38, 0.1],
						["Graphics/Reaper/ReaperRunL03.png", 16, 38, 0.1],
						["Graphics/Reaper/ReaperRunL04.png", 16, 38, 0.1],
						["Graphics/Reaper/ReaperRunL05.png", 16, 38, 0.1],
						["Graphics/Reaper/ReaperRunL06.png", 16, 38, 0.1],
						["Graphics/Reaper/ReaperRunL07.png", 16, 38, 0.1],
						["Graphics/Reaper/ReaperRunL08.png", 16, 38, 0.1],
						["Graphics/Reaper/ReaperRunL09.png", 16, 38, 0.1],
						["Graphics/Reaper/ReaperRunL10.png", 16, 38, 0.1],
						["Graphics/Reaper/ReaperRunL11.png", 16, 38, 0.1],
						["Graphics/Reaper/ReaperRunL12.png", 16, 38, 0.1],
					],
			},
				{
					"Name": "Simple Reaper Shuffling Right",
					"AnimType": AnimLoop,
					"State": eStates.runRight,
					"Frames":
						[
							["Graphics/Reaper/ReaperRunR01.png", 16, 38, 0.1],
							["Graphics/Reaper/ReaperRunR02.png", 16, 38, 0.1],
							["Graphics/Reaper/ReaperRunR03.png", 16, 38, 0.1],
							["Graphics/Reaper/ReaperRunR04.png", 16, 38, 0.1],
							["Graphics/Reaper/ReaperRunR05.png", 16, 38, 0.1],
							["Graphics/Reaper/ReaperRunR06.png", 16, 38, 0.1],
							["Graphics/Reaper/ReaperRunR07.png", 16, 38, 0.1],
							["Graphics/Reaper/ReaperRunR08.png", 16, 38, 0.1],
							["Graphics/Reaper/ReaperRunR09.png", 16, 38, 0.1],
							["Graphics/Reaper/ReaperRunR10.png", 16, 38, 0.1],
							["Graphics/Reaper/ReaperRunR11.png", 16, 38, 0.1],
							["Graphics/Reaper/ReaperRunR12.png", 16, 38, 0.1],
						],
				},
				{
					"Name": "Reaper Hurt L",
					"AnimType": AnimLoop,
					"State": eStates.hurtLeft,
					"Frames":
						[
							["Graphics/Reaper/ReaperL3.png", 16, 38, 0.3],
						],
				},
				{
					"Name": "Reaper Hurt R",
					"AnimType": AnimLoop,
					"State": eStates.hurtRight,
					"Frames":
						[
							["Graphics/Reaper/ReaperR3.png", 16, 38, 0.3],
						],
				},
				{
					"Name": "Reaper Fall L",
					"AnimType": AnimLoop,
					"State": eStates.fallLeft,
					"Frames":
						[
							["Graphics/Reaper/ReaperFallL.png", 24, 24, 0.3],
						],
				},
				{
					"Name": "Reaper Fall R",
					"AnimType": AnimLoop,
					"State": eStates.fallRight,
					"Frames":
						[
							["Graphics/Reaper/ReaperFallR.png", 24, 24, 0.3],
						],
				},
				{
					"Name": "Reaper Shadow",
					"AnimType": AnimSingle,
					"State": eStates.shadow,
					"Frames":
						[
							["Graphics/shadow.png", 16, 4, 0.3],
						],
				},
			]
		}


class ReaperController(Controller):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

			self.cooldown = -1
			self.health = 10
			self.vel = Vec3(0, 0, 0)
			self.mass = 3
			self.facing = eDirections.right

			common_data.state = eStates.stationary
			common_data.new_state = False

	def __init__(self, game, data):
		super(ReaperController, self).__init__(game)

	def update(self, data, common_data, dt):
		speed = 0.3
		# if doing something that can't be interrupted then countdown to end of it

		if self.coolDown(data, dt):
			pass
		else:
			if data.health <= 0:
				self.setState(data, common_data, eStates.dead)
				return
			if rand_num(10)==0:
				self.setState(data, common_data, eStates.stationary)
				data.vel = Vec3(0,0,0)
				data.cooldown = rand_num(1) + 2
			else:
				# chase hero
				target = common_data.game.requestTarget(common_data.pos)
				if(target.x<common_data.pos.x):
					self.setState(data, common_data, eStates.runLeft)
					data.vel = Vec3(-speed, 0, 0)
					data.facing = eDirections.left
				else:
					self.setState(data, common_data, eStates.runRight)
					data.vel = Vec3(speed, 0, 0)
					data.facing = eDirections.right
				if(target.y<common_data.pos.y):
					data.vel.y = -speed
				else:
					data.vel.y = speed

				data.cooldown = 0.5

		friction(data.vel)

		basic_physics(common_data.pos,data.vel)

		restrictToArena(common_data.pos, data.vel)


	def receiveCollision(self, data, common_data, message=False):
#		log("Reaper hit " +common_data.name)
		if message:
			# if message.source.common_data.name !="Reaper":
			# 	log("Reaper hit by " + message.source.common_data.name)
			data.vel += message.force/data.mass
			if message.damage>0 and data.health>0:
				hurt_cool = 1
				fall_cool = 2
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


class ReaperCollider(Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.dim = Vec3(20,10,16)
			self.orig = Vec3(10,2,0)

	def __init__(self, game, data):
		super(ReaperCollider, self).__init__(game)
		# global static data to all of ReaperCollider components
		self.radius = 10.0
		self.damage = 1

	def getRadius(self):
		return self.radius

	def getCollisionMessage(self, data, common_data):
		if common_data.entity.controller_data.health>0:
			return(Message(source=common_data.entity,damage=0,damage_hero=1, force=Vec3(0,0,0)))
		else:
		 	return(Message(source=common_data.entity))


