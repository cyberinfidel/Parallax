import json

import px_entity
import px_controller
import px_graphics
import PacBun



# class HighScore(object):
# 	def __init__(self, score, image):
# 		self.score = score
# 		self.image = image

def init(entity):
	entity.images = []

	for i in range(0, 10):
		score, r, g, b = formatScore(i, entity.scores_data[i][0], entity.scores_data[i][1])
		# todo: make this a little less hacky
		graphics = entity.getComponent('graphics')
		entity.images.append(
			graphics.render_layer.addImageFromString(string=score, font=graphics.font, color=px_graphics.Color(r, g, b, 1)))

def formatScore(index, initials, score):
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


# graphics component for high score table
class ScoreTable(px_entity.Component):
	def __init__(self, game, data):
		super(ScoreTable, self).__init__(game)
		self.render_layer = data["RenderLayer"]
		self.font = self.render_layer.addFont("Fonts/PacBun/PacBun.ttf", 32)

	def draw(self, entity):
		for i, image in enumerate(entity.images):
			self.render_layer.queueImage(image, 85, 270-i*20, 0)

	def update(self, entity, dt):
		pass

	def updateScores(self, entity):
		for i in range(0,10):
			score, r, g, b = self.formatScore(i,entity.scores_data[i][0],entity.scores_data[i][1])
			self.render_layer.replaceImageFromString(entity.images[i], string=score, font=self.font, color=px_graphics.Color(r, g, b, 255))


def makeGraphics(manager, render_layer):
	return manager.makeTemplate({
			"Name": "Scoreboard",
			"Template": ScoreTable,
			"RenderLayer": render_layer,
		})

###########################################################

def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(px_controller.Controller):
	def initEntity(self, entity, data=False):
			# entity.scores_data = []
			# load high score from json file
			with open('scores.json') as json_file:
				entity.scores_data = json.load(json_file)

	def __init__(self, game, data):
		super(Controller, self).__init__(game)

	def update(self, entity, dt):
		pass

	def isHighScore(self, entity, new_score):
		score_data = entity.scores_data
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


