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

def restrictToArena(pos, vel):
	# stop running through walls at either side
	# if pos on left side of line then force to right side
	while pos.whichSidePlane(Plane(1, -1, 0, 0)):
		basic_physics(pos, Vec3(0.1, -0.1, 0)) # normal vector to plane

	# stop running through walls at either side
	# if pos on left side of line then force to right side
	while not pos.whichSidePlane(Plane(1, 1, 0, -740)):
		basic_physics(pos, Vec3(-0.1, -0.1, 0)) # normal vector to plane

	# stop running off screen bottom, top and sides
	pos.clamp(Vec3(0, 0, 0), Vec3(740, 60, 200))


