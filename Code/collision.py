from entity import *

# globals
collision_debug = False

class eShapes(enum.IntEnum):
	sphere = 0
	cuboid = 1


class CollisionManager(ComponentManager):

	def __init__(self):
		super(CollisionManager, self).__init__()
		self.collidables = []

	def append(self, item):
		self.collidables.append(item)
		return len(self.collidables) - 1

	def pop(self, index):
		return pop(index)

	def doCollisions(self):
		for A in self.collidables:
			A.common_data.blink = False

		for indexA, colliderA in enumerate(self.collidables):
			for indexB, colliderB in enumerate(self.collidables):
				if indexB>indexA:
					self.checkCollide(colliderA, colliderB)

	def doCollisionsWithSingleEntity(self, entity):
		if collision_debug:
			for A in self.collidables:
				A.common_data.blink = False

		for colliderA in self.collidables:
					self.checkCollide(colliderA, entity)


	def cleanUpDead(self):
		for index, collider in enumerate(self.collidables):
			if collider.getState() == eStates.dead:
				self.collidables.pop(index)

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
								if collision_debug:
									log("Collide!")
									# only entities with controllers can react to a collision
									A.common_data.blink = True
									B.common_data.blink = True
								if A.controller:
									A.controller.receiveCollision(A.controller_data, A.common_data, B.collider.getCollisionMessage(A.collider_data, A.common_data))
								if B.controller:
									B.controller.receiveCollision(B.controller_data, B.common_data,A.collider.getCollisionMessage(B.controller_data,B.common_data))



class Collider(Component):
	def __init__(self):
		super(Collider, self).__init__()

	def getDim(self):
		return self.dim

	def getOrig(self):
		return self.orig

class Message():
	def __init__(self, source, damage=0, damage_hero=0):
		self.source = source
		self.damage = damage
		self.damage_hero = damage_hero

	def getCollisionMessage(self,data, common_data):
		return Message(source=False)

