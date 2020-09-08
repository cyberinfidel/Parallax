from px_entity import eStates, eDirections
from vector import Vec3
import controller
import collision
from graphics import MultiAnim, AnimSingle
import background

#########
# Arrow #
#########

def AGraphics(renlayer):
	return {
			"Name": "Arrow",
			"Template": MultiAnim,
			"RenderLayer": renlayer,
			"Anims":
				[
			{
				"Name": "Arrow",
				"AnimType": AnimSingle,
				"States": [eStates.stationary,eStates.runLeft,eStates.fallLeft],
				"Frames":
					[
						["Graphics/Arrow/ArrowLeft.png", 11, 3, 0, 0.04],
					],
			},
			{
				"Name": "Arrow fall right",
				"AnimType": AnimSingle,
				"States": [eStates.fallRight, eStates.runRight],
				"Frames":
					[
						["Graphics/Arrow/ArrowRight.png", 11, 3, 0, 0.04],
					],
			},
			{
				"Name": "Arrow Shadow",
				"AnimType": AnimSingle,
				"States": [eStates.shadow],
				"Frames":
					[
						["Graphics/shadowSmall.png", 16, 4, 0, 0.3],
					],
			},
				]
	}

class Controller(controller.Controller):

	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.cooldown = -1
			self.health = 5
			self.vel = Vec3(0,0,0)
			self.mass = 2
			self.facing = eDirections.left

	def __init__(self, game, data):
		super(Controller, self).__init__(game)

	def update(self, data, common_data, dt):

		data.facing = eDirections.left if data.vel.x<0 else eDirections.right

		if common_data.state==eStates.fallLeft or common_data.state==eStates.fallRight:
			if not self.coolDown(data,dt):
				self.setState(data, common_data, eStates.dead)
			controller.friction(data.vel, 0.1)
		elif common_data.pos.y>0:
			controller.friction(data.vel, 0.01)
		else:
			self.setState(data,common_data,eStates.fallLeft if data.facing==eDirections.left else eStates.fallRight)
			data.cooldown=1
			controller.friction(data.vel, 0.1)


		controller.basic_gravity(data.vel)
		controller.basic_physics(common_data.pos,data.vel)

		background.restrictToArena(common_data.pos, data.vel)



	def receiveCollision(self, this_entity, message):
		data = this_entity.controller_data
		common_data = this_entity.common_data
		if message:
			if not (common_data.state == eStates.fallRight or common_data.state == eStates.fallLeft):
				# if message.source.common_data.name !="Reaper":
				# 	log("Reaper hit by " + message.source.common_data.name)
				if message.absorb>2:
					data.vel = Vec3(0,0,0)+ message.force/data.mass
				else:
					data.vel = data.vel + message.force/data.mass

class Collider(collision.Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.dim = Vec3(10,16,8)
			self.orig = Vec3(5,8,4)

	def __init__(self, game, data):
		super(Collider, self).__init__(game)
		# global static data to all of BatCollider components

	def getCollisionMessage(self, data, common_data):
		if common_data.state==eStates.fallRight or common_data.state==eStates.fallLeft or common_data.state==eStates.dead:
			return False
		else:
			dam = 1 if common_data.entity.controller_data.vel.magsq()>10 else 0
			return(collision.Message(source=common_data.entity, damage=dam, damage_hero=dam))