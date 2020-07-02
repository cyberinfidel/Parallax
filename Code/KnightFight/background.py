from controller import Controller
from graphics import SingleImage


class BackgroundController(Controller):
	def __init__(self, game, data):
		super(Controller, self).__init__(game)

def backgroundGraphics(renlayer):
	return {
			"Name": "Background",
			"Template": SingleImage,
			"RenderLayer": renlayer,
			"Image": ["Graphics/FightCourtyard.png", 0, 136, 0]
		}

def backLGraphics(renlayer):
	return {
			"Name": "Background",
			"Template": SingleImage,
			"RenderLayer": renlayer,
			"Image": ["Graphics/BackLeft.png", 0, 50, 0]
		}

def backRGraphics(renlayer):
	return {
			"Name": "Background",
			"Template": SingleImage,
			"RenderLayer": renlayer,
			"Image": ["Graphics/BackRight.png", 0, 50, 0]
		}



