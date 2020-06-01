from entity import *

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
		for indexA, colliderA in enumerate(self.collidables):
			for indexB, colliderB in enumerate(self.collidables):
				if indexB>indexA:
					self.checkCollide(colliderA, colliderB)

	def cleanUpDead(self):
		for index, collider in enumerate(self.collidables):
			if collider.getState() == eStates.dead:
				self.collidables.pop(index)

	def checkCollide(self,A,B):
		# hack in simple 2D circle logic atm?
		# hack in 3D sphere logic atm?
		distSq = A.getPos().distSq(B.getPos())
#		log("Collision? %s : %s" % (A.getName(), B.getName()))
		if distSq<((A.collider.getRadius()+B.collider.getRadius())*(A.collider.getRadius()+B.collider.getRadius())):
			# only entities with controllers can react to a collision
			if A.controller:
				A.controller.receiveCollision(A.controller_data, A.common_data, B.collider.getCollisionMessage(A.collider_data, A.common_data))
			if B.controller:
				B.controller.receiveCollision(B.controller_data, B.common_data,A.collider.getCollisionMessage(B.controller_data,B.common_data))



class Collider(Component):
	def __init__(self):
		super(Collider, self).__init__()