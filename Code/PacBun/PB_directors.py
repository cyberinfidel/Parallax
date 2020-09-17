from px_director import *
from px_graphics import Color
import px_graphics

from px_vector import Vec3

#####################################################################
# scene directors - actually make a scene happen
def director_meet(game):
	bunnies = game.game_data['bunnies']
	return [
		FadeToClearColor(Color(0, 0, 0), 2),
		FadeRenderLayer('overlay', Color(1,1,1,1),1),
		FadeRenderLayer('game', Color(1,1,1,1), 1),
		Message("Meet the bunnies.", Vec3(240,250,0), Color(1, 1, 1, 1), 4, px_graphics.eAlign.centre),
		Delay(1.5),
		Message("Pinkie.", Vec3(220,180,0), bunnies['pinkie'].color, 2,px_graphics.eAlign.centre),
		MakeEntity('pinkie meet','pinkie', Vec3(220,150,1), game),
		Delay(1.6),
		Message("Blue.", Vec3(240,180,0), bunnies['blue'].color, 2, px_graphics.eAlign.centre),
		MakeEntity('blue meet','blue', Vec3(240,150,1), game),
		Delay(0.9),
		Message("Bowie.", Vec3(260,180,0), bunnies['bowie'].color, 2, px_graphics.eAlign.centre),
		MakeEntity('bowie meet','bowie', Vec3(260,150,1), game),
		Delay(1.5),
		Message("and of course:", Vec3(240,130,0), Color(1, 1, 1), 2.5, px_graphics.eAlign.centre),
		Delay(2),
		Message("Pac-Bun", Vec3(240,120,0), bunnies['pacbun'].color, 3, px_graphics.eAlign.centre),
		MakeEntity('pacbun meet','pacbun', Vec3(240,85,1), game),
		Delay(3),
		MakeDirector('fade_to_next_scene')
	]

def director_drake_blue(game):
	return [
		Message("Drake Blue Games presents...", Vec3(240, 180, 0), Color(0.8,0.75,1.0,1.0), -1, px_graphics.eAlign.centre),
		Delay(2),
		MakeDirector('fade_to_mode','title'),
	]


def director_title(game):
	bunnies = game.game_data['bunnies']
	return [
		SetRenderLayerColor('overlay', Color(0,0,0,0)),
		SetRenderLayerColor('game', Color(0,0,0,0)),
		FadeToClearColor(Color(0, 0, 0), 1),
		Delay(1),
		MakeEntity(template='title',
							 name='title',
							 pos=Vec3(240, 185, 0),
							 parent=game
							 ),
		MakeEntity(template='pacbun bye', name='pacbun',
							 pos=Vec3(230, 138, 1), parent=game),
		MakeEntity(template='pinkie bye', name='pinkie',
							 pos=Vec3(210, 138, 1), parent=game),
		MakeEntity(template='blue bye', name='blue',
							 pos=Vec3(250, 138, 1), parent=game),
		MakeEntity(template='bowie bye', name='bowie',
							 pos=Vec3(270, 138, 1), parent=game),
		FadeRenderLayer('overlay', Color(1,1,1,1),1),
		FadeRenderLayer('game', Color(1,1,1,1),1),
		Delay(2),
		Message("Press Space to play", Vec3(240, 110, 0), bunnies['pacbun'].color, -1, px_graphics.eAlign.centre),
		Delay(1),
		Message("(Esc to exit)", Vec3(240, 90, 0), bunnies['pacbun'].color, -1, px_graphics.eAlign.centre),
		Delay(5),
		# FadeRenderLayer('overlay', Color(0,0,0,0),1),
		# Delay(1),
		MakeDirector('fade_to_next_scene')

	]

def director_high_scores(game):
	return [
		FadeToClearColor(Color(0, 0, 0), 2),
		FadeRenderLayer('overlay', Color(1,1,1,1),1),
		Delay(1),
		Message("Best", Vec3(207, 260, 0), Color(1, 1, 0, 1), -1, px_graphics.eAlign.left),
		MakeEntity(template='high_scores',
							 name='high scores',
							 pos=Vec3(240, 250, 50),
							 parent=game,
							 init=	"import high_score\n"
											"high_score.init(self)"
							 ),
		Delay(0.8),
		Message("est", Vec3(230, 260, 0), Color(0, 1, 1, 1), -1, px_graphics.eAlign.left),
		Delay(0.8),
		Message("Buns", Vec3(250, 260, 0), Color(1, 0, 1, 1), -1, px_graphics.eAlign.left),
		Delay(3),
		# FadeRenderLayer('overlay', Color(0,0,0,0),1),
		# Delay(1),
		MakeDirector('fade_to_next_scene')

	]

