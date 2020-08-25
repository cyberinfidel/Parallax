global_tolerance = 0.00001
global_gravity = 0.1

import entity

# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')


class Controller(entity.Component):
	def __init__(self, game):
		super(Controller, self).__init__(game)

	# Update the entity state whether the last action has cooled down or not
	# By default repeating a state is ignored
	# e.g. so a running entity doesnt restart it's running animation every update
	# use the force_new_state flag to force exactly that to happen
	# e.g. when a bat decides to flap it's wings
	def setState(self, data, common_data, state, cooldown=-1, force_new_state=False):
		if common_data.state!=state or force_new_state:
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
	vel.y-=global_gravity

def basic_physics(pos, vel):
	pos.x += vel.x
	pos.y += vel.y
	pos.z += vel.z

def friction(vel, factor=0.1):

	vel.friction(factor)

	# todo: proper friction
