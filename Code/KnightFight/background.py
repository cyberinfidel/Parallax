import px_controller
import px_graphics
import px_vector
from px_vector import Vec3

def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(px_controller.Controller):
	def __init__(self, game, data):
		super(Controller, self).__init__(game)

def makeGraphics(renlayer):
	return {
			"Name": "Background",
			"Template": px_graphics.MultiImage,
			"RenderLayer": renlayer,
			"Images": [
				["Graphics/FightCourtyard.png", 0, 136, 0, 0],
				["Graphics/BackLeft.png", 0, 60, -44, 0],
				["Graphics/BackRight.png", -289, 60, -44, 0]
		]
		}

# def backLGraphics(renlayer):
# 	return {
# 			"Name": "Background",
# 			"Template": graphics.SingleImage,
# 			"RenderLayer": renlayer,
# 			"Image": ["Graphics/BackLeft.png", 0, 50, 0, 0]
# 		}
#
# def backRGraphics(renlayer):
# 	return {
# 			"Name": "Background",
# 			"Template": graphics.SingleImage,
# 			"RenderLayer": renlayer,
# 			"Image": ["Graphics/BackRight.png", 0, 50, 0, 0]
# 		}

def restrictToArena(pos, vel):
	# stop running through walls at either side
	# if pos on left side of line then force to right side
	while pos.whichSidePlane(px_vector.Plane(1, 0, -1, 0)):
		px_controller.basic_physics(pos, Vec3(0.1, 0, -0.1)) # normal vector to plane

	# stop running through walls at either side
	# if pos on left side of line then force to right side
	while not pos.whichSidePlane(px_vector.Plane(1, 0, 1, -320)):
		px_controller.basic_physics(pos, Vec3(-0.1, 0, -0.1)) # normal vector to plane

	# stop running off screen bottom, top and sides
	pos.clamp(Vec3(0, 0, 0), Vec3(320, 200, 60))


