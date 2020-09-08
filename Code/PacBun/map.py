import copy

import px_entity
from px_vector import Vec3

import tile
import fox
import PacBun

# container for information about the rabbit holes
class Hole(object):
	def __init__(self,pos, exit, direction):
		self.pos = pos
		self.exit = exit
		self.direction = direction

class Fox(object):
	def __init__(self, pos, type):
		self.pos = pos
		self.type = type


class Map(object):


	def __init__(self, game, data, tile_t):

		impassables = ['H','#','<','>']

		self.game = game
		self.map = copy.deepcopy(data['Map'])

		# flip since we draw from bottom left
		for i in range(0, 9):
			self.map[i], self.map[17-i] = self.map[17 - i], self.map[i]

		self.tiles = [None]*18
		for i in range(0,18):
			self.tiles[i] = [None]*20

		self.holes = []
		self.bunny_starts = []
		self.fox_starts=[]

		self.num_spaces=0
		self.num_poos=0
		for y in range(0,18):
			for x in range(0,20):
				# create tile for each square
				this_tile = self.game.requestNewEntity(tile_t,
																							 pos=Vec3(8 + x * 16, 8 + y * 16, 1),
																							 parent=self,
																							 name=f"back{x},{y}")
				self.tiles[y][x]=this_tile

				# set up each tile from what the map says
				if self.map[y][x]=="H":
					this_tile.controller.setState(this_tile.controller_data, this_tile, tile.eTileStates.hedge)
				elif self.map[y][x]=="#":
					this_tile.controller.setState(this_tile.controller_data, this_tile, tile.eTileStates.void)
				else:
					# work out ways out of the space
					exit_map_value=0
					if y+1<18:
						if self.map[y + 1][x] not in impassables:
							this_tile.controller.addExit(this_tile.controller_data, px_entity.eDirections.up)
							exit_coord = Vec3(x*16+8,y*16+10,0)
							exit_direction = px_entity.eDirections.up
							exit_map_value += 1
					if y-1>0:
						if self.map[y - 1][x] not in impassables:
							this_tile.controller.addExit(this_tile.controller_data, px_entity.eDirections.down)
							exit_coord = Vec3(x * 16 +8, y * 16 +6, 0)
							exit_direction = px_entity.eDirections.down
							exit_map_value += 2
					if x-1>0:
						if self.map[y][x - 1] not in impassables:
							this_tile.controller.addExit(this_tile.controller_data, px_entity.eDirections.left)
							exit_coord = Vec3(x * 16  +6, y * 16+8, 0)
							exit_direction = px_entity.eDirections.left
							exit_map_value += 4
					if x+1<20:
						if self.map[y][x + 1] not in impassables:
							this_tile.controller.addExit(this_tile.controller_data, px_entity.eDirections.right)
							exit_coord = Vec3(x * 16 + 10, y * 16+8, 0)
							exit_direction = px_entity.eDirections.right
							exit_map_value += 8

					if self.map[y][x] == "o":
						this_tile.controller.setState(this_tile.controller_data, this_tile, tile.eTileStates.hole)
						self.holes.append(Hole(Vec3(x, y, 0), exit_coord, exit_direction))
					elif self.map[y][x] == "O":
						this_tile.controller.setState(this_tile.controller_data, this_tile, tile.eTileStates.cutscene_hole)
					elif self.map[y][x] == "T":
						# map to which tunnel graphic to use based on exits
						# which_tunnel = [
						# 	tile.eTileStates.tunnel_no_exit,  # 0000
						# 	tile.eTileStates.tunnel_up,  # 0001
						# 	tile.eTileStates.tunnel_down,  # 0010, 2
						# 	tile.eTileStates.tunnel_up_down,  # 0011, 3
						# 	tile.eTileStates.tunnel_left,  # 0100, 4
						# 	tile.eTileStates.tunnel_up_left,  # 0101, 5
						# 	tile.eTileStates.tunnel_down_left,  # 0110, 6
						# 	tile.eTileStates.tunnel_up_down_left,  # 0111, 7
						# 	tile.eTileStates.tunnel_right,  # 1000, 8
						# 	tile.eTileStates.tunnel_up_right,  # 1001, 9
						# 	tile.eTileStates.tunnel_down_right,  # 1010,10
						# 	tile.eTileStates.tunnel_up_down_right,  # 1011,11
						# 	tile.eTileStates.tunnel_left_right,  # 1100,12
						# 	tile.eTileStates.tunnel_up_left_right,  # 1101,13
						# 	tile.eTileStates.tunnel_down_left_right,  # 1110,14
						# 	tile.eTileStates.tunnel_up_down_left_right,  # 1111,15
						# ][exit_map_value]

						if exit_map_value>15:
							print(f"warning: exit map value boo boo {exit_map_value}")
						this_tile.controller.setState(this_tile.controller_data, this_tile, tile.eTileStates.tunnel_no_exit+exit_map_value)


					else:
						if self.map[y][x] == "B":
							self.bunny_starts.append(Vec3(x * 16 + 8, y * 16 + 8, 0))
						elif self.map[y][x] == "1":
							self.fox_starts.append(Fox(pos=Vec3(x * 16 + 8, y * 16 + 8, 0),type=fox.eFoxTypes.direct))
						elif self.map[y][x] == "2":
							self.fox_starts.append(Fox(Vec3(x * 16 + 8, y * 16 + 8, 0),fox.eFoxTypes.axis_swap))
						elif self.map[y][x] == "3":
							self.fox_starts.append(Fox(Vec3(x * 16 + 8, y * 16 + 8, 0),fox.eFoxTypes.ahead))
						elif self.map[y][x] == "4":
							self.fox_starts.append(Fox(Vec3(x * 16 + 8, y * 16 + 8, 0),fox.eFoxTypes.cowardly))
						# blank space
						self.num_spaces += 1
						this_tile.controller.setState(this_tile.controller_data, this_tile, tile.eTileStates.path)




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

	def getBunnyStarts(self):
		return self.bunny_starts

	def getFoxStarts(self):
		return self.fox_starts

	def poo(self, current_tile, data):
		# can poo in a clear tile only
		current_tile.controller.setState(current_tile.controller_data, current_tile, tile.eTileStates.poo)
		self.num_poos+=1
		data.score+=1
		if self.num_poos>= self.num_spaces:
			data.score+=100
			self.game.setGameMode(PacBun.eGameModes.escape)
			return True	# signal win

		return False