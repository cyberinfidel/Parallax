# system
import enum

# Parallax
from entity import eStates
from game_pad import eActions
import controller
import collision
from graphics import AnimNoLoop, AnimLoop, MultiAnim, AnimSingle
from vector import Vec3
import background
import sound
from vector import rand_num

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

def sounds(mixer):
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

def graphics(renlayer):
	return {
		"Name": "Bunny Animations",
		"Template": MultiAnim,
		"RenderLayer": renlayer,
		"Anims": [
			{
				"Name": "Bunny Stands",
				"AnimType": AnimLoop,
				"States": [eStates.stationary, eStates.standRight],
				"Frames":
					[
						["Graphics/Macaroon/RunFast_000.png", 20, 36, 0.015],
					]
			},
			{
				"Name": "Bunny Stands",
				"AnimType": AnimLoop,
				"States": [eStates.standLeft],
				"Frames":
					[
						["Graphics/Macaroon/Left/RunFast_000.png", 20, 36, 0.015],
					]
			},
			{
				"Name": "Hero Runs Left",
				"AnimType": AnimLoop,
				"States": [eStates.runLeft],
				"Frames":
					[
						["Graphics/Macaroon/Left/RunFast_000.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_001.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_002.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_003.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_004.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_005.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_006.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_007.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_008.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_009.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_010.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_011.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_012.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_013.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_014.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_015.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_016.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_017.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_018.png", 20, 36, 0.01],
						["Graphics/Macaroon/Left/RunFast_019.png", 20, 36, 0.01],
					],
			},
			{
				"Name": "Hero Runs Right",
				"AnimType": AnimLoop,
				"States": [eStates.runRight, eStates.runUp, eStates.runDown],
				"Frames":
					[
						["Graphics/Macaroon/RunFast_000.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_001.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_002.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_003.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_004.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_005.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_006.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_007.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_008.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_009.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_010.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_011.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_012.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_013.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_014.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_015.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_016.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_017.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_018.png", 20, 36, 0.01],
						["Graphics/Macaroon/RunFast_019.png", 20, 36, 0.01],
					],
			},
			{
				"Name": "Hero Small Attack Right",
				"AnimType": AnimNoLoop,
				"States": [eStates.attackSmallRight],
				"Frames":
					[
						["Graphics/Macaroon/RunFast_000.png", 20, 36, 0.015],
					],
			},
			{
				"Name": "Hero Small Attack Left",
				"AnimType": AnimNoLoop,
				"States": [eStates.attackSmallLeft],
				"Frames":
					[
						["Graphics/Macaroon/Left/RunFast_000.png", 20, 36, 0.015],
					],
			},
			{
				"Name": "Bunny Jump Left",
				"AnimType": AnimLoop,
				"States": [eStates.jumpLeft],
				"Frames":
					[
						["Graphics/Macaroon/Left/RunFast_000.png", 20, 36, 0.015],
					],
			},
			{
				"Name": "Bunny Jump Right",
				"AnimType": AnimLoop,
				"States": [eStates.jumpRight],
				"Frames":
					[
						["Graphics/Macaroon/RunFast_000.png", 20, 36, 0.015],
					],
			},
			{
				"Name": "Bunny Shadow",
				"AnimType": AnimSingle,
				"States": [eStates.shadow],
				"Frames":
					[
						["Graphics/shadow.png", 16, 4, 0.3],
					],
			},
		]

	}


