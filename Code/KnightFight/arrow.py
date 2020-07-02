from entity import eStates, eDirections
from vector import Vec3
from controller import Controller, basic_gravity, basic_physics, restrictToArena, friction
from collision import Collider, Message
from graphics import MultiAnim, AnimSingle

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
						["Graphics/Arrow/ArrowLeft.png", 11, 3, 0.04],
					],
			},
			{
				"Name": "Arrow fall right",
				"AnimType": AnimSingle,
				"States": [eStates.fallRight, eStates.runRight],
				"Frames":
					[
						["Graphics/Arrow/ArrowRight.png", 11, 3, 0.04],
					],
			},
			{
				"Name": "Arrow Shadow",
				"AnimType": AnimSingle,
				"States": [eStates.shadow],
				"Frames":
					[
						["Graphics/shadowSmall.png", 16, 4, 0.3],
					],
			},
				]
	}

class AController(Controller):

	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.cooldown = -1
			self.health = 5
			self.vel = Vec3(0,0,0)
			self.mass = 0.5
			self.facing = eDirections.left

	def __init__(self, game, data):
		super(AController, self).__init__(game)

	def update(self, data, common_data, dt):

		data.facing = eDirections.left if data.vel.x<0 else eDirections.right

		if common_data.state==eStates.fallLeft or common_data.state==eStates.fallRight:
			if not self.coolDown(data,dt):
				self.setState(data, common_data, eStates.dead)
			friction(data.vel, 0.1)
		elif common_data.pos.z>0:
			friction(data.vel, 0.01)
		else:
			self.setState(data,common_data,eStates.fallLeft if data.facing==eDirections.left else eStates.fallRight)
			data.cooldown=1
			friction(data.vel, 0.1)


		basic_gravity(data.vel)
		basic_physics(common_data.pos,data.vel)

		restrictToArena(common_data.pos, data.vel)



	def receiveCollision(self, data, common_data, message):
		if message:
			if not (common_data.state == eStates.fallRight or common_data.state == eStates.fallLeft):
				# if message.source.common_data.name !="Reaper":
				# 	log("Reaper hit by " + message.source.common_data.name)
				data.vel += message.force/data.mass

class ACollider(Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.dim = Vec3(20,8,16)
			self.orig = Vec3(10,4,0)

	def __init__(self, game, data):
		super(ACollider, self).__init__(game)
		# global static data to all of BatCollider components

	def getCollisionMessage(self, data, common_data):
		if common_data.state==eStates.fallRight or common_data.state==eStates.fallLeft or common_data.state==eStates.dead:
			return False
		else:
			return(Message(source=common_data.entity, damage=1, damage_hero=1))