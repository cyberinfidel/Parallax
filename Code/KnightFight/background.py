from controller import *
from collision import *
from graphics import *


class BackgroundController(Controller):
	def __init__(self, data):
		pass

	def collision(self, data, pos):
		collision = False

		for wall in data:
			collision &=wall.collision(pos)

		return collision

def backGraphics(renlayer):
	return {
			"Name": "Background",
			"Template": SingleImage,
			"RenderLayer": renlayer,
			"Image": ["Graphics/FightCourtyard.png", 0, 136, 0]
		}



