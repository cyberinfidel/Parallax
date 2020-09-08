import px_entity
from vector import Vec3, rand_num
import controller
import collision
import graphics
import background
import arrow

def makeGraphics(manager, renlayer):
	return manager.makeTemplate({
			"Name": "Goblin Archer",
			"Template": graphics.MultiAnim,
			"RenderLayer": renlayer,
			"Anims":
				[
			{
				"Name": "Firing Arrow",
				"AnimType": graphics.AnimLoop,
				"States": [px_entity.eStates.attackSmallLeft],
				"Frames":
					[
						["Graphics/GoblinArcher/GoblinArcher 08.png", 22, 36, 0, 0.1],
						["Graphics/GoblinArcher/GoblinArcher 09.png", 22, 36, 0, 0.1],
						["Graphics/GoblinArcher/GoblinArcher 10.png", 22, 36, 0, 0.1],
						["Graphics/GoblinArcher/GoblinArcher 01.png", 22, 36, 0, 0.2],
						["Graphics/GoblinArcher/GoblinArcher 02.png", 22, 36, 0, 0.2],
						["Graphics/GoblinArcher/GoblinArcher 03.png", 22, 36, 0, 0.1],
						["Graphics/GoblinArcher/GoblinArcher 04.png", 22, 36, 0, 0.1],
						["Graphics/GoblinArcher/GoblinArcher 05.png", 22, 36, 0, 0.1],
						["Graphics/GoblinArcher/GoblinArcher 06.png", 22, 36, 0, 0.2],
						["Graphics/GoblinArcher/GoblinArcher 07.png", 22, 36, 0, 0.2],
					],
			},
			{
				"Name": "Firing Arrow",
				"AnimType": graphics.AnimLoop,
				"States": [px_entity.eStates.attackSmallRight],
				"Frames":
					[
						["Graphics/GoblinArcher/Right/GoblinArcher 08.png", 22, 36, 0, 0.1],
						["Graphics/GoblinArcher/Right/GoblinArcher 09.png", 22, 36, 0, 0.1],
						["Graphics/GoblinArcher/Right/GoblinArcher 10.png", 22, 36, 0, 0.1],
						["Graphics/GoblinArcher/Right/GoblinArcher 01.png", 22, 36, 0, 0.2],
						["Graphics/GoblinArcher/Right/GoblinArcher 02.png", 22, 36, 0, 0.2],
						["Graphics/GoblinArcher/Right/GoblinArcher 03.png", 22, 36, 0, 0.1],
						["Graphics/GoblinArcher/Right/GoblinArcher 04.png", 22, 36, 0, 0.1],
						["Graphics/GoblinArcher/Right/GoblinArcher 05.png", 22, 36, 0, 0.1],
						["Graphics/GoblinArcher/Right/GoblinArcher 06.png", 22, 36, 0, 0.2],
						["Graphics/GoblinArcher/Right/GoblinArcher 07.png", 22, 36, 0, 0.2],
					],
			},
			{
				"Name": "Standing",
				"AnimType": graphics.AnimLoop,
				"States": [px_entity.eStates.stationary],
				"Frames":
					[
						["Graphics/GoblinArcher/GoblinArcher 08.png", 22, 36, 0, 0.04],
					],
			},
			{
				"Name": "Standing",
				"AnimType": graphics.AnimLoop,
				"States": [px_entity.eStates.standLeft],
				"Frames":
					[
						["Graphics/GoblinArcher/GoblinArcher 08.png", 22, 36, 0, 0.04],
					],
			},
			{
				"Name": "Standing",
				"AnimType": graphics.AnimLoop,
				"States": [px_entity.eStates.standRight],
				"Frames":
					[
						["Graphics/GoblinArcher/Right/GoblinArcher 08.png", 22, 36, 0, 0.04],
					],
			},
			{
				"Name": "Simple Fall Left",
				"AnimType": graphics.AnimNoLoop,
				"States": [px_entity.eStates.fallLeft],
				"Frames":
					[
						["Graphics/GoblinArcher/GoblinArcherDies 1.png", 22, 36, 0, 0.5],
						["Graphics/GoblinArcher/GoblinArcherDies 2.png", 22, 36, 0, 0.5],
					],
			},
			{
				"Name": "Simple Fall Right",
				"AnimType": graphics.AnimNoLoop,
				"States": [px_entity.eStates.fallRight],
				"Frames":
					[
						["Graphics/GoblinArcher/Right/GoblinArcherDies 1.png", 22, 36, 0, 0.5],
						["Graphics/GoblinArcher/Right/GoblinArcherDies 2.png", 22, 36, 0, 0.5],
					],
			},
			{
				"Name": "Simple Hurt Left",
				"AnimType": graphics.AnimLoop,
				"States": [px_entity.eStates.hurtLeft],
				"Frames":
					[
						["Graphics/GoblinArcher/GoblinArcherDies 1.png", 22, 36, 0, 0.5],
					],
			},
			{
				"Name": "Simple HurtRight",
				"AnimType": graphics.AnimLoop,
				"States": [px_entity.eStates.hurtRight],
				"Frames":
					[
						["Graphics/GoblinArcher/Right/GoblinArcherDies 1.png", 22, 36, 0, 0.5],
					],
			},
			{
				"Name": "Goblin Archer Shadow",
				"AnimType": graphics.AnimSingle,
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
			self.facingleft = True
			self.fired = False

	def __init__(self, game, data):
		super(Controller, self).__init__(game)
		# values global to all instances
		self.invincible_states = (px_entity.eStates.dead, px_entity.eStates.fallLeft, px_entity.eStates.fallRight)

		arrow_controller = self.game.controller_manager.makeTemplate({"Template": arrow.Controller})
		arrow_collider = self.game.collision_manager.makeTemplate({"Template": arrow.Collider})
		arrow_graphics = self.game.graphics_manager.makeTemplate(arrow.AGraphics(self.game.renlayer))

		self.arrow_t = self.game.entity_manager.makeEntityTemplate(graphics=arrow_graphics, controller=arrow_controller,collider=arrow_collider)


	def shoot(self, data, common_data,
						 flippedX=False,
							):
		arrow = self.game.requestNewEntity(entity_template=self.arrow_t,
																							 pos=common_data.pos+Vec3(-5 if flippedX else 5,20,0),
																							 parent=common_data.entity,
																							 name="Goblin archer arrow")
		arrow.collider_data.force = 0#Vec3(-1 if flippedX else 1,0,0)
		arrow.collider_data.hero_damage = 1
		arrow.common_data.state = (px_entity.eStates.runLeft if flippedX else px_entity.eStates.runRight)
		arrow.controller_data.vel = Vec3(-7 if flippedX else 7,1,0)

	def update(self, data, common_data, dt):

		fire_cool = 1.4

		if self.coolDown(data, dt):
			if data.fired and (common_data.state not in [px_entity.eStates.fallLeft, px_entity.eStates.fallRight, px_entity.eStates.dead]):
				if data.cooldown<0.9:
					self.shoot(data,common_data,data.facingleft)
					data.fired = False
		else:
			if data.health <= 0:
				self.setState(data, common_data, px_entity.eStates.dead)
				return
			# fire at hero if in range
			target = common_data.game.requestTarget(common_data.pos)
			data.facingleft = (target.x<common_data.pos.x)
			if abs(target.x-common_data.pos.x)<200 and abs(target.z-common_data.pos.z)<20:
				self.setState(data, common_data, px_entity.eStates.attackSmallLeft if data.facingleft else px_entity.eStates.attackSmallRight)
				data.fired = True
				data.cooldown = fire_cool
			else:
				self.setState(data, common_data, px_entity.eStates.standLeft if data.facingleft else px_entity.eStates.standRight)
				data.cooldown = rand_num(1) + 2

		controller.friction(data.vel)
		controller.basic_gravity(data.vel)
		controller.basic_physics(common_data.pos,data.vel)
		background.restrictToArena(common_data.pos, data.vel)



	def receiveCollision(self, this_entity, message):
		data = this_entity.controller_data
		common_data = this_entity.common_data
		if message:
			# if message.source.common_data.name !="Reaper":
			# 	log("Reaper hit by " + message.source.common_data.name)
			data.vel += message.force/data.mass
			# don't get shot by own arrows
			if not message.source.common_data.parent is common_data.entity:
				if message.damage>0 and data.health>0:
					hurt_cool = 1
					fall_cool = 2
					data.health -= message.damage
					if data.facingleft:
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
class Collider(collision.Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.dim = Vec3(20,16,8)
			self.orig = Vec3(10,0,4)
			self.damage = 1.0
			self.damage_hero=1
			self.force = Vec3(0,0,0)

	def __init__(self, game, data):
		super(Collider, self).__init__(game)
		# global static data to all of BatCollider components
		self.radius = 10.0

	def getCollisionMessage(self, data, common_data):
		return(collision.Message(source=common_data.entity, damage=0, damage_hero=1))