def director_quit(game):
	bunnies = game.game_data['bunnies']
	return [
		FadeToClearColor(Color(0, 0, 0), 1),
		SetRenderLayerColor('game', Color(0,0,0,0)),
		SetRenderLayerColor('overlay', Color(0,0,0,0)),
		FadeRenderLayer('game', Color(1,1,1,1),0.5),
		FadeRenderLayer('overlay', Color(1,1,1,1),0.5),
		Message("Goodbye and thank you for playing", Vec3(240, 165, 0), bunnies['pacbun'].color, 3, px_graphics.eAlign.centre),
		Message("with me and my friends.", Vec3(240, 150, 0), bunnies['pacbun'].color, 3, px_graphics.eAlign.centre),
		MakeEntity(template='pacbun bye', name='pacbun',
							 pos=Vec3(240, 115, 1), parent=game),
		MakeEntity(template='pinkie bye', name='pinkie',
							 pos=Vec3(221, 89, 1), parent=game),
		MakeEntity(template='blue bye', name='blue',
							 pos=Vec3(236, 85, 1), parent=game),
		MakeEntity(template='bowie bye', name='bowie',
							 pos=Vec3(252, 86, 1), parent=game),
		Delay(2),
		FadeRenderLayer('game', Color(0,0,0,0),1),
		FadeRenderLayer('overlay', Color(0,0,0,0),1),
		Delay(2),
		Quit()
	]

def director_play(game, data):
	bunnies = game.game_data['bunnies']
	events =  [
		FadeRenderLayer('overlay', Color(1, 1, 1, 1), 1),
	]
	for message in data['title']:
		events.extend([
			Message(message, Vec3(240, 200, 0), bunnies.index(game.current_bun[0]).color, 2, px_graphics.eAlign.centre),
			Delay(2.5),
		])
	events.extend([
		MakeEntity('map', data=data['map']),
		FadeToClearColor(Color.fromInts(219, 182, 85), 1),
		FadeRenderLayer('game', Color(1,1,1,1),1),
		MakeDirector('bun_caught'),
		WaitForFlag('escape'),
		MakeEntity('escape',pos=Vec3(92,200,0)),
		WaitForFlag('next_scene'),
		KillEntity('escape'),

		# # fade out at end of scene
		Delay(1),
		# MakeEntity('director', init="import PB_directors\n"
		# 																					 "self.events = PB_directors.director_fade_to_next_scene(self.game)"),
		MakeDirector('fade_to_next_scene')
	])
	return events

def director_bunny_select(game):
	return [
		SetRenderLayerColor('game', Color(0,0,0,0)),
		SetRenderLayerColor('overlay', Color(0,0,0,0)),
		FadeToClearColor(Color.fromInts(0, 0, 0), 1),
		Message("Choose your bunny:", Vec3(240, 220, 0), Color(1,1,1,1), -1, px_graphics.eAlign.centre),
		MakeEntity('pacbun choose', data={
			'pos': Vec3(210,160,0),
			'parent': 'bunny choice',
			'bun num': 0,
			'bun name': 'Pac-Bun',
			'message color': px_graphics.Color(1, 1, 0, 1),
		}),
		MakeEntity('pinkie choose', data={
			'pos': Vec3(230, 160, 0),
			'parent': 'bunny choice',
			'bun num': 1,
			'bun name': 'Pinkie',
			'message color': px_graphics.Color(1, 0.8, 0.8, 1),
		}),
		MakeEntity('blue choose', data={
			'pos': Vec3(250, 160, 0),
			'parent': 'bunny choice',
			'bun num': 2,
			'bun name': 'Blue',
			'message color': px_graphics.Color(0.5, 0.5, 1.0, 1),
		}),
		MakeEntity('bowie choose', data={
			'pos': Vec3(270, 160, 0),
			'parent': 'bunny choice',
			'bun num': 3,
			'bun name': 'Bowie',
			'message color': px_graphics.Color(1, 1, 1.0, 1),
		}),
		FadeRenderLayer('overlay', Color(1, 1, 1, 1), 1),
		FadeRenderLayer('game', Color(1, 1, 1, 1), 1),
		WaitForFlag('next_scene'),
		MakeDirector('fade_to_mode','play')
	]

#####################################################################
# assistant directors - brought in by directors to do specific things
def director_fade_to_next_scene(game):
	return [
		FadeToClearColor(Color(0, 0, 0), 1),
		FadeRenderLayer('overlay', Color(0,0,0,0), 1),
		FadeRenderLayer('game', Color(0,0,0,0),1),
		Delay(1),
		NextScene()
	]

def director_fade_to_scene(game, scene):
	return [
		FadeToClearColor(Color(0, 0, 0), 1),
		FadeRenderLayer('overlay', Color(0,0,0,0), 1),
		FadeRenderLayer('game', Color(0,0,0,0),1),
		Delay(1),
		NextScene(next_scene=scene)
	]

def director_fade_to_mode(game, mode):
	return [
		FadeToClearColor(Color(0, 0, 0), 1),
		FadeRenderLayer('overlay', Color(0,0,0,0), 1),
		FadeRenderLayer('game', Color(0,0,0,0),1),
		Delay(1),
		NextScene(mode=mode)
	]


def director_bun_caught(game):
	return [
		WaitForFlag('bunny_caught'),
		Delay(1),
		FadeToClearColor(Color(0, 0, 0), 1),
		FadeRenderLayer('overlay', Color(0, 0, 0, 0), 1),
		FadeRenderLayer('game', Color(0, 0, 0, 0), 1),
		Delay(1),
		NextScene(mode='title')
	]