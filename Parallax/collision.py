import enum
from Parallax import entity, vector, log

# globals
collision_debug = False

class eShapes(enum.IntEnum):
	sphere = 0
	cuboid = 1


class CollisionManager(entity.ComponentManager):

	def __init__(self, game):
		super(CollisionManager, self).__init__(game)

	def doCollisions(self):
		if len(self.instances)>1:
			for indexA, colliderA in enumerate(self.instances):
				for colliderB in self.instances[indexA+1:]:
						self.checkCollide(colliderA, colliderB)

	def doCollisionsWithSingleEntity(self, entity):
		for colliderA in self.instances:
					self.checkCollide(colliderA, entity)


	def cleanUpDead(self):
		self.instances[:] = [x for x in self.instances if x.getState()!=entity.eStates.dead]

	def checkCollide(self,A,B):

		# progressive bounding box
		# check x first
		Apos = A.getPos()
		Adim = A.collider_data.dim
		Aorig = A.collider_data.orig
		Bpos = B.getPos()
		Bdim = B.collider_data.dim
		Borig = B.collider_data.orig

		if (Apos.x - Aorig.x + Adim.x)> (Bpos.x -Borig.x): # Aright > Bleft
			if (Bpos.x - Borig.x + Bdim.x) > (Apos.x - Aorig.x): # Bright < Aleft
				if (Apos.y - Aorig.y + Adim.y) > (Bpos.y - Borig.y):
					if (Bpos.y - Borig.y + Bdim.y) > (Apos.y - Aorig.y):
						if (Apos.z - Aorig.z + Adim.z) > (Bpos.z - Borig.z):
							if (Bpos.z - Borig.z + Bdim.z) > (Apos.z - Aorig.z):
								# we have a collision
								if collision_debug:
									log(f"Collision - A: {A.common_data.name} B: {B.common_data.name}")
								if A.controller:
									A.controller.receiveCollision(A.controller_data, A.common_data, B.collider.getCollisionMessage(B.collider_data, B.common_data))
								if B.controller:
									B.controller.receiveCollision(B.controller_data, B.common_data,A.collider.getCollisionMessage(A.collider_data,A.common_data))



class Collider(entity.Component):
	def __init__(self, game):
		super(Collider, self).__init__(game)

class Message():
	def __init__(self, source, damage=0, damage_hero=0, force=vector.Vec3(0,0,0), absorb=0):
		self.source = source
		self.damage = damage
		self.absorb = absorb
		self.damage_hero = damage_hero
		self.force = force

	def getCollisionMessage(self,data, common_data):
		return Message(source=False)

