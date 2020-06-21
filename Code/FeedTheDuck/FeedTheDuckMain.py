# import python libs
import sys

# import Parallax files
# 	add path to Parallax
sys.path.insert(1, '../')
# actually import files
import entity
import collision
import graphics
import game
from vector import Vec3


from FeedTheDuckScripts import DuckGraphics, DuckController, DuckCollider
from pond import RockGraphics, RockCollider

# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')



class FeedTheDuck(game.Game):
	def __init__(self):
		super(FeedTheDuck, self).__init__(title = "Feed the Duck", res_x= 320, res_y= 200, zoom = 3, fullscreen= False)

		self.collision_manager = collision.CollisionManager(game=self) # TODO: should this be a ComponentManager() like the others?

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
		back_t = self.entity_manager.makeEntityTemplate(graphics=backgraphics)
		back = self.entity_manager.makeEntity(back_t)
		self.drawables.append(back)
		back.setPos(Vec3(0,135,0))

		rock_t = self.entity_manager.makeEntityTemplate(graphics=rockgraphics, collider = rockcollider)

		#for rock_pos in [Vec3(100,50,0)]:#,Vec3(0,0,0)):
		for rock_pos in (Vec3(150,20,0), Vec3(180,20,0), Vec3(120,25,0), Vec3(90,20,0)
		 , Vec3(60,20,0), Vec3(30,25,0), Vec3(35,50,0), Vec3(32,76,0)
		 , Vec3(58,100,0), Vec3(91,114,0), Vec3(123,122,0), Vec3(156,120,0)
		 , Vec3(180,110,0), Vec3(213,116,0), Vec3(242,113,0), Vec3(271,114,0)
			, Vec3(274, 101, 0), Vec3(273, 82, 0), Vec3(277, 60, 0), Vec3(262, 34, 0)
										 , Vec3(244, 32, 0), Vec3(223, 26, 0), Vec3(217, 30, 0), 										 ):
			self.addObstacle(rock_pos, rock_t, self.collision_manager, self.drawables)


		duck_t = self.entity_manager.makeEntityTemplate(graphics=duckgraphics, controller=duckcontroller, collider=duckcollider)
		self.duck = self.entity_manager.makeEntity(duck_t, "Duck")

		self.duck.setPos(Vec3(160.0, 80.0, 0.0))
		self.duck.setGamePad(self.input.getGamePad(0))
		self.drawables.append(self.duck)
		self.updatables.append(self.duck)

	###########
	#  update #
	###########

	def update(self, dt):



		for index, updatable in reversed(list(enumerate(self.updatables))):
			updatable.update(dt)
			if updatable.getState() == entity.eStates.dead:
				self.updatables.pop(index)

		self.collision_manager.doCollisionsWithSingleEntity(self.duck)
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
			if not drawable.common_data.blink:
				drawable.graphics.draw(drawable.graphics_data, drawable.common_data)

		self.renlayer.renderSorted()

	def addObstacle(self, pos, template, collision_manager, drawables):
		rock = self.entity_manager.makeEntity(template, "Rock")
		drawables.append(rock)
		rock.setPos(pos)
		collision_manager.append(rock)


def run():
	game = FeedTheDuck()
	game.run()
	return 0


if __name__ == "__main__":
	sys.exit(run())
