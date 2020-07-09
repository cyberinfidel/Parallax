# system
import enum

# Parallax
from entity import eStates, eDirections
from game_pad import eActions
from controller import Controller, global_tolerance, restrictToArena, global_gravity
from collision import Collider, Message
from graphics import AnimNoLoop, AnimLoop, MultiAnim, AnimSingle
from vector import Vec3
import sound

# Knightfight
from strike import Strike, HitController, HitCollider


class eStrikes(enum.IntEnum):
	big = 0
	big_up = 1
	small = 2
	block = 3
	push = 4
	num_strikes = 5

class eEvents(enum.IntEnum):
	jump = 0
	num_events = 1

def heroSounds(mixer):
	return {
		"Name": "Hero Sounds",
		"Template": sound.MultiSound,
		"Mixer": mixer,
		"StateSounds": [
		],
		"EventSounds":
			[
				{
					"Name": "Jump",
					"Type": sound.Single,
					"Events": [eEvents.jump],
					"Samples":  # one of these will play at random if there's more than one
						[
							"Sounds/Hero/jump.wav"
						]
				}

			]
	}

def heroGraphics(renlayer):
	return {
		"Name": "Hero Animations",
		"Template": MultiAnim,
		"RenderLayer": renlayer,
		"Anims": [
			{
				"Name": "Hero Stands",
				"AnimType": AnimLoop,
				"States": [eStates.stationary],
				"Frames":
					[
						["Graphics/Hero/Hero.png", 16, 36, 2.0],
						["Graphics/Hero/HeroBlink.png", 16, 36, 0.5],
					]
			},
			{
				"Name": "Hero Runs Down",
				"AnimType": AnimLoop,
				"States": [eStates.runDown],
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
				"States": [eStates.runUp],
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
				"States": [eStates.runLeft],
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
				"States": [eStates.runRight],
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
				"States": [eStates.jumpRight],
				"Frames":
					[
						["Graphics/Hero/HeroRunR1.png", 16, 39, 0.1],
						["Graphics/Hero/HeroJumpR.png", 16, 39, 10.1],
					],
			},
			{
				"Name": "Hero Jumps Left",
				"AnimType": AnimNoLoop,
				"States": [eStates.jumpLeft],
				"Frames":
					[
						["Graphics/Hero/HeroRunL1.png", 16, 39, 0.1],
						["Graphics/Hero/HeroJumpL.png", 16, 39, 10.1],
					],
			},
			{
				"Name": "Hero Jumps Up",
				"AnimType": AnimNoLoop,
				"States": [eStates.jumpUp],
				"Frames":
					[
						["Graphics/Hero/HeroRunU1.png", 16, 39, 0.1],
						["Graphics/Hero/HeroJumpU.png", 16, 39, 10.1],
					],
			},
			{
				"Name": "Hero Jumps Down",
				"AnimType": AnimNoLoop,
				"States": [eStates.jumpDown, eStates.jumpStat],
				"Frames":
					[
						["Graphics/Hero/HeroRunD1.png", 16, 39, 0.1],
						["Graphics/Hero/HeroJumpD.png", 16, 39, 10.1],
					],
			},
			{
				"Name": "Hero Blocks Right",
				"AnimType": AnimNoLoop,
				"States": [eStates.blockRight],
				"Frames":
					[
						["Graphics/Hero/HeroStandR.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBlockR 1.png", 24, 39, 0.1],
					],
			},
			{
				"Name": "Hero Blocks Left",
				"AnimType": AnimNoLoop,
				"States": [eStates.blockLeft],
				"Frames":
					[
						["Graphics/Hero/HeroStandL.png", 48, 47, 0.1],
						["Graphics/Hero/HeroBlockL 1.png", 24, 39, 0.1],
					],
			},
			{
				"Name": "Hero Big Attack Right",
				"AnimType": AnimNoLoop,
				"States": [eStates.attackBigRight],
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
				"States": [eStates.attackSmallRight],
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
				"States": [eStates.attackSmallLeft],
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
				"States": [eStates.attackBigLeft],
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
				"States": [eStates.fallLeft],
				"Frames":
					[
						["Graphics/Hero/HeroFallL 1.png", 18, 47, 0.3],
						["Graphics/Hero/HeroFallL 2.png", 20, 40, 1.0],
					],
			},
			{
				"Name": "Hero Fall Right",
				"AnimType": AnimNoLoop,
				"States": [eStates.fallRight],
				"Frames":
					[
						["Graphics/Hero/HeroFallR 1.png", 18, 47, 0.3],
						["Graphics/Hero/HeroFallR 2.png", 20, 40, 1.0],
					],
			},
			{
				"Name": "Hero Shadow",
				"AnimType": AnimSingle,
				"States": [eStates.shadow],
				"Frames":
					[
						["Graphics/shadow.png", 16, 4, 0.3],
					],
			},
			{
				"Name": "Hero hurt Left",
				"AnimType": AnimNoLoop,
				"States": [eStates.hurtLeft],
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
				"States": [eStates.hurtRight],
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
	def __init__(self, game, data):
		super(HeroController, self).__init__(game)
		# values global to all instances
		self.invincible_states = (eStates.dead, eStates.fallLeft, eStates.fallRight)

		# set up all attacks
		hit_controller = self.game.controller_manager.makeTemplate({"Template": HitController})
		hit_collider = self.game.collision_manager.makeTemplate({"Template": HitCollider})
		hit_t = self.game.entity_manager.makeEntityTemplate(graphics=False,
																												controller=hit_controller,
																												collider=hit_collider)

		# cool downs in seconds
		self.strikes = [
			#			cool	del		range					dimension				origin			force		damage
			Strike(cool=0.8, delay=0.6, duration = 0.2, range=Vec3(24, 0, 0), dim=Vec3(10,8,12), orig=Vec3(5,4,6),
						 force=3, absorb=0, damage=2, template=hit_t, hero_damage=0),  # big
			Strike(cool=0.8, delay=0.4, duration = 0.2, range=Vec3(8, 10, 30), dim=Vec3(12,8,8), orig=Vec3(6,4,4),
						 force=3, absorb=0, damage=2, template=hit_t),  # big_up
			Strike(cool=0.3, delay=0.2, duration = 0.2, range=Vec3(12, 0, 0), dim=Vec3(10,8,8), orig=Vec3(5,4,4),
						 force=1, absorb=0, damage=1, template=hit_t),  # small
			Strike(cool=0.8, delay=0.6, duration = 0.5, range=Vec3(16, 0, 0), dim=Vec3(10,16,30), orig=Vec3(5,8,20),
						 force=0.2, absorb=100, damage=0, template=hit_t),  # block
			Strike(cool=0.8, delay=0.7, duration=0.1, range=Vec3(20, 0, 0), dim=Vec3(10, 16, 30), orig=Vec3(5, 8, 20),
						 force=3, absorb=100, damage=0, template=hit_t),  # push
		]

		# sounds





	################
	# end __init__ #
	################

	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				self.game_pad = init.game_pad
			else:
				self.game_pad = False

			# values for each instance

			self.cooldown = -1
			self.vel = Vec3(0.0,0.0,0.0)
			self.mass = 1
			self.jump = False
			self.attack = False
			self.facing = eDirections.down
			self.health = 3
			common_data.state = eStates.standDown
			self.invincible_cooldown = 2
			self.invincible = self.invincible_cooldown

			self.hero_struck=[]
			for s in range(0,eStrikes.num_strikes):
				self.hero_struck.append(False)

	#####################
	# end data __init__ #
	#####################


	def strike(self, data, common_data,
						 strike,
						 flippedX=False,
							):
		strike_ent = self.game.requestNewEntity(entity_template=strike.template,
																							 pos=common_data.pos +(strike.range.flippedX() if flippedX else strike.range),
																							 parent=common_data.entity,
																							 name="Hero strike")
		strike_ent.collider_data.force = Vec3(-strike.force if flippedX else strike.force,0,0)
		strike_ent.collider_data.absorb = strike.absorb
		strike_ent.collider_data.damage = strike.damage
		strike_ent.collider_data.dim = strike.dim
		strike_ent.collider_data.orig = strike.orig
		strike_ent.controller_data.cooldown = strike.duration


	def update(self, data, common_data, dt):
		hero_speed = 1.5
		hero_jump_speed = 3.0
		hero_stop = 0.05
		hero_friction_ground = 0.1
		hero_friction_air = 0.05


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

			# check if something needs to happen during an action

			# do strikes
			if common_data.state not in [eStates.dead, eStates.fallLeft, eStates.fallRight, eStates.hurtLeft, eStates.hurtRight]:
				for index, str in enumerate(self.strikes):
					# TODO: check if this really is a strike
					if data.hero_struck[index]:
						if data.cooldown<str.delay:
								self.strike(data, common_data,
														strike= str,
														flippedX = (data.facing==eDirections.left)
														)
								data.hero_struck[index] = False

		else:

			if data.health < 0:
				self.setState(data, common_data, eStates.dead)
				common_data.blink=True
				return

			# for s in range(1,eStrikes.num_strikes):
			# 	data.hero_struck[s]=False
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
					data.facing = eDirections.left
					if data.jump:
						self.updateState(data, common_data, eStates.jumpLeft, hero_jump_cool)
					else:
						self.updateState(data, common_data, eStates.runLeft, hero_run_cool)

				# going right
				elif data.game_pad.actions[eActions.right]:
					data.facing = eDirections.right
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
						# play jump sound
						common_data.entity.sounds.playEvent(data, common_data, eEvents.jump)


				# attacks and block
				if data.game_pad.actions[eActions.attack_big]:
					# big attack
					if data.jump:
						pass
					else:
						data.hero_struck[eStrikes.big]=True
						data.hero_struck[eStrikes.big_up]=True
						if data.facing == eDirections.left:
							self.updateState(data, common_data, eStates.attackBigLeft, self.strikes[eStrikes.big].cool)
						else:
							self.updateState(data, common_data, eStates.attackBigRight, self.strikes[eStrikes.big].cool)
				elif data.game_pad.actions[eActions.attack_small]:
					# small attack
					if data.jump:
						pass
					else:
						data.hero_struck[eStrikes.small]=True
						if data.facing == eDirections.left:
							self.updateState(data, common_data, eStates.attackSmallLeft, self.strikes[eStrikes.small].cool)
						else:
							self.updateState(data, common_data, eStates.attackSmallRight, self.strikes[eStrikes.small].cool)

				elif data.game_pad.actions[eActions.block]:
					# block
					if data.jump:
						pass
					else:
						data.hero_struck[eStrikes.block]=True
						data.hero_struck[eStrikes.push]=True
						if data.facing == eDirections.left:
							self.updateState(data, common_data, eStates.blockLeft, self.strikes[eStrikes.block].cool)
						else:
							self.updateState(data, common_data, eStates.blockRight, self.strikes[eStrikes.block].cool)


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
					fall_cool = 3
					if data.facing == eDirections.left:
						data.vel += Vec3(3,0,0)
						if data.health <= 0:
							self.setState(data, common_data, eStates.fallLeft, fall_cool)
							data.health =-1
						else:
							self.setState(data, common_data, eStates.hurtLeft, hurt_cool)

					else:
						data.vel += Vec3(-3,0,0)
						if data.health <= 0:
							self.setState(data, common_data, eStates.fallRight, fall_cool)
							data.health =-1
						else:
							self.setState(data, common_data, eStates.hurtRight, hurt_cool)
					data.invincible = data.invincible_cooldown

class HeroCollider(Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.dim = Vec3(14,8,30)
			self.orig = Vec3(7,4,15)

	def __init__(self, game, data):
		super(HeroCollider, self).__init__(game)
		# global static data to all of HeroCollider components
		self.radius = 10.0
		self.mass = 10.0

	def getRadius(self):
		return self.radius

	def getCollisionMessage(self, data, common_data):
		return(Message(source=common_data.entity, absorb=3))


