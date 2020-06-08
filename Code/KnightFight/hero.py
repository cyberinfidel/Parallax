from controller import *
from collision import *
from graphics import *


def heroGraphics(renlayer):
	return {
		"Name": "Hero Animations",
		"Template": MultiAnim,
		"RenderLayer": renlayer,
		"Anims": [
			{
				"Name": "Hero Stands",
				"AnimType": AnimLoop,
				"State": eStates.stationary,
				"Frames":
					[
						["Graphics/Hero/Hero.png", 16, 36, 2.0],
						["Graphics/Hero/HeroBlink.png", 16, 36, 0.5],
					]
			},
			{
				"Name": "Hero Runs Down",
				"AnimType": AnimLoop,
				"State": eStates.runDown,
				"Frames":
					[
						["Graphics/Hero/HeroRunD1.png", 16, 39, 0.1],
						["Graphics/Hero/HeroRunD2.png", 16, 39, 0.1],
						["Graphics/Hero/HeroRunD3.png", 16, 39, 0.1],
						["Graphics/Hero/HeroRunD4.png", 16, 39, 0.1],
					],
			},
			{
				"Name": "Hero Runs Up",
				"AnimType": AnimLoop,
				"State": eStates.runUp,
				"Frames":
					[
						["Graphics/Hero/HeroRunU1.png", 16, 39, 0.1],
						["Graphics/Hero/HeroRunU2.png", 16, 39, 0.1],
						["Graphics/Hero/HeroRunU3.png", 16, 39, 0.1],
						["Graphics/Hero/HeroRunU4.png", 16, 39, 0.1],
					],
			},
			{
				"Name": "Hero Runs Left",
				"AnimType": AnimLoop,
				"State": eStates.runLeft,
				"Frames":
					[
						["Graphics/Hero/HeroRunL1.png", 16, 39, 0.1],
						["Graphics/Hero/HeroRunL2.png", 16, 39, 0.05],
						["Graphics/Hero/HeroRunL3.png", 16, 39, 0.1],
						["Graphics/Hero/HeroRunL4.png", 16, 39, 0.1],
					],
			},
			{
				"Name": "Hero Runs Right",
				"AnimType": AnimLoop,
				"State": eStates.runRight,
				"Frames":
					[
						["Graphics/Hero/HeroRunR1.png", 16, 39, 0.1],
						["Graphics/Hero/HeroRunR2.png", 16, 39, 0.05],
						["Graphics/Hero/HeroRunR3.png", 16, 39, 0.1],
						["Graphics/Hero/HeroRunR4.png", 16, 39, 0.1],
					],
			},
			{
				"Name": "Hero Jumps Right",
				"AnimType": AnimNoLoop,
				"State": eStates.jumpRight,
				"Frames":
					[
						["Graphics/Hero/HeroRunR1.png", 16, 39, 0.1],
						["Graphics/Hero/HeroJumpR.png", 16, 39, 10.1],
					],
			},
			{
				"Name": "Hero Jumps Left",
				"AnimType": AnimNoLoop,
				"State": eStates.jumpLeft,
				"Frames":
					[
						["Graphics/Hero/HeroRunL1.png", 16, 39, 0.1],
						["Graphics/Hero/HeroJumpL.png", 16, 39, 10.1],
					],
			},
			{
				"Name": "Hero Jumps Up",
				"AnimType": AnimNoLoop,
				"State": eStates.jumpUp,
				"Frames":
					[
						["Graphics/Hero/HeroRunU1.png", 16, 39, 0.1],
						["Graphics/Hero/HeroJumpU.png", 16, 39, 10.1],
					],
			},
			{
				"Name": "Hero Jumps Down",
				"AnimType": AnimNoLoop,
				"State": eStates.jumpDown,
				"Frames":
					[
						["Graphics/Hero/HeroRunD1.png", 16, 39, 0.1],
						["Graphics/Hero/HeroJumpD.png", 16, 39, 10.1],
					],
			},
			{
				"Name": "Hero Jumps Stationary",
				"AnimType": AnimNoLoop,
				"State": eStates.jumpStat,
				"Frames":
					[
						["Graphics/Hero/HeroRunD1.png", 16, 39, 0.1],
						["Graphics/Hero/HeroJumpD.png", 16, 39, 10.1],
					],
			},
			{
				"Name": "Hero Blocks Right",
				"AnimType": AnimNoLoop,
				"State": eStates.blockRight,
				"Frames":
					[
						["Graphics/Hero/HeroStandR.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBlockR 1.png", 24, 39, 0.1],
					],
			},
			{
				"Name": "Hero Blocks Left",
				"AnimType": AnimNoLoop,
				"State": eStates.blockLeft,
				"Frames":
					[
						["Graphics/Hero/HeroStandL.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBlockL 1.png", 24, 39, 0.1],
					],
			},
			{
				"Name": "Hero Big Attack Right",
				"AnimType": AnimNoLoop,
				"State": eStates.attackBigRight,
				"Frames":
					[
						["Graphics/Hero/HeroBigAttack 2.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBigAttack 3.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBigAttack 4.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBigAttack 5.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBigAttack 6.png", 48, 47, 0.05],
						["Graphics/Hero/HeroBigAttack 7.png", 48, 47, 0.05],
						["Graphics/Hero/HeroBigAttack 8.png", 48, 47, 0.05],
						["Graphics/Hero/HeroBigAttack 9.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBigAttack 10.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBigAttack 11.png", 48, 47, 0.1],
					],
			},
			{
				"Name": "Hero Small Attack Right",
				"AnimType": AnimNoLoop,
				"State": eStates.attackSmallRight,
				"Frames":
					[
						["Graphics/Hero/HeroSmallAttackR 2.png", 21, 40, 0.05],
						["Graphics/Hero/HeroSmallAttackR 3.png", 21, 40, 0.05],
						["Graphics/Hero/HeroSmallAttackR 4.png", 21, 40, 0.05],
						["Graphics/Hero/HeroSmallAttackR 5.png", 21, 40, 0.05],
						["Graphics/Hero/HeroSmallAttackR 6.png", 21, 40, 0.05],
						["Graphics/Hero/HeroSmallAttackR 7.png", 21, 40, 0.05],
						["Graphics/Hero/HeroSmallAttackR 8.png", 21, 40, 0.05],
						["Graphics/Hero/HeroSmallAttackR 9.png", 21, 40, 0.1],
					],
			},
			{
				"Name": "Hero Small Attack Left",
				"AnimType": AnimNoLoop,
				"State": eStates.attackSmallLeft,
				"Frames":
					[
						["Graphics/Hero/HeroSmallAttackL 2.png", 21, 40, 0.05],
						["Graphics/Hero/HeroSmallAttackL 3.png", 21, 40, 0.05],
						["Graphics/Hero/HeroSmallAttackL 4.png", 21, 40, 0.05],
						["Graphics/Hero/HeroSmallAttackL 5.png", 21, 40, 0.05],
						["Graphics/Hero/HeroSmallAttackL 6.png", 21, 40, 0.05],
						["Graphics/Hero/HeroSmallAttackL 7.png", 21, 40, 0.05],
						["Graphics/Hero/HeroSmallAttackL 8.png", 21, 40, 0.05],
						["Graphics/Hero/HeroSmallAttackL 9.png", 21, 40, 0.1],
					],
			},
			{
				"Name": "Hero Big Attack Left",
				"AnimType": AnimNoLoop,
				"State": eStates.attackBigLeft,
				"Frames":
					[
						["Graphics/Hero/HeroBigAttackL2.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBigAttackL3.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBigAttackL4.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBigAttackL5.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBigAttackL6.png", 48, 47, 0.05],
						["Graphics/Hero/HeroBigAttackL7.png", 48, 47, 0.05],
						["Graphics/Hero/HeroBigAttackL8.png", 48, 47, 0.05],
						["Graphics/Hero/HeroBigAttackL9.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBigAttackL10.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBigAttackL11.png", 48, 47, 0.1],
					],
			},
			{
				"Name": "Hero Fall Left",
				"AnimType": AnimNoLoop,
				"State": eStates.fallLeft,
				"Frames":
					[
						["Graphics/Hero/HeroFallL 1.png", 18, 47, 0.3],
						["Graphics/Hero/HeroFallL 2.png", 20, 40, 1.0],
					],
			},
			{
				"Name": "Hero Fall Right",
				"AnimType": AnimNoLoop,
				"State": eStates.fallRight,
				"Frames":
					[
						["Graphics/Hero/HeroFallR 1.png", 18, 47, 0.3],
						["Graphics/Hero/HeroFallR 2.png", 20, 40, 1.0],
					],
			},
			{
				"Name": "Hero Shadow",
				"AnimType": AnimSingle,
				"State": eStates.shadow,
				"Frames":
					[
						["Graphics/shadow.png", 16, 4, 0.3],
					],
			},
			{
				"Name": "Hero hurt Left",
				"AnimType": AnimNoLoop,
				"State": eStates.hurtLeft,
				"Frames":
					[
						["Graphics/Hero/HeroStandL.png", 48, 47, 0.1],
						["Graphics/Hero/HeroFallL 1.png", 18, 47, 0.3],
						["Graphics/Hero/HeroBlockL 1.png", 24, 39, 0.1],
					],
			},
			{
				"Name": "Hero hurt Right",
				"AnimType": AnimNoLoop,
				"State": eStates.hurtRight,
				"Frames":
					[
						["Graphics/Hero/HeroStandR.png", 48, 47, 0.1],
						["Graphics/Hero/HeroFallR 1.png", 18, 47, 0.3],
						["Graphics/Hero/HeroBlockR 1.png", 24, 39, 0.1],
					],
			},
		]

	}


