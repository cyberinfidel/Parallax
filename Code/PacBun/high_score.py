import json

import entity
import controller
import graphics
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
		self.font = self.render_layer.addFont("Fonts/PacBun/PacBun.ttf", 32)


	def draw(self, data, common_data):
		for i, image in enumerate(data.images):
			self.render_layer.queueImage(image, 85, 270-i*20, 0)

	def update(self, data, common_data, dt):
		if common_data.game.game_mode == PacBun.eGameModes.high_score:
			common_data.blink=False
		else:
			common_data.blink=True

	def formatScore(self, index, initials, score):
		r, g, b = (
			(1, 1, 0),
			(1, 0, 1),
			(0, 1, 1),
			(1, 0, 0),
			(0, 1, 0),
			(0, 0, 1),
			(1, 1, 1),
			(0.5, 0.5, 1),
			(1, 0.5, 0.5),
			(0.5, 1, 0.5),
		)[index]
		return "{0:0=2d}: ".format(index+1) + " {0:0=4d} ".format(score) + str(initials), r,g,b


	def initScore(self, common_data):
		common_data.blink=True
		graphics_data = common_data.entity.graphics_data
		graphics_data.images = []

		scores_data = common_data.entity.controller_data.scores_data	# hold a pointer to the scores in the controller
		for i in range(0,10):
			score, r, g, b = self.formatScore(i,scores_data[i][0],scores_data[i][1])
			graphics_data.images.append(self.render_layer.addImageFromString(string=score, font=self.font, color=graphics.Color(r, g, b, 1)))



	def updateScores(self, entity):
		scores_data = entity.controller_data.scores_data	# hold a pointer to the scores in the controller

		for i in range(0,10):
			score, r, g, b = self.formatScore(i,scores_data[i][0],scores_data[i][1])
			self.render_layer.replaceImageFromString(entity.graphics_data.images[i], string=score, font=self.font, color=graphics.Color(r, g, b, 255))


def makeGraphics(manager, render_layer):
	return manager.makeTemplate({
			"Name": "Scoreboard",
			"Template": ScoreTable,
			"RenderLayer": render_layer,
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

			self.scores_data = []

			# load high score from json file
			with open('scores.json') as json_file:
				self.scores_data = json.load(json_file)

	def __init__(self, game, data):
		super(Controller, self).__init__(game)

	def update(self, data, common_data, dt):
		pass

	def isHighScore(self, entity, new_score):
		score_data = entity.controller_data.scores_data
		if new_score>score_data[9][1]:
			return True
		return False

	def updateScores(self, score_data, initials, new_score):
		for i in range(0,10):
			if new_score > score_data[i][1]:
				score_data[i:i] = [[initials,new_score]]
				break

		score_data = score_data[:10]	# chop of last place score

		# write scores back to disk
		with open('scores.json', 'w') as outfile:
			json.dump(score_data, outfile)

		return score_data

	# def isHighScore(self, entity, new_score):
	# 	data = entity.controller_data
	# 	if new_score>data.scores_data[9][1]:
	# 		print("High score!!!")
	# 		self.updateScores(data=data, initials="NEW", new_score=new_score)
	#
	# def updateScores(self, data, initials, new_score):
	# 	for i in range(0,10):
	# 		if new_score > data.scores_data[i][1]:
	# 			data.scores_data.insert(i,[initials,new_score])
	# 		data.scores_data=data.scores_data[:10]
	# 	print(data.scores_data)


