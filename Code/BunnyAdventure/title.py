from entity import eStates
from game_pad import eActions
import controller
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
	quit = 7
	numTitleStates = 8


def makeGraphics(manager, renlayer):
	return manager.makeTemplate({
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
								["Graphics/Title/Title.png", 4, 4, 0.9],
							],
					},
					{
						"Name": "TitleBar",
						"AnimType": AnimNoLoop,
						"States": [eTitleStates.play],
						"Frames":
							[
								["Graphics/Title/TitleBar.png", 4, 4, 0.9],
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
						"Name": "Win",
						"AnimType": AnimNoLoop,
						"States": [eTitleStates.win],
						"Frames":
							[
								["Graphics/Title/Win 0.png", 4, 4, 2],
							],
					},
					{
						"Name": "Quit",
						"AnimType": AnimNoLoop,
						"States": [eTitleStates.quit],
						"Frames":
							[
								["Graphics/Title/Quit.png", 4, 4, 2],
							],
					},
				]
	})

def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(controller.Controller):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

			self.cooldown = 0
			self.delay = 2

	def __init__(self, game, data):
		super(Controller, self).__init__(game)

	def update(self, data, common_data, dt):
#		if self.coolDown(data, dt):
#			self.cooldown = self.delay

			if common_data.game.game_mode==eGameModes.play:
				self.setState(data, common_data, eTitleStates.play)
				if data.game_pad.actions[eActions.pause]:
					common_data.game.setGameMode(eGameModes.paused)
					self.setState(data, common_data, eTitleStates.paused)
					data.game_pad.actions[eActions.pause] = False  # stops complete quite
					data.game_pad.actions[eActions.quit] = False  # stops complete quite
				if data.game_pad.actions[eActions.select]:
					common_data.game.swapControllers()
			else:
				if common_data.game.game_mode == eGameModes.paused:
					if data.game_pad:
						if data.game_pad.actions[eActions.jump]:
							common_data.game.setGameMode(eGameModes.play)
							self.setState(data, common_data, eTitleStates.play)
							data.game_pad.actions[eActions.jump]=False # stops hero jumping
						if data.game_pad.actions[eActions.quit]:
							common_data.game.setGameMode(eGameModes.title)
							common_data.game.killPlayEntities()
							self.setState(data, common_data, eTitleStates.title)
							data.game_pad.actions[eActions.quit]=False # stops complete quite
						if data.game_pad.actions[eActions.fullscreen]:
							common_data.game.toggleFullscreen()
							data.game_pad.actions[eActions.fullscreen] = False  # stops repeat

				elif common_data.game.game_mode == eGameModes.title:
					self.setState(data, common_data, eTitleStates.title)
					if data.game_pad:
						if data.game_pad.actions[eActions.jump]:
							common_data.game.setGameMode(eGameModes.start)
							self.setState(data, common_data, eTitleStates.play)
							data.game_pad.actions[eActions.jump]=False # stops hero jumping
						if data.game_pad.actions[eActions.quit]:
							common_data.game.setGameMode(eGameModes.quit)
							common_data.game.killPlayEntities()
							self.setState(data, common_data, eTitleStates.quit)
							data.game_pad.actions[eActions.quit] = False  # stops complete quite
						if data.game_pad.actions[eActions.fullscreen]:
							common_data.game.toggleFullscreen()
							data.game_pad.actions[eActions.fullscreen] = False  # stops repeat

				elif common_data.game.game_mode == eGameModes.game_over:
					self.setState(data, common_data, eTitleStates.game_over)
				elif common_data.game.game_mode == eGameModes.win:
					self.setState(data, common_data, eTitleStates.win)



