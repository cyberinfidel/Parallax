from controller import Controller
from graphics import SingleImage


class BackgroundController(Controller):
	def __init__(self, data):
		pass

	def collision(self, data, pos):
		collision = False

		for wall in data:
			collision &=wall.collision(pos)

		return collision

def backgroundGraphics(renlayer):
	return {
			"Name": "Background",
			"Template": SingleImage,
			"RenderLayer": renlayer,
			"Image": ["Graphics/FightCourtyard.png", 0, 136, 0]
		}



