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

		self.collision_manager = collision.CollisionManager(game=self) # TODO: should this be a ComponentManager() like the others?

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
		hit_controller = self.controller_manager.makeTemplate({"Template":HitController})

		# Collider Templates
		hero_collider = self.collision_manager.makeTemplate({"Template": HeroCollider})
		bat_collider =self.collision_manager.makeTemplate({"Template": BatCollider})
		reaper_collider =self.collision_manager.makeTemplate({"Template": ReaperCollider})
		hit_collider =self.collision_manager.makeTemplate({"Template": HitCollider})

		#########################################
		# Make entity templates from components #
		#########################################
		back_t = self.entity_manager.makeEntityTemplate(graphics=backgraphics, controller=backcontroller)
		bat_t = self.entity_manager.makeEntityTemplate(graphics=bat_graphics, controller = bat_controller, collider=bat_collider)
		reaper_t = self.entity_manager.makeEntityTemplate(graphics=reaper_graphics, controller = reaper_controller, collider=reaper_collider)
		self.rain_t = self.entity_manager.makeEntityTemplate( graphics=raingraphics, controller=raincontroller)
		hero_t = self.entity_manager.makeEntityTemplate(graphics=herographics, controller=herocontroller, collider=hero_collider)
		# set up hero's attacks
		self.hit_t = self.entity_manager.makeEntityTemplate(graphics=False, controller=hit_controller, collider=hit_collider )
		for hit in (eStates.attackBigLeft,eStates.attackBigRight, eStates.attackSmallLeft, eStates.attackSmallRight, eStates.blockLeft, eStates.blockRight):
			herocontroller.setStateSpawnTemplate(state= hit, template = self.hit_t)

		####################################################################
		# make some entities with all the templates that have been defined #
		####################################################################
		back = self.entity_manager.makeEntity(back_t)
		back.setPos(Vec3(0.0, 64.0, 0.0))

		self.drawables.append(back)

		# make bats
		self.bats = []
		self.numbats = 10
		for n in range(0, self.numbats):
			bat = self.entity_manager.makeEntity(bat_t, "Bat")
			if n % 2 == 0:
				bat.setPos(Vec3(rand_num(20), rand_num(64), rand_num(20)+40))
			else:
				bat.setPos(Vec3(rand_num(20) + 250, rand_num(64), rand_num(20)+40))
			self.drawables.append(bat)
			self.updatables.append(bat)
			self.collision_manager.append(bat)

		# make reapers
		self.reapers = []
		self.numreapers = 10
		for n in range(0, self.numreapers):
			reaper = self.entity_manager.makeEntity(reaper_t, "Reaper")
			if n % 2 == 0:
				reaper.setPos(Vec3(rand_num(40), rand_num(100), 0))
			else:
				reaper.setPos(Vec3(rand_num(40) + 250, rand_num(100), 0))

			self.drawables.append(reaper)
			self.updatables.append(reaper)
			self.collision_manager.append(reaper)


		# make rain
		self.numrain = 0
		for n in range(0, self.numrain):
			rain = self.entity_manager.makeEntity(self.rain_t, "Rain Drop")
			rain.setState(RainController.state_fall)
			rain.setPos(Vec3(rand_num(320), rand_num(64), 150))
			self.drawables.append(rain)
			self.updatables.append(rain)

		# make hero
		self.hero = self.requestNewEntity(entity_template=hero_t,pos=Vec3(160,60,0),parent=False, name="Hero")
		self.hero.setGamePad(self.input.getGamePad(0))

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
		#self.collision_manager.doCollisionsWithSingleEntity(self.hero) # collisions with hero

		# clean up dead entities
		for index, updatable in reversed(list(enumerate(self.updatables))):
			if updatable.getState() == entity.eStates.dead:
				self.updatables.pop(index)
		self.collision_manager.cleanUpDead()
		for index, drawable in reversed(list(enumerate(self.drawables))):
			if drawable.getState() == entity.eStates.dead:
				self.drawables.pop(index)

	def requestNewEntity(self, entity_template, pos, parent, name=False):
		new_entity = self.entity_manager.makeEntity(entity_template, name)
		new_entity.setPos(pos)
		new_entity.setParent(parent)
		#	TODO: add generic names to entity templates
		# if name:
		# 	new_entity.name=name
#		else:
#			new_entity.name=entity_template.getName()

		if new_entity.graphics:
			self.drawables.append(new_entity)
		if new_entity.controller:
			self.updatables.append(new_entity)
		if new_entity.collider:
			self.collision_manager.append(new_entity)
		return new_entity

	def requestTarget(self,pos):
		return self.hero.common_data.pos

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
