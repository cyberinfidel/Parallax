from entity import eStates
from controller import Controller
from graphics import MultiAnim, AnimRandom, AnimNoLoop

def heartGraphics(renlayer):
	return{
			"Name": "Heart Animations",
			"Template": MultiAnim,
			"RenderLayer": renlayer,
			"Anims":
				[
					{
						"Name": "stationary",
						"AnimType": AnimRandom,
						"States": [eStates.stationary],
						"Frames":
							[
								["Graphics/Heart/Heart 7.png", 4, 4, 0.9],
								["Graphics/Heart/Heart 6.png", 4, 4, 0.1],
							],
					},
					{
						"Name": "appear",
						"AnimType": AnimNoLoop,
						"States": [eStates.appear],
						"Frames":
							[
								["Graphics/Heart/Heart 1.png", 4, 4, 0.2],
								["Graphics/Heart/Heart 2.png", 4, 4, 0.2],
								["Graphics/Heart/Heart 3.png", 4, 4, 0.2],
								["Graphics/Heart/Heart 4.png", 4, 4, 0.2],
								["Graphics/Heart/Heart 5.png", 4, 4, 0.3],
								["Graphics/Heart/Heart 6.png", 4, 4, 0.4],
								["Graphics/Heart/Heart 7.png", 4, 4, 0.5],
							],
					},
					{
						"Name": "fade",
						"AnimType": AnimNoLoop,
						"States": [eStates.fade],
						"Frames":
							[
								["Graphics/Heart/Heart 7.png", 4, 4, 0.5],
								["Graphics/Heart/Heart 6.png", 4, 4, 0.4],
								["Graphics/Heart/Heart 5.png", 4, 4, 0.3],
								["Graphics/Heart/Heart 4.png", 4, 4, 0.2],
								["Graphics/Heart/Heart 3.png", 4, 4, 0.2],
								["Graphics/Heart/Heart 2.png", 4, 4, 0.2],
								["Graphics/Heart/Heart 1.png", 4, 4, 0.2],
								["Graphics/Heart/Heart 0.png", 4, 4, 0.2],
							],
					},
				]
	}

class HeartIndicatorController(Controller):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

			self.cooldown = 0
			self.health_num = 0

	def __init__(self, game, data):
		super(HeartIndicatorController, self).__init__(game)

	def update(self, data, common_data, dt):
		if not self.coolDown(data, dt):
			# cooling down so can't do anything new
			# if hero health is greater or equal to this heart's number
			common_data.blink = False
			if common_data.parent.controller_data.health>=data.health_num:
				if common_data.state==eStates.fade:
					self.setState(data, common_data, eStates.appear, 1)
				else:
					self.setState(data, common_data, eStates.stationary, 1)
			else:
				if common_data.state in (eStates.appear,eStates.stationary):
					self.setState(data, common_data, eStates.fade, 1)
				else:
					common_data.blink=True
