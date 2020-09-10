import copy

import px_entity
import px_controller
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

########################################
# controller for select bunnies scene
def makeMapController(manager):
	return manager.makeTemplate({"Template": MapController})
class MapController(px_controller.Controller):


	def __init__(self, game, data, tile_t):
		super(MapController, self).__init__(game)

	def initEntity(self, entity, data=False):
		impassables = ['H','#','<','>']

		entity.map = copy.deepcopy(data['Map'])

		# flip since we draw from bottom left
		for i in range(0, 9):
			entity.map[i], entity.map[17-i] = entity.map[17 - i], entity.map[i]

		entity.tiles = [None]*18
		for i in range(0,18):
			entity.tiles[i] = [None]*20

		entity.holes = []
		entity.bunny_starts = []
		entity.fox_starts=[]

		tile_t = entity.game.getTemplateForName('tile')
		entity.num_spaces=0
		entity.num_poos=0
		for y in range(0,18):
			for x in range(0,20):
				# create tile for each square
				this_tile = entity.game.requestNewEntity(tile_t,
																							 pos=Vec3(8 + x * 16, 8 + y * 16, 1),
																							 parent=self,
																							 name=f"back{x},{y}")
				entity.tiles[y][x]=this_tile

				# set up each tile from what the map says
				if entity.map[y][x]=="H":
					this_tile.controller.setState(this_tile, tile.eTileStates.hedge)
				elif entity.map[y][x]=="#":
					this_tile.controller.setState(this_tile, tile.eTileStates.void)
				else:
					# work out ways out of the space
					exit_map_value=0
					if y+1<18:
						if entity.map[y + 1][x] not in impassables:
							this_tile.controller.addExit(this_tile, px_entity.eDirections.up)
							exit_coord = Vec3(x*16+8,y*16+10,0)
							exit_direction = px_entity.eDirections.up
							exit_map_value += 1
					if y-1>0:
						if entity.map[y - 1][x] not in impassables:
							this_tile.controller.addExit(this_tile, px_entity.eDirections.down)
							exit_coord = Vec3(x * 16 +8, y * 16 +6, 0)
							exit_direction = px_entity.eDirections.down
							exit_map_value += 2
					if x-1>0:
						if entity.map[y][x - 1] not in impassables:
							this_tile.controller.addExit(this_tile, px_entity.eDirections.left)
							exit_coord = Vec3(x * 16  +6, y * 16+8, 0)
							exit_direction = px_entity.eDirections.left
							exit_map_value += 4
					if x+1<20:
						if entity.map[y][x + 1] not in impassables:
							this_tile.controller.addExit(this_tile, px_entity.eDirections.right)
							exit_coord = Vec3(x * 16 + 10, y * 16+8, 0)
							exit_direction = px_entity.eDirections.right
							exit_map_value += 8

					if entity.map[y][x] == "o":
						this_tile.controller.setState(this_tile, tile.eTileStates.hole)
						entity.holes.append(Hole(Vec3(x, y, 0), exit_coord, exit_direction))
					elif entity.map[y][x] == "O":
						this_tile.controller.setState(this_tile, tile.eTileStates.cutscene_hole)
					elif entity.map[y][x] == "T":
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
						this_tile.controller.setState(this_tile, tile.eTileStates.tunnel_no_exit+exit_map_value)


					else:
						if entity.map[y][x] == "B":
							entity.bunny_starts.append(Vec3(x * 16 + 8, y * 16 + 8, 0))
						elif entity.map[y][x] == "1":
							entity.fox_starts.append(Fox(pos=Vec3(x * 16 + 8, y * 16 + 8, 0),type=fox.eFoxTypes.direct))
						elif entity.map[y][x] == "2":
							entity.fox_starts.append(Fox(Vec3(x * 16 + 8, y * 16 + 8, 0),fox.eFoxTypes.axis_swap))
						elif entity.map[y][x] == "3":
							entity.fox_starts.append(Fox(Vec3(x * 16 + 8, y * 16 + 8, 0),fox.eFoxTypes.ahead))
						elif entity.map[y][x] == "4":
							entity.fox_starts.append(Fox(Vec3(x * 16 + 8, y * 16 + 8, 0),fox.eFoxTypes.cowardly))
						# blank space
						entity.num_spaces += 1
						this_tile.controller.setState(this_tile.controller_data, this_tile, tile.eTileStates.path)




	def getLocFromCoord(self,entity,x,y):
		return entity.map[y][x]

	def getCoordFromPos(self,pos):
		return int(pos.x/16),int(pos.y/16)

	def getTileFromCoord(self,entity,x,y):
		return entity.tiles[y][x]

	def getNextHole(self,entity,x,y):
		for index,hole in enumerate(entity.holes):
			if (x==hole.pos.x and y==hole.pos.y):
				if len(entity.holes)>index+1:
					return entity.holes[index+1]
				else:
					return entity.holes[0]

	def getBunnyStarts(self,entity):
		return entity.bunny_starts

	def getFoxStarts(self,entity):
		return entity.fox_starts

	def poo(self, entity, current_tile, data):
		# can poo in a clear tile only
		current_tile.setState(current_tile, tile.eTileStates.poo)
		entity.num_poos+=1
		data.score+=1
		if entity.num_poos>= entity.num_spaces:
			data.score+=100
			entity.game.setGameMode(PacBun.eGameModes.escape)
			print("Win not implemented yet")
			return True	# signal win
		return False