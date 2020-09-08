import px_entity
import controller
import graphics
def makeGraphics(manager, renlayer):
	return manager.makeTemplate({
			"Name": "Heart Animations",
			"Template": graphics.MultiAnim,
			"RenderLayer": renlayer,
			"Anims":
				[
					{
						"Name": "stationary",
						"AnimType": graphics.AnimRandom,
						"States": [px_entity.eStates.stationary],
						"Frames":
							[
								["Graphics/Heart/Heart 7.png", 4, 4, 0, 0.9],
								["Graphics/Heart/Heart 6.png", 4, 4, 0, 0.1],
							],
					},
					{
						"Name": "appear",
						"AnimType": graphics.AnimNoLoop,
						"States": [px_entity.eStates.appear],
						"Frames":
							[
								["Graphics/Heart/Heart 1.png", 4, 4, 0, 0.2],
								["Graphics/Heart/Heart 2.png", 4, 4, 0, 0.2],
								["Graphics/Heart/Heart 3.png", 4, 4, 0, 0.2],
								["Graphics/Heart/Heart 4.png", 4, 4, 0, 0.2],
								["Graphics/Heart/Heart 5.png", 4, 4, 0, 0.3],
								["Graphics/Heart/Heart 6.png", 4, 4, 0, 0.4],
								["Graphics/Heart/Heart 7.png", 4, 4, 0, 0.5],
							],
					},
					{
						"Name": "fade",
						"AnimType": graphics.AnimNoLoop,
						"States": [px_entity.eStates.fade],
						"Frames":
							[
								["Graphics/Heart/Heart 7.png", 4, 4, 0, 0.5],
								["Graphics/Heart/Heart 6.png", 4, 4, 0, 0.4],
								["Graphics/Heart/Heart 5.png", 4, 4, 0, 0.3],
								["Graphics/Heart/Heart 4.png", 4, 4, 0, 0.2],
								["Graphics/Heart/Heart 3.png", 4, 4, 0, 0.2],
								["Graphics/Heart/Heart 2.png", 4, 4, 0, 0.2],
								["Graphics/Heart/Heart 1.png", 4, 4, 0, 0.2],
								["Graphics/Heart/Heart 0.png", 4, 4, 0, 0.2],
							],
					},
				]
	})

def makeController(manager):
	return manager.makeTemplate({"Template": HeartIndicatorController})
class HeartIndicatorController(controller.Controller):
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
				if common_data.state==px_entity.eStates.fade:
					self.setState(data, common_data, px_entity.eStates.appear, 1)
				else:
					self.setState(data, common_data, px_entity.eStates.stationary, 1)
			else:
				if common_data.state in (px_entity.eStates.appear, px_entity.eStates.stationary):
					self.setState(data, common_data, px_entity.eStates.fade, 1)
				else:
					common_data.blink=True
