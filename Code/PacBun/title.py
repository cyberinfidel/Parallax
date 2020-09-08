# controller for title mode of PacBun

# Parallax
import controller
import game_pad

import PacBun

class eTitleStates:
	dead, hide, title, paused, game_over, win, play, quit, escape, high_score, new_high_score, numTitleStates = range(0,12)

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
			self.delay = 2
			print("Made title controller instance")

	def __init__(self, game, data):
		super(Controller, self).__init__(game)
		print("Made title controller template")

	def update(self, data, common_data, dt):
		print("Controller update")
		pass