class Controller(controller.Controller):
	def __init__(self, game, data):
		super(Controller, self).__init__(game)
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
			Strike(cool=1.5, delay=0.2, duration = 0.2, range=Vec3(25, 0, 0), dim=Vec3(30,16,16), orig=Vec3(5,4,4),
						 force=1, absorb=0, damage=1, template=hit_t),  # small
			Strike(cool=1.5, delay=0.6, duration = 0.5, range=Vec3(16, 0, 0), dim=Vec3(10,16,30), orig=Vec3(5,8,20),
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
			self.jump = True
			self.attack = False
			self.facingleft = True
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
		hero_speed = 4 #6
		hero_speed_while_jumping = 2
		hero_jump_speed = 6.0
		hero_stop = 5
		hero_friction_ground = 0.075
		hero_friction_air = 0.05


		hero_run_cool = 0.0
		hero_jump_cool = -1

		# flags

		# things that can interrupt other actions happen here e.g. landing


		# ground vs in the air

		# find out how far we are above something
		#height = common_data.game.getDistanceBelow(common_data.pos)


		if common_data.pos.z < 0.0 + controller.global_tolerance:
			# we're on the ground guys
			common_data.pos.z = 0.0
			data.vel.z = 0.0
			data.jump = False
		else:
			data.vel.z -= controller.global_gravity

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
														flippedX = (data.facingleft)
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
				self.updateState(data, common_data, eStates.standLeft if data.facingleft else eStates.standRight)
			else:
				# todo add skidding
				pass

			# get input and set up an action
			if data.game_pad:
				# i.e. this hero is being controlled by a game_pad
				# going left
				if data.game_pad.actions[eActions.left]:
					data.facingleft = True
					if data.jump:
						self.updateState(data, common_data, eStates.jumpLeft, hero_jump_cool)
					else:
						self.updateState(data, common_data, eStates.runLeft, hero_run_cool)

				# going right
				elif data.game_pad.actions[eActions.right]:
					data.facingleft = False
					if data.jump:
						self.updateState(data, common_data, eStates.jumpRight, hero_jump_cool)
					else:
						self.updateState(data, common_data, eStates.runRight, hero_run_cool)

				# going up
				elif data.game_pad.actions[eActions.up]:
					if data.jump:
						pass
					else:
						self.updateState(data, common_data, eStates.runUp, hero_run_cool)


				# going down
				elif data.game_pad.actions[eActions.down]:
					if data.jump:
						pass
					else:
						self.updateState(data, common_data, eStates.runDown, hero_run_cool)

				if data.game_pad.actions[eActions.left]:
					data.vel.x = -(hero_speed_while_jumping if data.jump else hero_speed)
				# going right
				elif data.game_pad.actions[eActions.right]:
					data.vel.x = (hero_speed_while_jumping if data.jump else hero_speed)

				# going up
				if data.game_pad.actions[eActions.up]:
					data.vel.y = (hero_speed_while_jumping if data.jump else hero_speed)
				# going down
				elif data.game_pad.actions[eActions.down]:
					data.vel.y = -(hero_speed_while_jumping if data.jump else hero_speed)



				# attacks and block
				if data.game_pad.actions[eActions.jump]:
					# small attack
					if data.jump:
						pass
					else:
						# binky
						data.jump=True
						self.setState(data,common_data,eStates.jumpLeft if data.facingleft else eStates.jumpRight, 0)
						data.vel.z+= hero_jump_speed

				if data.game_pad.actions[eActions.attack_big]:
					data.hero_struck[eStrikes.small]=True
					if data.facingleft:
						self.updateState(data, common_data, eStates.attackSmallLeft, self.strikes[eStrikes.small].cool)
					else:
						self.updateState(data, common_data, eStates.attackSmallRight, self.strikes[eStrikes.small].cool)


		# "physics"
		if data.jump:
			data.vel.friction(hero_friction_air)
		elif data.vel.magsqhoriz() > hero_stop:
			data.vel.friction(hero_friction_ground)
		else:
			# not jumping or moving fast enough so properly stop
			data.vel =  Vec3(0.0,0.0,data.vel.z)

		common_data.pos+=data.vel

		# background.restrictToArena(common_data.pos, data.vel)


	def receiveCollision(self, data, common_data, message=False):
		# log("Hero hit: "+message["name"])
		if message:
			if message.impassable:
				# move out of the way
				pos = common_data.pos
				dim = common_data.entity.collider_data.dim
				orig = common_data.entity.collider_data.orig

				other_pos = message.source.common_data.pos
				other_dim = message.source.collider_data.dim
				other_orig = message.source.collider_data.orig

				if True: #message.platform:
					landed = False
					overlap_bottom = (other_pos.z - other_orig.z) - (pos.z - orig.z + dim.z)
					overlap_top = (other_pos.z - other_orig.z + other_dim.z)- (pos.z - orig.z)
					# print(f"top {overlap_top} bottom {overlap_bottom}")
					if (abs(overlap_top)<abs(overlap_bottom)):
						# closer to top than bottom
						min_z_overlap = overlap_top
						landed = True
					else:
						min_z_overlap = overlap_bottom

					# 	if overlap_top < 10:
					# 		pos.z+=overlap_top+0.02
					# 		data.vel.z=0
					# 		data.jump=False
					# elif data.vel.z<0:
					# 	pos.z+=overlap_bottom
					# 	data.vel.z=-1
					# 	print("bump")
					# else:


					# hit side so work out axis with smallest overlap and spit out
					overlap_right = (other_pos.x-other_orig.x) - (pos.x-orig.x+dim.x)
					overlap_left = ((other_pos.x -other_orig.x+other_dim.x) - (pos.x - orig.x))
					if (abs(overlap_left)<abs(overlap_right)):
						min_x_overlap = overlap_left
					else:
						min_x_overlap = overlap_right

					overlap_up = (other_pos.y-other_orig.y) -(pos.y-orig.y+dim.y)
					overlap_down =  (other_pos.y - other_orig.y + other_dim.y) - (pos.y - orig.y)
					if (abs(overlap_down)<abs(overlap_up)):
						min_y_overlap = overlap_down
					else:
						min_y_overlap = overlap_up

					if abs(min_x_overlap)<abs(min_y_overlap):
						if abs(min_x_overlap)<abs(min_z_overlap):
							pos.x+=min_x_overlap
						else:
							pos.z+=min_z_overlap
							data.vel.z = 0
							if landed:
								data.jump = False
								print("landed")
					else:
						if abs(min_y_overlap)<abs(min_z_overlap):
							pos.y+=min_y_overlap
						else:
							pos.z+=min_z_overlap
							data.vel.z = 0
							if landed:
								data.jump = False
								print("landed 2")







				# print("Landed")
					# 	else:
					# 		print("hit side")
					# 	pos.z=top
					# elif data.vel.z>0:
					# 	# rising and hit bottom
					# 	pos.z = other_pos.z-other_orig.z+orig.z
					# 	print("Bumped head")
					# else:
					# 	data.vel=Vec3(0,0,0)



				# get vector between colliders

				# while collision_manager.checkCollide(common_data.entity, message.source):
				# 	common_data.pos.x -= data.vel.x * 1.1
				# 	common_data.pos.y -= data.vel.y * 1.1
				# 	common_data.pos.z -= data.vel.z * 1.1
				# data.vel.z = 0 #Vec3(0, 0, 0)


class Collider(collision.Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.dim = Vec3(30,8,20)
			self.orig = Vec3(15,4,0)

	def __init__(self, game, data):
		super(collision.Collider, self).__init__(game)
		# global static data to all of HeroCollider components
		self.radius = 10.0
		self.mass = 10.0

	def getRadius(self):
		return self.radius

	def getCollisionMessage(self, data, common_data):
		return(collision.Message(source=common_data.entity, absorb=3))


