import enum

import entity
from vector import Vec3
import vector

import tile
import fox

class Hole(object):
	def __init__(self,pos, exit, direction):
		self.pos = pos
		self.exit = exit
		self.direction = direction

class Level(object):

	def __init__(self, game, map):
		self.game = game
		self.map = map

		# flip since we draw from bottom left
		for i in range(0, 10):
			self.map[i], self.map[19-i] = self.map[19 - i], self.map[i]

		self.tiles = [None]*20
		for i in range(0,20):
			self.tiles[i] = [None]*20

		self.holes = []
		self.fox_starts=[]

		self.num_spaces=0
		self.num_poos=0
		for y in range(0,20):
			for x in range(0,20):
				# create tile for each square
				this_tile = self.game.requestNewEntity(self.game.tile_t, pos=Vec3(8 + x * 16, 8 + y * 16, 1), parent=self, name=f"back{x},{y}")
				self.tiles[y][x]=this_tile

				# set up each tile from what the map says
				if self.map[y][x]=="H":
					this_tile.controller.setState(this_tile.controller_data, this_tile.common_data, [tile.eTileStates.hedge,tile.eTileStates.hedge2,tile.eTileStates.hedge3][vector.rand_num(3)])
				else:
					# work out ways out of the space
					if self.map[y + 1][x] != "H":
						this_tile.controller.addExit(this_tile.controller_data, entity.eDirections.up)
						exit_coord = Vec3(x*16+8,y*16+10,0)
						exit_direction = entity.eDirections.up
					if self.map[y - 1][x] != "H":
						this_tile.controller.addExit(this_tile.controller_data, entity.eDirections.down)
						exit_coord = Vec3(x * 16 +8, y * 16 +6, 0)
						exit_direction = entity.eDirections.down
					if self.map[y][x - 1] != "H":
						this_tile.controller.addExit(this_tile.controller_data, entity.eDirections.left)
						exit_coord = Vec3(x * 16  +6, y * 16+8, 0)
						exit_direction = entity.eDirections.left
					if self.map[y][x + 1] != "H":
						this_tile.controller.addExit(this_tile.controller_data, entity.eDirections.right)
						exit_coord = Vec3(x * 16 + 10, y * 16+8, 0)
						exit_direction = entity.eDirections.right

					if self.map[y][x] == "o":
						this_tile.controller.setState(this_tile.controller_data, this_tile.common_data, tile.eTileStates.hole)
						self.holes.append(Hole(Vec3(x,y,0),exit_coord, exit_direction))
					else:
						if self.map[y][x] == "B":
							self.bunny_start = Vec3(x * 16 + 8, y * 16 + 8, 0)
						elif self.map[y][x] == "1":
							self.fox_starts.append((Vec3(x * 16 + 8, y * 16 + 8, 0),fox.eFoxTypes.direct))
						elif self.map[y][x] == "2":
							self.fox_starts.append((Vec3(x * 16 + 8, y * 16 + 8, 0),fox.eFoxTypes.axis_swap))
						elif self.map[y][x] == "3":
							self.fox_starts.append((Vec3(x * 16 + 8, y * 16 + 8, 0),fox.eFoxTypes.ahead))
						elif self.map[y][x] == "4":
							self.fox_starts.append((Vec3(x * 16 + 8, y * 16 + 8, 0),fox.eFoxTypes.cowardly))
						# blank space
						self.num_spaces += 1
						this_tile.controller.setState(this_tile.controller_data, this_tile.common_data, tile.eTileStates.clear)




	def getLocFromCoord(self,x,y):
		return self.map[y][x]

	def getCoordFromPos(self, pos):
		return int(pos.x/16),int(pos.y/16)

	def getTileFromCoord(self, x, y):
		return self.tiles[y][x]

	def getNextHole(self,x,y):
		for index,hole in enumerate(self.holes):
			if (x==hole.pos.x and y==hole.pos.y):
				if len(self.holes)>index+1:
					return self.holes[index+1]
				else:
					return self.holes[0]

	def getBunnyStart(self):
		return self.bunny_start

	def getFoxStarts(self):
		return self.fox_starts

	def poo(self, current_tile, data):
		# can poo in a clear tile only
		current_tile.controller.setState(current_tile.controller_data, current_tile.common_data, tile.eTileStates.poo)
		self.num_poos+=1
		data.score+=1
		if self.num_poos>= self.num_spaces:
			data.score+=100
			return True	# signal win

		return False