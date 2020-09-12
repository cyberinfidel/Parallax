import enum
from px_entity import ComponentManager, Component, eStates
from px_vector import Vec3
from px_log import log

# globals
collision_debug = False

class eShapes(enum.IntEnum):
	sphere = 0
	cuboidAA = 1,
	cuboid = 2


class CollisionManager(ComponentManager):

	def __init__(self, game):
		super(CollisionManager, self).__init__(game)
		self.odd= True

	def doCollisions(self):
		if len(self.instances)>1:
			for indexA, colliderA in enumerate(self.instances):
				for colliderB in self.instances[indexA+1:]:
					if self.checkCollide(colliderA, colliderB):
						self.resolveCollision(colliderA, colliderB)

	def doCollisionsWithSingleEntity(self, entity):
		for colliderA in self.instances:
					if self.checkCollide(colliderA, entity):
						self.resolveCollision(colliderA,entity)

	def getDistanceBelow(self, pos):
		for collider in self.instances:
			pass
		return 0


	def cleanUpDead(self):
		self.instances[:] = [x for x in self.instances if x.getState()!=eStates.dead]

	def checkCollide(self,A,B):

		# progressive bounding box
		# check x first
		Apos = A.getPos()
		Adim = A.dim
		Aorig = A.orig
		Bpos = B.getPos()
		Bdim = B.dim
		Borig = B.orig

		if (Apos.x - Aorig.x + Adim.x)> (Bpos.x -Borig.x): # Aright > Bleft
			if (Bpos.x - Borig.x + Bdim.x) > (Apos.x - Aorig.x): # Bright < Aleft
				if (Apos.z - Aorig.z + Adim.z) > (Bpos.z - Borig.z):
					if (Bpos.z - Borig.z + Bdim.z) > (Apos.z - Aorig.z):
						if (Apos.y - Aorig.y + Adim.y) > (Bpos.y - Borig.y):
							if (Bpos.y - Borig.y + Bdim.y) > (Apos.y - Aorig.y):
								# we have a collision

								if collision_debug:
									log(f"Collision - A: {A.name} B: {B.name}")
								return True

	def resolveCollision(self, A, B):
			if A.hasComponent('controller'):
				A.getComponent('controller').receiveCollision(A, B.getComponent('collider').getCollisionMessage(B))
			if B.hasComponent('controller'):
				B.getComponent('controller').receiveCollision(B, A.getComponent('collider').getCollisionMessage(A))




class Collider(Component):
	def __init__(self, game):
		super(Collider, self).__init__(game)

class Message(object):
	def __init__(self, source, damage=0, damage_hero=0, force=Vec3(0,0,0), absorb=0, impassable=False):
		self.source = source
		self.damage = damage
		self.absorb = absorb
		self.damage_hero = damage_hero
		self.force = force
		self.absorb = absorb
		self.impassable = impassable
