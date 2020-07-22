from director import Event, Controller, Delay, SpawnEntity, EndGame
from vector import Vec3, rand_num

class SpawnEnemies(Event):
	def __init__(game, spawns):
		super(Event, game).__init__()
		game.spawns = spawns

	def update(game, data, common_data, dt):
		# spawn entities in spawns list
		for spawn in game.spawns:
			common_data.game.requestNewEnemy(
				entity_template= spawn.template,
				pos = spawn.pos,
				parent = False,
				name = spawn.name
			)
		return False # all done

class WaitForNoEnemies(Event):
	def __init__(game):
		super(Event, game).__init__()

	def update(game, data, common_data, dt):
		return common_data.game.num_monsters > 0



def KFEvents(game):
	return[
			# wait a bit
			Delay(2),
		SpawnEnemies([
			SpawnEntity(game.bat_t, Vec3(290, 5, 35), False, "Bat 1"),
		]),

		SpawnEnemies([
				SpawnEntity(game.goblin_archer_t, Vec3(292, 0, 35), False, "Goblin Archer"),
			]),
		SpawnEnemies([
				SpawnEntity(game.goblin_archer_t, Vec3(25, 0, 35), False, "Goblin Archer"),
			]),
		# wait a bit
			Delay(0.7),
			SpawnEnemies([
			SpawnEntity(game.reaper_t, Vec3(30, 0, 35), False, "Reaper"),
			]),
			Delay(rand_num(1)+0.5),

			# wait until all monsters destroyed
			WaitForNoEnemies(),
			# wait a bit
			Delay(4),

			# first wave
			SpawnEnemies([
				SpawnEntity(game.reaper_t, Vec3(300, 0, 35), False, "Reaper 2"),
			]),
			Delay(rand_num(1)+0.5),
			SpawnEnemies([
				SpawnEntity(game.reaper_t, Vec3(20, 0, 35), False, "Reaper 2"),
			]),

			# wait until all monsters destroyed
			WaitForNoEnemies(),
			# wait a bit
			Delay(4),

			# second  wave
			SpawnEnemies([
				SpawnEntity(game.bat_t, Vec3(30, 5, 35), False, "Bat 1"),
			]),
			Delay(rand_num(1)+0.5),
			# spawn other half of wave
			SpawnEnemies([
				SpawnEntity(game.bat_t, Vec3(300, 5, 35), False, "Bat 1"),
			]),
			Delay(rand_num(1)+0.5),
			SpawnEnemies([
				SpawnEntity(game.bat_t, Vec3(155, 5, 110), False, "Bat 1"),
			]),
			Delay(rand_num(1)+0.5),
			# spawn other half of wave
			SpawnEnemies([
				SpawnEntity(game.bat_t, Vec3(300, 5, 35), False, "Bat 1"),
			]),
			Delay(rand_num(1)+0.5),
			SpawnEnemies([
				SpawnEntity(game.bat_t, Vec3(30, 5, 35), False, "Bat 1"),
			]),
			Delay(rand_num(1)+0.5),
			# spawn other half of wave
			SpawnEnemies([
				SpawnEntity(game.bat_t, Vec3(155, 5, 110), False, "Bat 1"),
			]),

			# wait until all monsters destroyed
			WaitForNoEnemies(),

			# wait a bit
			Delay(2),

			# ...

			WaitForNoEnemies(),
			# wait a bit
			Delay(2),
			# signal game complete
			EndGame()
		]