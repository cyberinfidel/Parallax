import controller
import graphics
import vector
from vector import Vec3

def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(controller.Controller):
	def __init__(self, game, data):
		super(Controller, self).__init__(game)

def makeGraphics(renlayer):
	return {
			"Name": "Background",
			"Template": graphics.MultiImage,
			"RenderLayer": renlayer,
			"Images": [
				["Graphics/FightCourtyard.png", 0, 136, 0],
				["Graphics/BackLeft.png", 0, 15, 0],
				["Graphics/BackRight.png", -289, 15, 0]
		]
		}

def backLGraphics(renlayer):
	return {
			"Name": "Background",
			"Template": graphics.SingleImage,
			"RenderLayer": renlayer,
			"Image": ["Graphics/BackLeft.png", 0, 50, 0]
		}

def backRGraphics(renlayer):
	return {
			"Name": "Background",
			"Template": graphics.SingleImage,
			"RenderLayer": renlayer,
			"Image": ["Graphics/BackRight.png", 0, 50, 0]
		}

def restrictToArena(pos, vel):
	# stop running through walls at either side
	# if pos on left side of line then force to right side
	while pos.whichSidePlane(vector.Plane(1, -1, 0, 0)):
		controller.basic_physics(pos, Vec3(0.1, -0.1, 0)) # normal vector to plane

	# stop running through walls at either side
	# if pos on left side of line then force to right side
	while not pos.whichSidePlane(vector.Plane(1, 1, 0, -320)):
		controller.basic_physics(pos, Vec3(-0.1, -0.1, 0)) # normal vector to plane

	# stop running off screen bottom, top and sides
	pos.clamp(Vec3(0, 0, 0), Vec3(320, 60, 200))


