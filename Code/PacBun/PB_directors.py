from director import *
import graphics

from vector import Vec3

def director_meet(game):
	return [
				FadeToClearColor(graphics.Color(0.4,0,0),2),
				Message("Meet the bunnies.", Vec3(160,250,0), graphics.Color(1,1,1,1), 2, graphics.eAlign.centre),
				Delay(1.5),
				Message("Pinkie.", Vec3(140,180,0), graphics.Color(1,0.8,0.8,1), 2, graphics.eAlign.centre),
				Spawn(spawns=[SpawnEntity('pinkie','pinkie', Vec3(140,150,1), game)]),
				Delay(1.6),
				Message("Blue.", Vec3(160,180,0), graphics.Color(0.5,0.5,1.0,1), 2, graphics.eAlign.centre),
				Spawn(spawns=[SpawnEntity('blue','blue', Vec3(160,150,1), game)]),
				Delay(0.9),
				Message("Bowie.", Vec3(180,180,0), graphics.Color(1.0,1.0,1.0,1), 2, graphics.eAlign.centre),
				Spawn(spawns=[SpawnEntity('bowie','bowie', Vec3(180,150,1), game)]),
				Delay(1.5),
				Message("and of course:", Vec3(160,130,0), graphics.Color(1,1,1), 2.5, graphics.eAlign.centre),
				Delay(2),
				Message("PacBun", Vec3(160,120,0), graphics.Color(1,1,0,1), 3, graphics.eAlign.centre),
				Spawn(spawns=[SpawnEntity('pacbun','pacbun', Vec3(160,90,1), game)]),
				Delay(3),
				NextScene() # go to next level
			]

def director_title(game):
	return [
		FadeToClearColor(graphics.Color(0,0.4,0),2),
		Spawn(spawns=[SpawnEntity(template='title',
															name='title',
															pos=Vec3(36, 250, 50),
															parent=game
		)]),
		# Spawn(spawns=[SpawnEntity(game.templates['title'], Vec3(160, 90, 1), game, "title")]),
		Delay(3),
		NextScene()

	]

def director_high_scores(game):
	return [
		FadeToClearColor(graphics.Color(0,0,0.4),2),
		Spawn(spawns=[SpawnEntity(template='high_scores',
															name='high scores',
															pos=Vec3(36, 250, 50),
															parent=game,
															init=	"import high_score\n"
																		"high_score.init(self)"
		)]),
		Delay(3),
		NextScene()

	]

def director_quit(game):
	return [
		FadeToClearColor(graphics.Color(0,0,0),2),
		Message("Goodbye and thank you for playing with me.", Vec3(160, 150, 0), graphics.Color(1, 1, 0, 1), 3, graphics.eAlign.centre),
		Spawn(spawns=[SpawnEntity('pacbun', 'pacbun', Vec3(160, 120, 1), game)]),
		Delay(3),
		Quit()
	]