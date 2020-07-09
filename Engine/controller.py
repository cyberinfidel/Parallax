global_tolerance = 0.00001
global_gravity = 0.1

from entity import Component
from vector import Plane, Vec3

# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')


class Controller(Component):
	def __init__(self, game):
		super(Controller, self).__init__(game)

	# Update the entity state whether the last action has cooled down or not
	def setState(self, data, common_data, state, cooldown=-1):
		if common_data.state!=state:
			common_data.state = state
			common_data.new_state = True
			data.cooldown = cooldown

	# Updates the entity state only if the last action has cooled down
	# if an action is supposed to interrupt everything else then don't use this function
	def updateState(self, data, common_data, state, cooldown=-1):
		if data.cooldown<=0 and common_data.state!=state:
			common_data.state = state
			common_data.new_state = True
			data.cooldown = cooldown

	def coolDown(self,data, dt):
		# if doing something that can't be interrupted then countdown and return True
		# unless got to end of it so return False
		# or otherwise return False - not doing anything blocking
		if data.cooldown>0:
			data.cooldown -=dt
			if data.cooldown<=0:
				# cooled down right now
				data.cooldown = -1
				return False
			else:
				# still cooling down
				return True
		# already cooled down
		return False

def basic_gravity(vel):
	vel.z-=global_gravity

def basic_physics(pos, vel):
	pos.x += vel.x
	pos.y += vel.y
	pos.z += vel.z

def friction(vel, factor=0.1):

	vel.friction(factor)

	# todo: proper friction
	# magsq = vel.magsq()/10.0
	# if magsq>global_tolerance:
	# 	vel.x = vel.x + magsq
	# 	vel.y = vel.y + magsq
	# 	vel.z = vel.z + magsq

def restrictToArena(pos, vel):
	# stop running through walls at either side
	# if pos on left side of line then force to right side
	while pos.whichSidePlane(Plane(1, -1, 0, 0)):
		basic_physics(pos, Vec3(0.1, -0.1, 0)) # normal vector to plane

	# stop running through walls at either side
	# if pos on left side of line then force to right side
	while not pos.whichSidePlane(Plane(1, 1, 0, -320)):
		basic_physics(pos, Vec3(-0.1, -0.1, 0)) # normal vector to plane

	# stop running off screen bottom, top and sides
	pos.clamp(Vec3(0, 0, 0), Vec3(320, 60, 200))
