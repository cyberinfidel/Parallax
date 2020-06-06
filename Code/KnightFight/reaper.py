# Reaper
from controller import *
from collision import *
from graphics import *

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
			self.health = 50
			self.vel = Vec3(0,0,0)

			common_data.state = eStates.stationary
			common_data.new_state = False

	def __init__(self, data):
		super(ReaperController, self).__init__()

	def update(self, data, common_data, dt):
		speed = 0.2
		# if doing something that can't be interrupted then countdown to end of it
		if not self.coolDown(data, dt):
			if rand_num(10)==0:
				self.setState(data, common_data, eStates.stationary)
				data.vel = Vec3(0,0,0)
				data.cooldown = rand_num(1) + 2
			elif common_data.state==eStates.stationary:
				if rand_num(1)==0:
					self.setState(data,common_data, eStates.runLeft)
				else:
					self.setState(data,common_data, eStates.runRight)

			if common_data.state==eStates.runRight:
				if rand_num(10)==0:
					# turn
					self.setState(data, common_data, eStates.runLeft)
					data.vel = Vec3(-speed, 0, 0)
				else:
					data.vel = Vec3(speed, 0, 0)
				data.cooldown = 0.5
			elif common_data.state == eStates.runLeft:
				if rand_num(10) == 0:
					# turn
					self.setState(data, common_data, eStates.runRight)
					data.vel = Vec3(speed, 0, 0)
				else:
					data.vel = Vec3(-speed, 0, 0)
				data.cooldown = 0.5

		basic_physics(common_data.pos,data.vel)

		restrictToArena(common_data.pos, data.vel)

		friction(data.vel)

	def receiveCollision(self, data, common_data, message=False):
#		log("Reaper hit " +common_data.name)
		if message:
			if message.source.common_data.name=="reaper":
				log("Reaper hit reaper")


class ReaperCollider(Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

	def __init__(self, data):
		super(ReaperCollider, self).__init__()
		# global static data to all of ReaperCollider components
		self.radius = 10.0
		self.damage = 1
		self.dim = Vec3(20,8,16)
		self.orig = Vec3(10,4,0)

	def getRadius(self):
		return self.radius

	def getCollisionMessage(self, data, common_data):
		return(Message(source=common_data.entity,damage=0,damage_hero=1))

