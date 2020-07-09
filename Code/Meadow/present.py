from graphics import SingleImage
import controller, collision
import game
from vector import Vec3, rand_num

class Controller(controller.Controller):
	def __init__(self, game, data):
		super(Controller, self).__init__(game)

	def receiveCollision(self, data, common_data, message):
		if message:
			if message.damage>0:
				common_data.game.setGameMode(game.eGameModes.win)
				for num in range(0,20):
					bfly = common_data.game.requestNewEntity(
						entity_template= self.butterfly_templates[rand_num(3)],
						pos= common_data.pos,
						parent = common_data.entity,
						name=f"Butterfly {num}"
					)

	def setButterflyTemplates(self, templates):
		self.butterfly_templates = templates

	def update(self,data,common_data, dt):
		pass

def graphics(renlayer):
	return {
			"Name": "Background",
			"Template": SingleImage,
			"RenderLayer": renlayer,
			"Image": ["Graphics/Present/Present.png", 31, 48, 0]
		}


class Collider(collision.Collider):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass
			self.dim = Vec3(64,20,64)
			self.orig = Vec3(32,10,0)

	def __init__(self, game, data):
		super(Collider, self).__init__(game)
		# global static data to all of BatCollider components

	def getRadius(self):
		return self.radius

	def getCollisionMessage(self, data, common_data):
		return(collision.Message(source=common_data.entity, damage=0, damage_hero=0))


