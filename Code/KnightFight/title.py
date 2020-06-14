from entity import eStates, eActions
from controller import Controller
from graphics import MultiAnim, AnimRandom, AnimNoLoop
from game import eGameModes

def titleGraphics(renlayer):
	return{
			"Name": "Title Animations",
			"Template": MultiAnim,
			"RenderLayer": renlayer,
			"Anims":
				[
					{
						"Name": "stationary",
						"AnimType": AnimRandom,
						"State": eStates.stationary,
						"Frames":
							[
								["Graphics/Title/Title.png", 4, 4, 0.9],
								# ["Graphics/Title/Title 6.png", 4, 4, 0.1],
							],
					},
					{
						"Name": "appear",
						"AnimType": AnimNoLoop,
						"State": eStates.appear,
						"Frames":
							[
								["Graphics/Title/Title.png", 4, 4, 0.2],
								# ["Graphics/Title/Title 2.png", 4, 4, 0.2],
								# ["Graphics/Title/Title 3.png", 4, 4, 0.2],
								# ["Graphics/Title/Title 4.png", 4, 4, 0.2],
								# ["Graphics/Title/Title 5.png", 4, 4, 0.3],
								# ["Graphics/Title/Title 6.png", 4, 4, 0.4],
								# ["Graphics/Title/Title 7.png", 4, 4, 0.5],
							],
					},
					{
						"Name": "fade",
						"AnimType": AnimNoLoop,
						"State": eStates.fade,
						"Frames":
							[
								["Graphics/Title/Title.png", 4, 4, 0.5],
								# ["Graphics/Title/Title 6.png", 4, 4, 0.4],
								# ["Graphics/Title/Title 5.png", 4, 4, 0.3],
								# ["Graphics/Title/Title 4.png", 4, 4, 0.2],
								# ["Graphics/Title/Title 3.png", 4, 4, 0.2],
								# ["Graphics/Title/Title 2.png", 4, 4, 0.2],
								# ["Graphics/Title/Title 1.png", 4, 4, 0.2],
								# ["Graphics/Title/Title 0.png", 4, 4, 0.2],
							],
					},
				]
	}

class TitleController(Controller):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

			self.cooldown = 0
			self.health_num = 0

	def __init__(self, data):
		super(TitleController, self).__init__()

	def update(self, data, common_data, dt):
		if not self.coolDown(data, dt):
			if data.game_pad:
				if data.game_pad.actions[eActions.jump]:
					common_data.parent.setGameMode(eGameModes.start)
					common_data.state = eStates.dead
			# cooling down so can't do anything new
			# if hero health is greater or equal to this Title's number
			# common_data.blink = False
			# if common_data.parent.controller_data.health>=data.health_num:
			# 	if common_data.state==eStates.fade:
			# 		self.setState(data, common_data, eStates.appear, 1)
			# 	else:
			# 		self.setState(data, common_data, eStates.stationary, 1)
			# else:
			# 	if common_data.state in (eStates.appear,eStates.stationary):
			# 		self.setState(data, common_data, eStates.fade, 1)
			# 	else:
			# 		common_data.blink=True
