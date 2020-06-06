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

#import Knight Fight files
from KnightFightScripts import *

# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')


class KnightFight(game.Game):
	def __init__(self):
		super(KnightFight, self).__init__("Knight Fight", res_x= 320, res_y= 200, zoom = 3, fullscreen= False)

		self.collision_manager = collision.CollisionManager() # TODO: should this be a ComponentManager() like the others?

		###################
		# make components #
		###################
		# Graphics Templates

		backgraphics = self.graphics_manager.makeTemplate(backGraphics(self.renlayer))
		bat_graphics = self.graphics_manager.makeTemplate(batGraphics(self.renlayer))
		reaper_graphics = self.graphics_manager.makeTemplate(reaperGraphics(self.renlayer))
		reaper_controller = self.controller_manager.makeTemplate({"Template": ReaperController})
		raingraphics = self.graphics_manager.makeTemplate(rainGraphics(self.renlayer))
		herographics = self.graphics_manager.makeTemplate( heroGraphics(self.renlayer))

		# Controller Templates
		backcontroller = self.controller_manager.makeTemplate(
			{"Template": BackgroundController,
			 "Lines":
				 [
					 Line(Vec3(64, 136, 0), Vec3(256, 136, 0)),
					 Line(Vec3(0, 199, 0), Vec3(319, 199, 0)),
					 Line(Vec3(64, 136, 0), Vec3(0, 199, 0)),
					 Line(Vec3(256, 136, 0), Vec3(319, 199, 0)),
				 ],
			 }
		)
		raincontroller = self.controller_manager.makeTemplate({"Template": RainController})
		herocontroller = self.controller_manager.makeTemplate({"Template": HeroController})
		bat_controller = self.controller_manager.makeTemplate({"Template": BatController})

		# Collider Templates
		hero_collider = self.collision_manager.makeTemplate({"Template": HeroCollider})
		bat_collider =self.collision_manager.makeTemplate({"Template": BatCollider})
		reaper_collider =self.collision_manager.makeTemplate({"Template": ReaperCollider})

		# make some entities with all the components that have been defined
		back_t = self.entity_manager.makeTemplate(graphics=backgraphics, controller=backcontroller)
		back = self.entity_manager.makeEntity(back_t)
		back.setPos(Vec3(0.0, 64.0, 0.0))

		self.drawables.append(back)

		# make bats
		self.singlebats = []
		self.numbats = 5
		singlebat_t = self.entity_manager.makeTemplate(graphics=bat_graphics, controller = bat_controller, collider=bat_collider)
		for n in range(0, self.numbats):
			singlebat = self.entity_manager.makeEntity(singlebat_t, "Bat")
			if n % 2 == 0:
				singlebat.setPos(Vec3(rand_num(20), rand_num(64), rand_num(20)+40))
			else:
				singlebat.setPos(Vec3(rand_num(20) + 250, rand_num(64), rand_num(20)+40))
			self.singlebats.append(singlebat)
			singlebat.update(rand_num(200) / 200.0)
			self.drawables.append(singlebat)
			self.updatables.append(singlebat)
			self.collision_manager.append(singlebat)

		# make reapers
		self.singlereapers = []
		self.numreapers = 5
		singlereaper_t = self.entity_manager.makeTemplate(graphics=reaper_graphics, controller = reaper_controller, collider=reaper_collider)
		for n in range(0, self.numreapers):
			singlereaper = self.entity_manager.makeEntity(singlereaper_t, "Reaper")
			if n % 2 == 0:
				singlereaper.setPos(Vec3(rand_num(20), rand_num(64), 0))
			else:
				singlereaper.setPos(Vec3(rand_num(20) + 250, rand_num(64), 0))


			self.singlebats.append(singlereaper)
			singlereaper.update(rand_num(200) / 200.0)
			self.drawables.append(singlereaper)
			self.updatables.append(singlereaper)
			self.collision_manager.append(singlereaper)


		# make rain
		self.numrain = 0
		self.rain_t = self.entity_manager.makeTemplate(graphics=raingraphics, controller=raincontroller)
		for n in range(0, self.numrain):
			rain = self.entity_manager.makeEntity(self.rain_t, "Rain Drop")
			rain.setState(RainController.state_fall)
			rain.setPos(Vec3(rand_num(320), rand_num(64), 150))
			self.drawables.append(rain)
			self.updatables.append(rain)

		hero_t = self.entity_manager.makeTemplate(graphics=herographics, controller=herocontroller, collider=hero_collider)

		self.hero = self.entity_manager.makeEntity(hero_t, "Knight")

		self.hero.setPos(Vec3(160.0, 60.0, 0.0))
		self.hero.setGamePad(self.input.getGamePad(0))
		self.drawables.append(self.hero)
		self.updatables.append(self.hero)

	###########
	#  update #
	###########

	def update(self, dt):
		# rain
		if (rand_num(10)==0):
			rain = self.entity_manager.makeEntity(self.rain_t)
			rain.setState(RainController.state_fall)
			rain.setPos(Vec3(rand_num(320), rand_num(64), 200))
			self.drawables.append(rain)
			self.updatables.append(rain)

		for index, updatable in reversed(list(enumerate(self.updatables))):
			updatable.update(dt)

		self.collision_manager.doCollisions() # collisions between monsters
		self.collision_manager.doCollisionsWithSingleEntity(self.hero) # collisions with hero

		for index, updatable in reversed(list(enumerate(self.updatables))):
			if updatable.getState() == entity.eStates.dead:
				self.updatables.pop(index)

		self.collision_manager.cleanUpDead()

		for index, drawable in reversed(list(enumerate(self.drawables))):
			if drawable.getState() == entity.eStates.dead:
				self.drawables.pop(index)

	###########
	#  interp #
	###########

	def interp(self, alpha):
		pass

	###########
	#  draw		#
	###########

	def draw(self):
		for drawable in self.drawables:
			# draw shadows first
			if drawable.graphics.hasShadow():
				drawable.graphics.drawShadow(drawable.graphics_data, drawable.common_data)
			# draw actual things
			if not drawable.common_data.blink:
				drawable.graphics.draw(drawable.graphics_data, drawable.common_data)

		self.renlayer.renderSorted()


def run(tests=False):
	game = KnightFight()
	if tests:
		if game.runTests() != 0:
			log("Unit tests failed.")
			return 1

	game.run()
	return 0


if __name__ == "__main__":
	sys.exit(run(tests=True))
