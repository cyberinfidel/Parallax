import enum

from entity import eStates, eDirections
from vector import Vec3, rand_num
import controller
import collision
from graphics import AnimLoop, AnimNoLoop, MultiAnim, AnimSingle
import sound
from background import restrictToArena

class eEvents(enum.IntEnum):
	flap = 0
	num_events = 1



def makeGraphics(manager, renlayer):
	return manager.makeTemplate({
			"Name": "Butterfly",
			"Template": MultiAnim,
			"RenderLayer": renlayer,
			"Anims":
				[
			{
				"Name": "Butterfly Flapping",
				"AnimType": AnimLoop,
				"States": [eStates.stationary],
				"Frames":
					[
						["Graphics/Butterfly/Butterfly 2.png", 8, 0, 15, 0.04],
						["Graphics/Butterfly/Butterfly 3.png", 8, 0, 15, 0.04],
						["Graphics/Butterfly/Butterfly 4.png", 8, 0, 15, 0.1],
						["Graphics/Butterfly/Butterfly 3.png", 8, 0, 15, 0.1],
						["Graphics/Butterfly/Butterfly 2.png", 8, 0, 15, 0.1],
						["Graphics/Butterfly/Butterfly 1.png", 8, 0, 15, 0.5],
					],
			},
			{
				"Name": "Butterfly Shadow",
				"AnimType": AnimSingle,
				"States": [eStates.shadow],
				"Frames":
					[
						["Graphics/shadowSmall.png", 16, 0, 4, 0.3],
					],
			},
			]
		})

def makeGraphics2(manager, renlayer):
	return manager.makeTemplate({
			"Name": "Butterfly",
			"Template": MultiAnim,
			"RenderLayer": renlayer,
			"Anims":
				[
			{
				"Name": "Butterfly Flapping",
				"AnimType": AnimLoop,
				"States": [eStates.stationary],
				"Frames":
					[
						["Graphics/Butterfly2/Butterfly 2.png", 8, 0, 15, 0.04],
						["Graphics/Butterfly2/Butterfly 3.png", 8, 0, 15, 0.04],
						["Graphics/Butterfly2/Butterfly 4.png", 8, 0, 15, 0.1],
						["Graphics/Butterfly2/Butterfly 3.png", 8, 0, 15, 0.1],
						["Graphics/Butterfly2/Butterfly 2.png", 8, 0, 15, 0.1],
						["Graphics/Butterfly2/Butterfly 1.png", 8, 0, 15, 0.5],
					],
			},
			{
				"Name": "Butterfly Shadow",
				"AnimType": AnimSingle,
				"States": [eStates.shadow],
				"Frames":
					[
						["Graphics/shadowSmall.png", 16, 0,  4, 0.3],
					],
			},
			]
		})

def makeGraphics3(manager, renlayer):
	return manager.makeTemplate({
			"Name": "Butterfly",
			"Template": MultiAnim,
			"RenderLayer": renlayer,
			"Anims":
				[
			{
				"Name": "Butterfly Flapping",
				"AnimType": AnimLoop,
				"States": [eStates.stationary],
				"Frames":
					[
						["Graphics/Butterfly3/Butterfly 2.png", 8, 0, 15, 0.04],
						["Graphics/Butterfly3/Butterfly 3.png", 8, 0, 15, 0.04],
						["Graphics/Butterfly3/Butterfly 4.png", 8, 0, 15, 0.1],
						["Graphics/Butterfly3/Butterfly 3.png", 8, 0, 15, 0.1],
						["Graphics/Butterfly3/Butterfly 2.png", 8, 0, 15, 0.1],
						["Graphics/Butterfly3/Butterfly 1.png", 8, 0, 15, 0.5],
					],
			},
			{
				"Name": "Butterfly Shadow",
				"AnimType": AnimSingle,
				"States": [eStates.shadow],
				"Frames":
					[
						["Graphics/shadowSmall.png", 16, 0, 4, 0.3],
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
			self.cooldown = 0
			self.health = 5
			self.vel = Vec3(0,0,0)
			self.mass = 4
			self.facing = eDirections.left
			self.target_cool=0

	def __init__(self, game, data):
		super(Controller, self).__init__(game)

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
				data.cooldown = rand_num(5)/8.0+0.3
			else:
				# chase hero
				if data.target_cool<=0:
					data.target = Vec3(rand_num(600), rand_num(200),rand_num(200))
					data.target_cool = rand_num(20)
				else:
					data.target_cool-=1
				if(data.target.x<common_data.pos.x):
#					self.setState(data, common_data, eStates.runLeft)
					data.vel = Vec3(-speed, 0, 0)
					data.facing = eDirections.left
				else:
#					self.setState(data, common_data, eStates.runRight)
					data.vel = Vec3(speed, 0, 0)
					data.facing = eDirections.right
				if(data. target.y<common_data.pos.y):
					data.vel.y = -speed
				else:
					data.vel.y = speed

				if common_data.pos.distSq(Vec3(data.target.x,data.target.y,common_data.pos.z))<800:
					data.vel.z = 0 # drop on target
				elif (common_data.pos.z<80+rand_num(200)) and (data.vel.z<3):
					data.vel.z += 2+rand_num(5) # otherwise flap
					common_data.entity.graphics.startAnim(data = common_data.entity.graphics_data)

				data.cooldown = 0.2

		if common_data.pos.z>0:
			controller.friction(data.vel, 0.01)
		else:
			controller.friction(data.vel, 0.1)

		controller.basic_gravity(data.vel)
		controller.basic_physics(common_data.pos,data.vel)

		restrictToArena(common_data.pos, data.vel)