class HeroController(Controller):
	def __init__(self, data):
		super(HeroController, self).__init__()
		# values global to all heroes
		self.invincible_states = (eStates.dead, eStates.fallLeft, eStates.fallRight, eStates.dead)

		self.state_spawns = {}	# holds the templates that can be spawned from different hero states e.g. eStates.attackBigLeft makes the big attack entity

	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				self.game_pad = init.game_pad
			else:
				self.game_pad = False

			self.cooldown = -1
			self.vel = Vec3(0.0,0.0,0.0)
			self.mass = 1
			self.jump = False
			self.attack = False
			self.facing = Directions.down
			self.health = 3
			common_data.state = eStates.standDown
			self.invincible_cooldown = 2
			self.invincible = self.invincible_cooldown

	def strike(self, data, common_data,
						 range,
						 force,
							damage,
						 name
							):
		strike = common_data.game.requestNewEntity(entity_template=self.state_spawns[common_data.state],
																							 pos=common_data.pos +Vec3(range,0,0), parent=common_data.entity,
																							 name=name)
		strike.collider_data.force = Vec3(force,0,0)
		strike.collider_data.damage = damage
		data.hero_struck = True

	def update(self, data, common_data, dt):
		# get input
		hero_speed = 1.5
		hero_jump_speed = 3.0
		hero_stop = 0.05
		hero_friction_ground = 0.1
		hero_friction_air = 0.05

		# cool downs in seconds
		hero_big_attack_cool = 0.8
		hero_big_attack_delay = 0.2	# note delays are when strike happens
		hero_big_attack_force = 5
		hero_big_attack_damage = 1
		hero_big_attack_range = 24
		hero_small_attack_cool = 0.3
		hero_small_attack_delay = 0.1
		hero_small_attack_force = 1
		hero_small_attack_damage = 0.3
		hero_small_attack_range = 12
		hero_block_cool = 0.3
		hero_block_delay = 0.2
		hero_block_force = 4
		hero_block_damage = 0
		hero_block_range = 10
		hero_run_cool = 0
		hero_jump_cool = -1

		# flags

		# things that can interrupt other actions happen here e.g. landing


		if data.invincible > 0:
			common_data.blink = (int(data.invincible*8)%2)==0
			data.invincible -= dt
		else:
			common_data.blink=False

		# ground vs in the air
		if common_data.pos.z < 0.0 + global_tolerance:
			# we're on the ground guys
			common_data.pos.z = 0.0
			data.vel.z = 0.0
			data.jump = False
		else:
			data.vel.z -= global_gravity

		# deal with things that can't interrupt actions that are already happening

		if self.coolDown(data, dt):
			# cooling down so can't do anything new
			if data.health < 0:
				self.setState(data, common_data, eStates.dead)
				return

			# check if something needs to happen during an action
			if data.cooldown<hero_big_attack_delay:
				if not data.hero_struck:
					if common_data.state == eStates.attackBigLeft:
						self.strike(data, common_data,
												range=-hero_big_attack_range,
												force=-hero_big_attack_force,
												damage=hero_big_attack_damage,
												name="Big Hit Left"
												)
					elif common_data.state==eStates.attackBigRight:
						self.strike(data, common_data,
												range=hero_big_attack_range,
												force=hero_big_attack_force,
												damage=hero_big_attack_damage,
												name="Big Hit Right"
												)

			if data.cooldown < hero_small_attack_delay:
				if not data.hero_struck:
					if common_data.state == eStates.attackSmallLeft:
						self.strike(data, common_data,
												range=-hero_small_attack_range,
												force=-hero_small_attack_force,
												damage=hero_small_attack_damage,
												name="Small Hit Left"
												)
					elif common_data.state == eStates.attackSmallRight:
						self.strike(data, common_data,
												range=hero_small_attack_range,
												force=hero_small_attack_force,
												damage=hero_small_attack_damage,
												name="Small Hit Right"
												)

			if data.cooldown < hero_block_delay:
				if not data.hero_struck:
					if common_data.state == eStates.blockLeft:
						self.strike(data, common_data,
												range=-hero_block_range,
												force=-hero_block_force,
												damage=hero_block_damage,
												name="Block Left"
												)
					elif common_data.state == eStates.blockRight:
						self.strike(data, common_data,
												range=hero_block_range,
												force=hero_block_force,
												damage=hero_block_damage,
												name="Block Right"
												)


		else:
			data.hero_struck=False
			# not doing anything that's cooling down so can do something else
			if data.vel.magsqhoriz() < hero_stop:
				# stopped so react automatically - most likely idle, but only if stationary
				if data.jump:
					self.updateState(data, common_data, eStates.jumpStat)
				else:
					self.updateState(data, common_data, eStates.stationary)

			# get input and set up an action
			if data.game_pad:
				# i.e. this hero is being controlled by a game_pad
				# going left
				if data.game_pad.actions[eActions.left]:
					data.facing = Directions.left
					if data.jump:
						self.updateState(data, common_data, eStates.jumpLeft, hero_jump_cool)
					else:
						self.updateState(data, common_data, eStates.runLeft, hero_run_cool)

				# going right
				elif data.game_pad.actions[eActions.right]:
					data.facing = Directions.right
					if data.jump:
						self.updateState(data, common_data, eStates.jumpRight, hero_jump_cool)
					else:
						self.updateState(data, common_data, eStates.runRight, hero_run_cool)

				# going up
				elif data.game_pad.actions[eActions.up]:
					if data.jump:
						self.updateState(data, common_data, eStates.jumpUp, hero_jump_cool)
					else:
						self.updateState(data, common_data, eStates.runUp, hero_run_cool)


				# going down
				elif data.game_pad.actions[eActions.down]:
					if data.jump:
						self.updateState(data, common_data, eStates.jumpDown, hero_jump_cool)
					else:
						self.updateState(data, common_data, eStates.runDown, hero_run_cool)

				if data.game_pad.actions[eActions.left]:
					data.vel.x = -hero_speed
				# going right
				elif data.game_pad.actions[eActions.right]:
						data.vel.x = hero_speed

				# going up
				if data.game_pad.actions[eActions.up]:
					data.vel.y = hero_speed
				# going down
				elif data.game_pad.actions[eActions.down]:
					data.vel.y = -hero_speed

				# deal with jump button
				if data.game_pad.actions[eActions.jump]:
					if data.jump:
						pass
					else:
						data.jump = True
						data.vel.z += hero_jump_speed

				# attacks and block
				if data.game_pad.actions[eActions.attack_big]:
					# big attack
					if data.jump:
						pass
					else:
						if data.facing == Directions.left:
							self.updateState(data, common_data, eStates.attackBigLeft, hero_big_attack_cool)
						else:
							self.updateState(data, common_data, eStates.attackBigRight, hero_big_attack_cool)
				elif data.game_pad.actions[eActions.attack_small]:
					# small attack
					if data.jump:
						pass
					else:
						if data.facing == Directions.left:
							self.updateState(data, common_data, eStates.attackSmallLeft, hero_small_attack_cool)
						else:
							self.updateState(data, common_data, eStates.attackSmallRight, hero_small_attack_cool)

				elif data.game_pad.actions[eActions.block]:
					# block
					if data.jump:
						pass
					else:
						if data.facing == Directions.left:
							self.updateState(data, common_data, eStates.blockLeft, hero_block_cool)
						else:
							self.updateState(data, common_data, eStates.blockRight, hero_block_cool)


		# "physics"
		if data.jump:
			common_data.pos+=data.vel
			data.vel.friction(hero_friction_air)
		elif data.vel.magsq() > hero_stop:
			common_data.pos+=data.vel
			data.vel.friction(hero_friction_ground)
		else:
			# not jumping or moving fast enough so properly stop
			data.vel = Vec3(0.0,0.0,0.0)

		restrictToArena(common_data.pos, data.vel)

	def receiveCollision(self, data, common_data, message=False):
		# log("Hero hit: "+message["name"])
		if message:
			if(message.damage_hero>0):
				data.vel += message.force / data.mass
				if (common_data.state not in self.invincible_states
					and not data.invincible>0):
					# hero has been hit
					data.health-=message.damage_hero
					hurt_cool = 1
					fall_cool = 5
					if data.facing == Directions.left:
						data.vel += Vec3(3,0,0)
						if data.health <= 0:
							self.setState(data, common_data, eStates.fallLeft, fall_cool)
						else:
							self.setState(data, common_data, eStates.hurtLeft, hurt_cool)

					else:
						data.vel += Vec3(-3,0,0)
						if data.health <= 0:
							self.setState(data, common_data, eStates.fallRight, fall_cool)
						else:
							self.setState(data, common_data, eStates.hurtRight, hurt_cool)
					data.invincible = data.invincible_cooldown

	def setStateSpawnTemplate(self, state, template):
		self.state_spawns[state]=template

