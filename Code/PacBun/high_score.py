import json
import sdl2

import entity
import controller
import graphics
import text
import PacBun



# class HighScore(object):
# 	def __init__(self, score, image):
# 		self.score = score
# 		self.image = image

# graphics component for high score table
class ScoreTable(entity.Component):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				pass
			else:
				pass


	def __init__(self,game, data):
		super(ScoreTable, self).__init__(game)
		self.render_layer = data["RenderLayer"]
		self.font_manager = data["FontManager"]
		self.font = self.font_manager.addFontFromFile("Fonts/Silom/Silom.ttf", 20)


	def draw(self, data, common_data):
		for i, image in enumerate(data.images):
			self.render_layer.queueImage(image, 85, 270-i*20, 0)

	def update(self, data, common_data, dt):
		if common_data.game.game_mode == PacBun.eGameModes.high_score:
			common_data.blink=False
		else:
			common_data.blink=True

	def initScore(self, common_data):
		common_data.blink=True
		graphics_data = common_data.entity.graphics_data
		graphics_data.images = []

		graphics_data.images.append(
			self.render_layer.addImageFromString(font_manager=self.font_manager, string="     Best Buns", font=self.font,
																					 color=sdl2.SDL_Color(0, 0, 0, 255)))

		graphics_data.scores_data = common_data.entity.controller_data.scores_data	# hold a pointer to the scores in the controller
		for i in range(0,10):
			r,g,b = (
				(255,255,0),
				(255, 0, 255),
				(0, 255, 255),
				(255, 0, 0),
				(0, 255, 0),
				(0, 0, 255),
				(255, 255, 255),
				(128, 128, 255),
				(255, 128, 128),
				(128, 255, 128),
			)[i]
			score = "{0:0=2d}: ".format(i+1) + " {0:0=4d} ".format(graphics_data.scores_data[i][1]) + str(graphics_data.scores_data[i][0])
			graphics_data.images.append(self.render_layer.addImageFromString(font_manager= self.font_manager, string=score, font=self.font, color=sdl2.SDL_Color(r,g,b,255)))



	def updateImages(self):
		pass
		# self.scores = []
		# for i in range(0,10):
		# 	self.scores.append(Score(f"{self.score_data[i].initials}: "+ "{0:0=4d}".format(self.current_score)), None)
		# # render the scores
		# for index, score in enumerate(self.scores):
		# 	self.render_layer.replaceImageFromString(self.font_manager, "{0:0=4d}".format(self.current_score), size=10)
		# 	self.overlay_renlayer.replaceImageFromMessage(message=self.message, old_image=self.score_image)

def makeGraphics(manager, render_layer, font_manager):
	return manager.makeTemplate({
			"Name": "Scoreboard",
			"Template": ScoreTable,
			"RenderLayer": render_layer,
			"FontManager": font_manager,
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

			self.scores_data = []

			# load high score from json file
			with open('scores.json') as json_file:
				scores_data = json.load(json_file)
				for i in range(0,10):
					self.scores_data.append(scores_data["scores"][i])
					print(self.scores_data[i])

	def __init__(self, game, data):
		super(Controller, self).__init__(game)

	def update(self, data, common_data, dt):
		pass

	def updateScores(self, data, common_data, new_score):
		pass



