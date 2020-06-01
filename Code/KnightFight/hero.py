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
						["Graphics/Hero/HeroBlockR 1.png", 16, 39, 0.1],
					],
			},
			{
				"Name": "Hero Blocks Left",
				"AnimType": AnimNoLoop,
				"State": eStates.blockLeft,
				"Frames":
					[
						["Graphics/Hero/HeroStandL.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBlockL 1.png", 16, 39, 0.1],
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
						["Graphics/Hero/HeroFallL 2.png", 18, 47, 1.0],
					],
			},
			{
				"Name": "Hero Fall Right",
				"AnimType": AnimNoLoop,
				"State": eStates.fallRight,
				"Frames":
					[
						["Graphics/Hero/HeroFallR 1.png", 18, 47, 0.3],
						["Graphics/Hero/HeroFallR 2.png", 18, 47, 1.0],
					],
			},
		]

	}


class HeroController(Controller):
	def __init__(self, data):
		super(HeroController, self).__init__()
		# values global to all heroes
		self.invincible_states = (eStates.dead, eStates.fallLeft, eStates.fallRight, eStates.dead)

	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				self.game_pad = init.game_pad
			else:
				self.game_pad = False

			self.cooldown = -1
			self.vel = Vec3(0.0,0.0,0.0)
			self.jump = False
			self.attack = False
			self.facing = Directions.down
			self.health = 5
			common_data.state = eStates.standDown
			self.invincible_cooldown = 2
			self.invincible = self.invincible_cooldown

	def update(self, data, common_data, dt):
		# get input
		hero_speed = 1.5
		hero_jump_speed = 3.0
		hero_stop = 0.05
		hero_friction_ground = 0.1
		hero_friction_air = 0.05

		# cool downs in seconds
		hero_big_attack_cool = 0.8
		hero_small_attack_cool = 0.3
		hero_block_cool = 0.3
		hero_run_cool = 0
		hero_jump_cool = -1
		hero_stand_cool = 0

		# things that can interrupt other actions happen here e.g. landing

		if data.health<0:
			data.health = -1
			log("Dead!")
			return

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
			pass
		else:
			if data.invincible > 0:
				common_data.blink = (int(data.invincible*16)%2)==0
				data.invincible -= dt
			else:
				common_data.blink=False
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
		hero_fall_cool = 2
		# log("Hero hit: "+message["name"])
		if message:
			if(message["damage_hero"]>0
				and common_data.state not in self.invincible_states
				and not data.invincible>0):
				if data.facing == Directions.left:
					self.updateState(data, common_data, eStates.fallLeft, hero_fall_cool)
				else:
					self.updateState(data, common_data, eStates.fallRight, hero_fall_cool)
				data.invincible = data.invincible_cooldown



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

	def getRadius(self):
		return self.radius

	def getCollisionMessage(self, data, common_data):
		message={"name":"hero", "damage":0}
		return(message)