class HeroCollider(Collider):

	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

	def __init__(self, data):
		super(HeroCollider, self).__init__()
		# global static data to all of HeroCollider components
		self.radius = 10.0
		self.mass = 10.0
		self.dim = Vec3(20,8,16)
		self.orig = Vec3(10,4,0)

	def getRadius(self):
		return self.radius

	def getCollisionMessage(self, data, common_data):
		return(Message(source=common_data.entity))


###########
# Strikes #
###########

class HitController(Controller):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

			self.cooldown = 0.5

	def __init__(self, data):
		super(HitController, self).__init__()

	def update(self, data, common_data, dt):

		if not self.coolDown(data, dt):
			# finished big hit - otherwise just hang around
			common_data.state = eStates.dead

	def receiveCollision(self, data, common_data, message=False):
		# if a hit hits then it lasts only for the remainder of that tick
		# this avoids hitting the same thing multiple times
		# common_data.state = eStates.dead

		# otherwise the damage would need to be spread over multiple ticks
		# The more ticks that the hit collides with an object th emore damage
		# if you just tickle it, then you don't do much damageb
		pass

class HitCollider(Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

	def __init__(self, data):
		super(HitCollider, self).__init__()
		# global static data to all of components
		self.dim = Vec3(20,8,16)
		self.orig = Vec3(10,4,0)

	def getCollisionMessage(self, data, common_data):
		return(Message(source=common_data.entity, damage=data.damage, force=data.force))

