import json
import sdl2

import entity
import controller
import graphics
import text
import game_pad

import game
import PacBun



# class HighScore(object):
# 	def __init__(self, score, image):
# 		self.score = score
# 		self.image = image

# graphics component for getting initials for new high score
class NewScore(entity.Component):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass


	def __init__(self,game, data):
		super(NewScore, self).__init__(game)
		self.render_layer = data["RenderLayer"]
		self.font_manager = data["FontManager"]
		self.font = self.font_manager.addFontFromFile("Fonts/Silom/Silom.ttf", 48)
		self.initial_images = []
		colours = (
			sdl2.SDL_Color(255, 255, 0, 255),
			sdl2.SDL_Color(0, 255, 255, 255),
			sdl2.SDL_Color(255, 0, 255, 255),
		)

		for i in range(0, 3):
			self.initial_images.append(
				self.render_layer.addImageFromString(font_manager=self.font_manager, string="A", font=self.font,
																						 color=colours[i]))

	def draw(self, data, common_data):
		controller_data = common_data.entity.controller_data

		# self.render_layer.queueImage(controller_data.score_image, 85, 270-i*20, 0)
		for i in range(0,3):
			if i!=controller_data.current_initial or not controller_data.blink:
				self.render_layer.queueImage(self.initial_images[i], 100+50*i, 180, 0)

	def update(self, data, common_data, dt):
		pass

	def updateInitials(self, entity):
		# no checking for which one is updated
		# just draws them all again
		colours = (
			sdl2.SDL_Color(255, 255, 0, 255),
			sdl2.SDL_Color(0, 255, 255, 255),
			sdl2.SDL_Color(255, 0, 255, 255),
		)

		for i in range(0, 3):
				self.render_layer.replaceImageFromString(old_image=self.initial_images[i], font_manager=self.font_manager, string=entity.controller_data.initials[i], font=self.font, color=colours[i])

def makeGraphics(manager, render_layer, font_manager):
	return manager.makeTemplate({
			"Name": "Scoreboard",
			"Template": NewScore,
			"RenderLayer": render_layer,
			"FontManager": font_manager,
		})

###########################################################

def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(controller.Controller):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass

			self.initials = ['A','A','A']
			self.current_initial = 0
			self.blink_time = 0.25
			self.blink_cool = self.blink_time
			self.blink = False

	def __init__(self, game, data):
		super(Controller, self).__init__(game)

	def update(self, data, common_data, dt):
		redraw=False
		initial_value = ord(data.initials[data.current_initial])
		if data.game_pad.actions[game_pad.eActions.up]:
			initial_value += 1
			if initial_value>96: initial_value=32
			data.game_pad.actions[game_pad.eActions.up] = False
			redraw=True
		elif data.game_pad.actions[game_pad.eActions.down]:
			initial_value -= 1
			if initial_value<32: initial_value=96
			data.game_pad.actions[game_pad.eActions.down] = False
			redraw = True
		# keep within ascii values 32 (space) and 96 (') inclusive which means
		# a bunch of symbols and uppercase, but no lowercase

		elif data.game_pad.actions[game_pad.eActions.right]:
			data.current_initial = (data.current_initial + 1)%3
			data.game_pad.actions[game_pad.eActions.right] = False
		elif data.game_pad.actions[game_pad.eActions.left]:
			data.current_initial = (data.current_initial - 1)%3
			data.game_pad.actions[game_pad.eActions.left] = False

		elif data.game_pad.actions[game_pad.eActions.jump]:
			data.game_pad.actions[game_pad.eActions.jump] = False
			common_data.game.addNewHighScore(str(data.initials[0])+str(data.initials[1])+str(data.initials[2]))
			self.setState(data, common_data, entity.eStates.dead)

		data.blink_cool -= dt
		if data.blink_cool<=0:
			data.blink_cool = data.blink_time
			data.blink = not data.blink

		data.initials[data.current_initial] = chr(initial_value)
		if redraw:
			common_data.entity.graphics.updateInitials(common_data.entity)






	def getInitials(self, entity, new_score):
		initials = ""
		for i in range(0,3):
			initials += entity.controller_data.initials[i]
		return initials


