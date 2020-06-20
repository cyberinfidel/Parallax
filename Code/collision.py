import enum
from entity import ComponentManager, Component, eStates
from vector import Vec3

# globals
collision_debug = False

class eShapes(enum.IntEnum):
	sphere = 0
	cuboid = 1


class CollisionManager(ComponentManager):

	def __init__(self, game):
		super(CollisionManager, self).__init__(game)
		self.collidables = []

	def append(self, item):
		self.collidables.append(item)
		return len(self.collidables) - 1

	def pop(self, index):
		return pop(index)

	def doCollisions(self):
		if len(self.collidables)>1:
			for indexA, colliderA in enumerate(self.collidables):
				for colliderB in self.collidables[indexA+1:]:
						self.checkCollide(colliderA, colliderB)

	def doCollisionsWithSingleEntity(self, entity):
		for colliderA in self.collidables:
					self.checkCollide(colliderA, entity)


	def cleanUpDead(self):
		self.collidables[:] = [x for x in self.collidables if x.getState()!=eStates.dead]

	def checkCollide(self,A,B):

		# progressive bounding box
		# check x first
		Apos = A.getPos()
		Adim = A.collider.getDim()
		Aorig = A.collider.getOrig()
		Bpos = B.getPos()
		Bdim = B.collider.getDim()
		Borig = B.collider.getOrig()

		if (Apos.x - Aorig.x + Adim.x)> (Bpos.x -Borig.x): # Aright > Bleft
			if (Bpos.x - Borig.x + Bdim.x) > (Apos.x - Aorig.x): # Bright < Aleft
				if (Apos.y - Aorig.y + Adim.y) > (Bpos.y - Borig.y):
					if (Bpos.y - Borig.y + Bdim.y) > (Apos.y - Aorig.y):
						if (Apos.z - Aorig.z + Adim.z) > (Bpos.z - Borig.z):
							if (Bpos.z - Borig.z + Bdim.z) > (Apos.z - Aorig.z):
								# we have a collision
								if A.controller:
									A.controller.receiveCollision(A.controller_data, A.common_data, B.collider.getCollisionMessage(B.collider_data, B.common_data))
								if B.controller:
									B.controller.receiveCollision(B.controller_data, B.common_data,A.collider.getCollisionMessage(A.collider_data,A.common_data))



class Collider(Component):
	def __init__(self, game):
		super(Collider, self).__init__(game)

	def getDim(self):
		return self.dim

	def getOrig(self):
		return self.orig

class Message():
	def __init__(self, source, damage=0, damage_hero=0, force=Vec3(0,0,0)):
		self.source = source
		self.damage = damage
		self.damage_hero = damage_hero
		self.force = force

	def getCollisionMessage(self,data, common_data):
		return Message(source=False)

