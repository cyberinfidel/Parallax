import enum

import entity
import controller
import graphics
import game
import game_pad

class eTitleStates:
	dead, hide, title, paused, game_over, win, play, quit, escape, numTitleStates = range(0,10)


def makeGraphics(manager, renlayer):
	return manager.makeTemplate({
			"Name": "Title Animations",
			"Template": graphics.MultiAnim,
			"RenderLayer": renlayer,
			"Anims":
				[
					{
						"Name": "Title",
						"AnimType": graphics.AnimNoLoop,
						"States": [eTitleStates.title],
						"Frames":
							[
								["Graphics/Title/Title.png", 10, -24, 0, 0.9],
							],
					},
					{
						"Name": "TitleBar",
						"AnimType": graphics.AnimNoLoop,
						"States": [eTitleStates.play],
						"Frames":
							[
								["Graphics/Title/TitleBar.png", -110, 20, 0, 0.9],
							],
					},
					{
						"Name": "Paused",
						"AnimType": graphics.AnimNoLoop,
						"States": [eTitleStates.paused],
						"Frames":
							[
								["Graphics/Title/Paused.png", -30, -24, 0, 0.2],
							],
					},
					{
						"Name": "Game Over",
						"AnimType": graphics.AnimNoLoop,
						"States": [eTitleStates.game_over],
						"Frames":
							[
								["Graphics/Title/GameOver.png", -50, -24, 0, 0.2],
							],
					},
					{
						"Name": "Win",
						"AnimType": graphics.AnimNoLoop,
						"States": [eTitleStates.win],
						"Frames":
							[
								["Graphics/Title/Win.png", 4, 4, 0, 2],
							],
					},
					{
						"Name": "Escape",
						"AnimType": graphics.AnimLoop,
						"States": [eTitleStates.escape],
						"Frames":
							[
								["Graphics/Title/Escape.png", 4, -100, 0, 0.5],
								["Graphics/Title/Escape2.png", 4, -100, 0, 0.5],
							],
					},
					{
						"Name": "Quit",
						"AnimType": graphics.AnimNoLoop,
						"States": [eTitleStates.quit],
						"Frames":
							[
								["Graphics/Title/Quit.png", 6, -24, 0, 2],
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

			if common_data.game.game_mode==game.eGameModes.play:
				self.setState(data, common_data, eTitleStates.play)
				if data.game_pad.actions[game_pad.eActions.pause]:
					common_data.game.setGameMode(game.eGameModes.paused)
					self.setState(data, common_data, eTitleStates.paused)
					data.game_pad.actions[game_pad.eActions.pause] = False  # stops complete quite
					data.game_pad.actions[game_pad.eActions.quit] = False  # stops complete quite
			else:
				if common_data.game.game_mode == game.eGameModes.paused:
					if data.game_pad:
						if data.game_pad.actions[game_pad.eActions.jump]:
							common_data.game.setGameMode(game.eGameModes.play)
							self.setState(data, common_data, eTitleStates.play)
							data.game_pad.actions[game_pad.eActions.jump]=False # stops hero jumping
						if data.game_pad.actions[game_pad.eActions.quit]:
							common_data.game.setGameMode(game.eGameModes.title)
							common_data.game.killPlayEntities()
							self.setState(data, common_data, eTitleStates.title)
							data.game_pad.actions[game_pad.eActions.quit]=False # stops complete quite
						if data.game_pad.actions[game_pad.eActions.fullscreen]:
							common_data.game.toggleFullscreen()
							data.game_pad.actions[game_pad.eActions.fullscreen] = False  # stops repeat

				elif common_data.game.game_mode == game.eGameModes.title:
					self.setState(data, common_data, eTitleStates.title)
					if data.game_pad:
						if data.game_pad.actions[game_pad.eActions.jump]:
							common_data.game.setGameMode(game.eGameModes.start)
							self.setState(data, common_data, eTitleStates.play)
							data.game_pad.actions[game_pad.eActions.jump]=False # stops hero jumping
						if data.game_pad.actions[game_pad.eActions.quit]:
							common_data.game.setGameMode(game.eGameModes.quit)
							common_data.game.killPlayEntities()
							self.setState(data, common_data, eTitleStates.quit)
							data.game_pad.actions[game_pad.eActions.quit] = False  # stops complete quite
						if data.game_pad.actions[game_pad.eActions.fullscreen]:
							common_data.game.toggleFullscreen()
							data.game_pad.actions[game_pad.eActions.fullscreen] = False  # stops repeat

				elif common_data.game.game_mode == game.eGameModes.game_over:
					self.setState(data, common_data, eTitleStates.game_over)
				elif common_data.game.game_mode == game.eGameModes.win:
					self.setState(data, common_data, eTitleStates.win)



