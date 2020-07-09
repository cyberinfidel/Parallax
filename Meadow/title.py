from entity import eStates
from game_pad import eActions
from controller import Controller
from graphics import MultiAnim, AnimNoLoop
from game import eGameModes

import enum
class eTitleStates(enum.IntEnum):
	dead = eStates.dead
	hide = eStates.hide,
	title = 2,
	paused = 3,
	game_over = 4,
	win = 5,
	play = 6,
	numTitleStates = 6


def titleGraphics(renlayer):
	return{
			"Name": "Title Animations",
			"Template": MultiAnim,
			"RenderLayer": renlayer,
			"Anims":
				[
					{
						"Name": "Title",
						"AnimType": AnimNoLoop,
						"States": [eTitleStates.title],
						"Frames":
							[
								["Graphics/Title/Title.png", 0, 0, 0.9],
							],
					},
					{
						"Name": "TitleBar",
						"AnimType": AnimNoLoop,
						"States": [eTitleStates.play],
						"Frames":
							[
								["Graphics/Title/TitleBar.png", 0, 0, 0.9],
							],
					},
					{
						"Name": "Paused",
						"AnimType": AnimNoLoop,
						"States": [eTitleStates.paused],
						"Frames":
							[
								["Graphics/Title/Paused.png", 4, 4, 0.2],
							],
					},
					{
						"Name": "Game Over",
						"AnimType": AnimNoLoop,
						"States": [eTitleStates.game_over],
						"Frames":
							[
								["Graphics/Title/GameOver.png", 4, 4, 0.2],
							],
					},
					{
						"Name": "Win Over",
						"AnimType": AnimNoLoop,
						"States": [eTitleStates.win],
						"Frames":
							[
								["Graphics/Title/Win 0.png", 4, 4, 2],
							],
					},
				]
	}

class TitleController(Controller):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

			self.cooldown = 0
			self.delay = 2

	def __init__(self, game, data):
		super(TitleController, self).__init__(game)

	def update(self, data, common_data, dt):
#		if self.coolDown(data, dt):
#			self.cooldown = self.delay

			if common_data.game.game_mode==eGameModes.play:
				self.setState(data, common_data, eTitleStates.play)
				if data.game_pad.actions[eActions.pause]:
					common_data.game.setGameMode(eGameModes.paused)
					self.setState(data, common_data, eTitleStates.paused)
			else:
				if common_data.game.game_mode == eGameModes.paused:
					if data.game_pad:
						if data.game_pad.actions[eActions.jump]:
							common_data.game.setGameMode(eGameModes.play)
							self.setState(data, common_data, eTitleStates.play)
							data.game_pad.actions[eActions.jump]=False # stops hero jumping
				elif common_data.game.game_mode == eGameModes.title:
					self.setState(data, common_data, eTitleStates.title)
					if data.game_pad:
						if data.game_pad.actions[eActions.jump]:
							common_data.game.setGameMode(eGameModes.start)
							self.setState(data, common_data, eTitleStates.play)
							data.game_pad.actions[eActions.jump]=False # stops hero jumping
				elif common_data.game.game_mode == eGameModes.game_over:
					self.setState(data, common_data, eTitleStates.game_over)
				elif common_data.game.game_mode == eGameModes.win:
					self.setState(data, common_data, eTitleStates.win)



