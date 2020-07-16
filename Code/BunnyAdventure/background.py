from graphics import SingleImage
import controller
from vector import Vec3

class BackgroundController(controller.Controller):
	def __init__(self, game, data):
		super(BackgroundController, self).__init__(game)

def backgroundGraphics(renlayer):
	return {
			"Name": "Background",
			"Template": SingleImage,
			"RenderLayer": renlayer,
			"Image": ["Graphics/Back/Meadow.png", 0, 230, 0]
		}


def restrictToArena(pos, vel):
	# stop running through walls at either side
	# if pos on left side of line then force to right side
	# while pos.whichSidePlane(Plane(1, -1, 0, 0)):
	# 	controller.basic_physics(pos, Vec3(0.1, -0.1, 0)) # normal vector to plane

	# stop running through walls at either side
	# if pos on left side of line then force to right side
	# while not pos.whichSidePlane(Plane(1, 1, 0, -1920)):
	# 	controller.basic_physics(pos, Vec3(-0.1, -0.1, 0)) # normal vector to plane

	# stop running off screen bottom, top and sides
	pos.clamp(Vec3(100, 0, 0), Vec3(600, 200, 1000))


