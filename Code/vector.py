import enum
import sys

# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')

x,y,z = 0,1,2

class Plane:
	def __init__(self,a,b,c,d):
		self.a = a
		self.b = b
		self.c = c
		self.d = d

class Vec3:
	def __init__(self, x,y,z):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self, vector):
		return(Vec3(self.x + vector.x, self.y + vector.y, self.z + vector.z))

	def __iadd__(self, vector):
		self.x += vector.x
		self.y += vector.y
		self.z += vector.z
		return self

	def __sub__(self, vector):
		return(Vec3(self.x - vector.x, self.y - vector.y, self.z - vector.z))

	def __isub__(self, vector):
		self.x -= vector.x
		self.y -= vector.y
		self.z -= vector.z
		return self

	def __truediv__(self, div):
		self.x /= div
		self.y /= div
		self.z /= div
		return self

	def __eq__(self, other):
		return self.x==other.x and self.y==other.y and self.z==other.z

	def __ne__(self, other):
		return self.x!=other.x or self.y!=other.y or self.z!=other.z

	def __neg__(self):
		return Vec3(-self.x,-self.y,-self.z)

	def __str__(self):
		return f"({self.x},{self.y},{self.z})"

	def __abs__(self):
		return Vec3(abs(self.x), abs(self.y), abs(self.z))

	def __mul__(self, scalar):
		return Vec3(self.x*scalar,self.y*scalar,self.z*scalar)

	def magsq(self):
		return (self.x*self.x + self.y*self.y + self.z * self.z)

	def magsqhoriz(self):
		return (self.x*self.x + self.z*self.z)

	def distSq(self, B):
		x = (self.x - B.x)
		y = (self.y - B.y)
		z = (self.z - B.z)
		return x * x + y * y + z * z

	def friction(self, factor):
		self.x -= self.x*factor
		self.y -= self.y*factor
		self.z -= self.z*factor

	def clamp(self, minVec, maxVec):
		self.x = max(minVec.x, self.x)
		self.y = max(minVec.y, self.y)
		self.z = max(minVec.z, self.z)

		self.x = min(maxVec.x, self.x)
		self.y = min(maxVec.y, self.y)
		self.z = min(maxVec.z, self.z)

	def whichSidePlane(self, plane):
		return self.x*plane.a+self.y*plane.b+self.z*plane.c+plane.d<0

# convenience methods to get a single dimension flipped
	def flippedX(self):
		return(Vec3(-self.x, self.y, self.z))
	def flippedY(self):
		return(Vec3(self.x, -self.y, self.z))
	def flippedZ(self):
		return(Vec3(self.x, self.y, -self.z))

	## todo operators

#each wall needs a line and a way of telling
#  whether a point is inside the line.
# top
# y = 136
# bottom
# y = 200
# left
# 64, 136 to 0,199
# dx = 64-0, dy = 136-199 = 63 so g = 63/64
# if Py < (Ay - By)/(Ax - Bx) * (Px - Ax) + Ay
#		P below line

# right
# 256, 136 to 319,199

# walls in the background

# y = mx+ c



class LineType(enum.IntEnum):
	sloped = 0,
	vert = 1,
	horiz = 2


class Line(object):

	def __init__(self, A, B):
		if A.y - B.y == 0:
			self.type = LineType.horiz
			self.y = A.y
		elif A.x - B.x == 0:
			self.type = LineType.vert
			self.x = A.x
		else:
			self.type = LineType.sloped
			self.m = (A.y - B.y)/(A.x- B.x)
			self.c = A.y - self.m * A.x

	def whichSide(self,P):
		if self.type == LineType.sloped:
			return P.y < self.m*P.x + self.c
		elif self.type == LineType.horiz:
			return P.y<self.y
		else:
			return P.x < self.x


import random
# wrapper for random numbers
def rand_num(stop):
	return random.randrange(stop)

def runTests():
	a = Vec3(1,1,1)
	b = Vec3(1,2,3)
	# z = Vec3(0,0,0)

	fails=[]

	# test 1
	if not (a+b)==Vec3(2,3,4):
		log("Fail in test 1: a+b")
		fails.append(1)

	# test 2
	if not (b-a)==Vec3(0,1,2):
		log("Fail in test 2: b-a")
		fails.append(2)

	# test 3
	b+=a
	if not (b==Vec3(2,3,4)):
		log("Fail in test 3: b+=a")
		fails.append(3)

	# test 4
	b-=Vec3(1,1,1)
	if not (b==Vec3(1,2,3)):
		log("Fail in test 4: b-=Vec3(1,1,1)")
		fails.append(4)

	# test 5 abs
	a = abs(Vec3(-1,-2,-3))
	if not (a ==Vec3(1,2,3)):
		log("Fail in test 5: abs(Vec3(-1,-2,-3))==Vec3(1,2,3)")
		fails.append(5)

	# test 6 Vec3 * int
	a = Vec3(-1, 2,-3)*4
	if not (a ==Vec3(-4,8,-12)):
		log("Fail in test 6: a ==Vec3(-4,8,-12)")
		fails.append(6)

	# test 6 Vec3 / int
	a = Vec3(-1, 2,-3)/2
	if not (a ==Vec3(-0.5,1,-1.5)):
		log("Fail in test 7: a ==Vec3(-0.5,1,-1.5)")
		fails.append(7)

	return fails

if __name__ == "__main__":
	sys.exit(len(runTests()))
