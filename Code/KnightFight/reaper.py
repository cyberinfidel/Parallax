# Reaper
import controller
import collision
import graphics
import entity
from vector import Vec3, rand_num

def makeGraphics(manager, renlayer):
	return manager.makeTemplate({
			"Name": "Reaper",
			"Template": graphics.MultiAnim,
			"RenderLayer": renlayer,
			"Anims": [
				{
					"Name": "Simple Reaper Stationary",
					"AnimType": graphics.AnimLoop,
					"States": [entity.eStates.stationary],
					"Frames":
						[
							["Graphics/Reaper/ReaperR1.png", 16, 38, 0.1],
						],
				},
				{
				"Name": "Simple Reaper Shuffling Left",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runLeft],
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
					"AnimType": graphics.AnimLoop,
					"States": [entity.eStates.runRight],
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
					"AnimType": graphics.AnimLoop,
					"States": [entity.eStates.hurtLeft],
					"Frames":
						[
							["Graphics/Reaper/ReaperL3.png", 16, 38, 0.3],
						],
				},
				{
					"Name": "Reaper Hurt R",
					"AnimType": graphics.AnimLoop,
					"States": [entity.eStates.hurtRight],
					"Frames":
						[
							["Graphics/Reaper/ReaperR3.png", 16, 38, 0.3],
						],
				},
				{
					"Name": "Reaper Fall L",
					"AnimType": graphics.AnimLoop,
					"States": [entity.eStates.fallLeft],
					"Frames":
						[
							["Graphics/Reaper/ReaperFallL.png", 24, 24, 0.3],
						],
				},
				{
					"Name": "Reaper Fall R",
					"AnimType": graphics.AnimLoop,
					"States": [entity.eStates.fallRight],
					"Frames":
						[
							["Graphics/Reaper/ReaperFallR.png", 24, 24, 0.3],
						],
				},
				{
					"Name": "Reaper Shadow",
					"AnimType": graphics.AnimSingle,
					"States": [entity.eStates.shadow],
					"Frames":
						[
							["Graphics/shadow.png", 16, 4, 0.3],
						],
				},
			]
		})


def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(controller.Controller):
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
			self.facing = entity.eDirections.right

			common_data.state = entity.eStates.stationary
			common_data.new_state = False

	def __init__(self, game, data):
		super(Controller, self).__init__(game)

	def update(self, data, common_data, dt):
		speed = 0.3
		# if doing something that can't be interrupted then countdown to end of it

		if self.coolDown(data, dt):
			pass
		else:
			if data.health <= 0:
				self.setState(data, common_data, entity.eStates.dead)
				return
			if rand_num(10)==0:
				self.setState(data, common_data, entity.eStates.stationary)
				data.vel = Vec3(0,0,0)
				data.cooldown = rand_num(1) + 2
			else:
				# chase hero
				target = common_data.game.requestTarget(common_data.pos)
				if(target.x<common_data.pos.x):
					self.setState(data, common_data, entity.eStates.runLeft)
					data.vel = Vec3(-speed, 0, 0)
					data.facing = entity.eDirections.left
				else:
					self.setState(data, common_data, entity.eStates.runRight)
					data.vel = Vec3(speed, 0, 0)
					data.facing = entity.eDirections.right
				if(target.y<common_data.pos.y):
					data.vel.y = -speed
				else:
					data.vel.y = speed

				data.cooldown = 0.5

		controller.friction(data.vel)
		controller.basic_physics(common_data.pos,data.vel)
		controller.restrictToArena(common_data.pos, data.vel)


	def receiveCollision(self, this_entity, message=False):
#		log("Reaper hit " +common_data.name)
		data = this_entity.controller_data
		common_data = this_entity.common_data

		if message:
			# if message.source.common_data.name !="Reaper":
			# 	log("Reaper hit by " + message.source.common_data.name)
			data.vel += message.force/data.mass
			if message.damage>0 and data.health>0:
				hurt_cool = 1
				fall_cool = 2
				data.health -= message.damage
				if data.facing == entity.eDirections.left:
					if data.health <= 0:
						self.setState(data, common_data, entity.eStates.fallLeft, fall_cool)
						common_data.game.reportMonsterDeath()
					else:
						self.setState(data, common_data, entity.eStates.hurtLeft, hurt_cool)
				else:
					if data.health <= 0:
						self.setState(data, common_data, entity.eStates.fallRight, fall_cool)
						common_data.game.reportMonsterDeath()
					else:
						self.setState(data, common_data, entity.eStates.hurtRight, hurt_cool)
			# todo change damage_hero to 0 in collider on death

def makeCollider(manager):
	return manager.makeTemplate({"Template": Collider})
class Collider(collision.Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.dim = Vec3(20,10,16)
			self.orig = Vec3(10,2,0)
			self.damage_hero=1


	def __init__(self, game, data):
		super(Collider, self).__init__(game)
		# global static data to all of ReaperCollider components
		self.radius = 10.0
		self.damage_hero = 1

	def getCollisionMessage(self, data, common_data):
		if common_data.entity.controller_data.health > 0:
			return (collision.Message(source=common_data.entity, damage=0, damage_hero=1, force=Vec3(0, 0, 0)))
		else:
			return (collision.Message(source=common_data.entity))