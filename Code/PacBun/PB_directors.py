from px_director import *
from px_graphics import Color
import px_graphics

from px_vector import Vec3

def director_meet(game):
	bunnies = game.game_data['bunnies']
	return [
		FadeToClearColor(Color(0, 0, 0), 2),
		FadeRenderLayer('overlay', Color(1,1,1,1),1),
		FadeRenderLayer('game', Color(1,1,1,1), 1),
		Message("Meet the bunnies.", Vec3(256,250,0), Color(1, 1, 1, 1), 4, px_graphics.eAlign.centre),
		Delay(1.5),
		Message("Pinkie.", Vec3(236,180,0), bunnies['pinkie'].color, 2,px_graphics.eAlign.centre),
		Spawn(spawns=[SpawnEntity('pinkie meet','pinkie', Vec3(236,150,1), game)]),
		Delay(1.6),
		Message("Blue.", Vec3(256,180,0), bunnies['blue'].color, 2, px_graphics.eAlign.centre),
		Spawn(spawns=[SpawnEntity('blue meet','blue', Vec3(256,150,1), game)]),
		Delay(0.9),
		Message("Bowie.", Vec3(276,180,0), bunnies['bowie'].color, 2, px_graphics.eAlign.centre),
		Spawn(spawns=[SpawnEntity('bowie meet','bowie', Vec3(276,150,1), game)]),
		Delay(1.5),
		Message("and of course:", Vec3(256,130,0), Color(1, 1, 1), 2.5, px_graphics.eAlign.centre),
		Delay(2),
		Message("PacBun", Vec3(256,120,0), bunnies['pacbun'].color, 3, px_graphics.eAlign.centre),
		Spawn(spawns=[SpawnEntity('pacbun meet','pacbun', Vec3(256,85,1), game)]),
		Delay(3),
		FadeRenderLayer('overlay', Color(0, 0, 0, 0), 1),
		FadeRenderLayer('game', Color(0, 0, 0, 0), 1),
		Delay(1),
		NextScene() # go to next level
	]

def director_title(game):
	return [
		SetRenderLayerColor('overlay', Color(0,0,0,0)),
		FadeToClearColor(Color(0, 0, 0), 1),
		Delay(1),
		FadeRenderLayer('overlay', Color(1,1,1,1),1),
		Spawn(spawns=[SpawnEntity(template='title',
															name='title',
															pos=Vec3(132, 250, 50),
															parent=game
															)]),
		# Spawn(spawns=[SpawnEntity(game.templates['title'], Vec3(256, 90, 1), game, "title")]),
		Delay(3),
		FadeRenderLayer('overlay', Color(0,0,0,0),1),
		Delay(1),
		NextScene()

	]

def director_high_scores(game):
	return [
		FadeToClearColor(Color(0, 0, 0), 2),
		FadeRenderLayer('overlay', Color(1,1,1,1),1),
		Message("Best", Vec3(228, 287, 0), Color(1, 1, 0, 1), -1, px_graphics.eAlign.left),
		Spawn(spawns=[SpawnEntity(template='high_scores',
															name='high scores',
															pos=Vec3(256, 250, 50),
															parent=game,
															init=	"import high_score\n"
																		 "high_score.init(self)"
															)]),
		Delay(0.8),
		Message("est", Vec3(251, 287, 0), Color(0, 1, 1, 1), -1, px_graphics.eAlign.left),
		Delay(0.8),
		Message("Buns", Vec3(271, 287, 0), Color(1, 0, 1, 1), -1, px_graphics.eAlign.left),
		Delay(3),
		FadeRenderLayer('overlay', Color(0,0,0,0),1),
		Delay(1),
		NextScene()

	]

def director_quit(game):
	bunnies = game.game_data['bunnies']
	return [
		FadeToClearColor(Color(0, 0, 0), 1),
		SetRenderLayerColor('game', Color(0,0,0,0)),
		SetRenderLayerColor('overlay', Color(0,0,0,0)),
		FadeRenderLayer('game', Color(1,1,1,1),0.5),
		FadeRenderLayer('overlay', Color(1,1,1,1),0.5),
		Message("Goodbye and thank you for playing", Vec3(256, 165, 0), bunnies['pacbun'].color, 3, px_graphics.eAlign.centre),
		Message("with me and my friends.", Vec3(256, 150, 0), bunnies['pacbun'].color, 3, px_graphics.eAlign.centre),
		Spawn(spawns=[
			SpawnEntity(template='pacbun bye', name='pacbun',
									pos=Vec3(256, 115, 1), parent=game),
			SpawnEntity(template='pinkie bye', name='pinkie',
									pos=Vec3(237, 89, 1), parent=game),
			SpawnEntity(template='blue bye', name='blue',
									pos=Vec3(252, 85, 1), parent=game),
			SpawnEntity(template='bowie bye', name='bowie',
									pos=Vec3(268, 86, 1), parent=game),
		]),
		Delay(2),
		FadeRenderLayer('game', Color(0,0,0,0),1),
		FadeRenderLayer('overlay', Color(0,0,0,0),1),
		Delay(1),
		Quit()
	]

def director_play(game, data):
	bunnies = game.game_data['bunnies']
	events =  [
		FadeToClearColor(Color.fromInts(0, 0, 0), 1),
		FadeRenderLayer('overlay', Color(1,1,1,1), 1),
		FadeRenderLayer('game', Color(0,0,0,0),1),
		Delay(1),
	]
	for message in data['title']:
		events.extend([
			Message(message, Vec3(256, 200, 0), bunnies.index(game.current_bun[0]).color, 2, px_graphics.eAlign.centre),
			Delay(2.5),
		])
	events.extend([
		Spawn(spawns=
					[
						SpawnEntity('map',
												data=data['map']
												)
					]),
		FadeToClearColor(Color.fromInts(219, 182, 85), 1),
		FadeRenderLayer('game', Color(1,1,1,1),1),
		WaitFor(game.checkReady,'escape'),
		Spawn(spawns=[SpawnEntity('escape',
															pos=Vec3(108,200,0))]),
		WaitFor(game.checkReady,'next_scene'),

		# # fade out at end of scene
		Delay(1),
		FadeToClearColor(Color.fromInts(0, 0, 0), 1),
		FadeRenderLayer('overlay', Color(0,0,0,0), 1),
		FadeRenderLayer('game', Color(0,0,0,0),1),
		Delay(1),
		NextScene()
	])
	return events

def director_bunny_select(game):
	return [
		SetRenderLayerColor('game', Color(0,0,0,0)),
		SetRenderLayerColor('overlay', Color(0,0,0,0)),
		FadeToClearColor(Color.fromInts(0, 0, 0), 1),
		FadeRenderLayer('overlay', Color(1, 1, 1, 1), 1),
		FadeRenderLayer('game', Color(1, 1, 1, 1), 1),
		Message("Choose your bunny:", Vec3(256, 260, 0), Color(1,1,1,1), -1, px_graphics.eAlign.centre),
		#todo: add a wait for signal event then fade out
		# FadeRenderLayer('overlay', Color(0,0,0,0), 1),
		# FadeRenderLayer('game', Color(0,0,0,0), 1),
	]