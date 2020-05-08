# import python libs
import sys

# import Parallax files
# 	add path to Parallax
sys.path.insert(1, '../')
# actually import files
import game
import entity
import controller
import collision
import graphics
import game
from vector import *


from FeedTheDuckScripts import *
from pond import *

# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')


class Prototype(game.Game):
	def __init__(self):
		super(Prototype, self).__init__()

		self.collision_manager = collision.CollisionManager() # TODO: should this be a ComponentManager() like the others?

		###################
		# make components #
		###################
		# Graphics Templates

		backgraphics = self.graphics_manager.makeTemplate({
			"Name": "Background",
			"Template": graphics.SingleImage,
			"RenderLayer": self.renlayer,
			"Image": ["Graphics/Background/Back.png", 0, 65, 0]
		})
		rockgraphics = self.graphics_manager.makeTemplate(RockGraphics(self.renlayer))
		duckgraphics = self.graphics_manager.makeTemplate(DuckGraphics(self.renlayer))

		# Controller Templates

		duckcontroller = self.controller_manager.makeTemplate(
			{
				"Template": DuckController
			}
		)

		# Collider Templates
		duckcollider = self.collision_manager.makeTemplate(
			{
				"Template": DuckCollider
			}
		)

		rockcollider = self.collision_manager.makeTemplate(
			{
				"Template": RockCollider
			}
		)

		# make some entities with components
		back_t = self.entity_manager.makeTemplate(graphics=backgraphics)
		back = self.entity_manager.makeEntity(back_t)
		self.drawables.append(back)
		back.setPos(Vec3(0,135,0))

		rock_t = self.entity_manager.makeTemplate(graphics=rockgraphics, collider = rockcollider)
		rock = self.entity_manager.makeEntity(rock_t, "Rock")
		self.drawables.append(rock)
		rock.setPos(Vec3(180.0,50.0,0.0))
		self.collision_manager.append(rock)

		duck_t = self.entity_manager.makeTemplate(graphics=duckgraphics, controller=duckcontroller, collider=duckcollider)
		duck = self.entity_manager.makeEntity(duck_t, "Duck")

		duck.setPos(Vec3(160.0, 100.0, 0.0))
		duck.setGamePad(self.input.getGamePad(0))
		self.drawables.append(duck)
		self.updatables.append(duck)
		self.collision_manager.append(duck)

	###########
	#  update #
	###########

	def update(self, dt):



		for index, updatable in reversed(list(enumerate(self.updatables))):
			updatable.update(dt)
			if updatable.getState() == entity.eStates.dead:
				self.updatables.pop(index)

		self.collision_manager.doCollisions()
		self.collision_manager.cleanUpDead()


		for index, drawable in enumerate(self.drawables):
			if drawable.getState() == entity.eStates.dead:
				self.drawables.pop(index)

	###########
	#  interp #
	###########
	# TODO: interpolate movement/animation frames to make smoother
	def interp(self, alpha):
		pass

	###########
	#  draw		#
	###########

	def draw(self):
		for drawable in self.drawables:
			drawable.draw()

		self.renlayer.renderSorted()


def run():
	game = Prototype()
	game.run()
	return 0


if __name__ == "__main__":
	sys.exit(run())
