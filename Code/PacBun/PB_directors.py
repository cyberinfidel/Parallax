from px_director import *
import px_graphics

from px_vector import Vec3

def director_meet(game):
	bunnies = game.game_data['bunnies']
	return [
		FadeToClearColor(px_graphics.Color(0, 0, 0), 2),
		FadeRenderLayer('overlay', px_graphics.Color(1,1,1,1),1),
		FadeRenderLayer('game', px_graphics.Color(1,1,1,1), 1),
		Message("Meet the bunnies.", Vec3(160,250,0), px_graphics.Color(1, 1, 1, 1), 4, px_graphics.eAlign.centre),
		Delay(1.5),
		Message("Pinkie.", Vec3(140,180,0), bunnies['pinkie'].color, 2,px_graphics.eAlign.centre),
		Spawn(spawns=[SpawnEntity('pinkie meet','pinkie', Vec3(140,150,1), game)]),
		Delay(1.6),
		Message("Blue.", Vec3(160,180,0), bunnies['blue'].color, 2, px_graphics.eAlign.centre),
		Spawn(spawns=[SpawnEntity('blue meet','blue', Vec3(160,150,1), game)]),
		Delay(0.9),
		Message("Bowie.", Vec3(180,180,0), bunnies['bowie'].color, 2, px_graphics.eAlign.centre),
		Spawn(spawns=[SpawnEntity('bowie meet','bowie', Vec3(180,150,1), game)]),
		Delay(1.5),
		Message("and of course:", Vec3(160,130,0), px_graphics.Color(1, 1, 1), 2.5, px_graphics.eAlign.centre),
		Delay(2),
		Message("PacBun", Vec3(160,120,0), bunnies['pacbun'].color, 3, px_graphics.eAlign.centre),
		Spawn(spawns=[SpawnEntity('pacbun meet','pacbun', Vec3(160,90,1), game)]),
		Delay(3),
		FadeRenderLayer('overlay', px_graphics.Color(0, 0, 0, 0), 1),
		FadeRenderLayer('game', px_graphics.Color(0, 0, 0, 0), 1),
		Delay(1),
		NextScene() # go to next level
	]

def director_title(game):
	return [
		SetRenderLayerColor('overlay', px_graphics.Color(0,0,0,0)),
		FadeToClearColor(px_graphics.Color(0, 0, 0), 1),
		Delay(1),
		FadeRenderLayer('overlay', px_graphics.Color(1,1,1,1),1),
		Spawn(spawns=[SpawnEntity(template='title',
															name='title',
															pos=Vec3(36, 250, 50),
															parent=game
															)]),
		# Spawn(spawns=[SpawnEntity(game.templates['title'], Vec3(160, 90, 1), game, "title")]),
		Delay(3),
		FadeRenderLayer('overlay', px_graphics.Color(0,0,0,0),1),
		Delay(1),
		NextScene()

	]

def director_high_scores(game):
	return [
		FadeToClearColor(px_graphics.Color(0, 0, 0), 2),
		FadeRenderLayer('overlay', px_graphics.Color(1,1,1,1),1),
		Message("Best", Vec3(132, 287, 0), px_graphics.Color(1, 1, 0, 1), -1, px_graphics.eAlign.left),
		Spawn(spawns=[SpawnEntity(template='high_scores',
															name='high scores',
															pos=Vec3(36, 250, 50),
															parent=game,
															init=	"import high_score\n"
																		 "high_score.init(self)"
															)]),
		Delay(0.8),
		Message("est", Vec3(155, 287, 0), px_graphics.Color(0, 1, 1, 1), -1, px_graphics.eAlign.left),
		Delay(0.8),
		Message("Buns", Vec3(175, 287, 0), px_graphics.Color(1, 0, 1, 1), -1, px_graphics.eAlign.left),
		Delay(3),
		FadeRenderLayer('overlay', px_graphics.Color(0,0,0,0),1),
		Delay(1),
		NextScene()

	]

def director_quit(game):
	bunnies = game.game_data['bunnies']
	return [
		FadeToClearColor(px_graphics.Color(0, 0, 0), 1),
		SetRenderLayerColor('game', px_graphics.Color(0,0,0,0)),
		SetRenderLayerColor('overlay', px_graphics.Color(0,0,0,0)),
		FadeRenderLayer('game', px_graphics.Color(1,1,1,1),0.5),
		FadeRenderLayer('overlay', px_graphics.Color(1,1,1,1),0.5),
		Message("Goodbye and thank you for playing", Vec3(160, 165, 0), bunnies['pacbun'].color, 3, px_graphics.eAlign.centre),
		Message("with me and my friends.", Vec3(160, 150, 0), bunnies['pacbun'].color, 3, px_graphics.eAlign.centre),
		Spawn(spawns=[
			SpawnEntity(template='pacbun bye', name='pacbun',
									pos=Vec3(160, 120, 1), parent=game),
			SpawnEntity(template='pinkie bye', name='pinkie',
									pos=Vec3(143, 94, 1), parent=game),
			SpawnEntity(template='blue bye', name='blue',
									pos=Vec3(158, 90, 1), parent=game),
			SpawnEntity(template='bowie bye', name='bowie',
									pos=Vec3(174, 91, 1), parent=game),
		]),
		Delay(2),
		FadeRenderLayer('game', px_graphics.Color(0,0,0,0),1),
		FadeRenderLayer('overlay', px_graphics.Color(0,0,0,0),1),
		Delay(1),
		Quit()
	]

def director_play(game, data):
	bunnies = game.game_data['bunnies']
	events =  [
		FadeToClearColor(px_graphics.Color.fromInts(0, 0, 0), 1),
		FadeRenderLayer('overlay', px_graphics.Color(1,1,1,1), 1),
		FadeRenderLayer('game', px_graphics.Color(0,0,0,0),1),
		Delay(1),
	]
	for message in data['title']:
		events.extend([
			Message(message, Vec3(160, 200, 0), bunnies.index(game.current_bun[0]).color, 2, px_graphics.eAlign.centre),
			Delay(2.5),
		])
	events.extend([
		Spawn(spawns=
					[
						SpawnEntity('map',
												data=data['map']
												)
					]),
		FadeToClearColor(px_graphics.Color.fromInts(219, 182, 85), 1),
		FadeRenderLayer('game', px_graphics.Color(1,1,1,1),1),
		Delay(20),

		# fade out at end of scene
		FadeToClearColor(px_graphics.Color.fromInts(0, 0, 0), 1),
		FadeRenderLayer('overlay', px_graphics.Color(0,0,0,0), 1),
		FadeRenderLayer('game', px_graphics.Color(0,0,0,0),1),
		Delay(1),
		NextScene()
	])
	return events

def director_bunny_select(game):
	return [
		SetRenderLayerColor('game', px_graphics.Color(0,0,0,0)),
		SetRenderLayerColor('overlay', px_graphics.Color(0,0,0,0)),
		FadeToClearColor(px_graphics.Color.fromInts(0, 0, 0), 1),
		FadeRenderLayer('overlay', px_graphics.Color(1, 1, 1, 1), 1),
		FadeRenderLayer('game', px_graphics.Color(1, 1, 1, 1), 1),
		Message("Choose your bunny:", Vec3(160, 260, 0), px_graphics.Color(1,1,1,1), -1, px_graphics.eAlign.centre),
		#todo: add a wait for signal event then fade out
		# FadeRenderLayer('overlay', px_graphics.Color(0,0,0,0), 1),
		# FadeRenderLayer('game', px_graphics.Color(0,0,0,0), 1),
	]