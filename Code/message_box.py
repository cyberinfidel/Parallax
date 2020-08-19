import sdl2

import entity
# import text
import graphics
import controller
import vector



# stub for sounds
def makeSounds(manager, mixer):
	return None
	# return manager.makeTemplate()

# end sounds ####################################################

# graphics component for displaying a message
class MessageBox(entity.Component):
	class Data(object):
		def __init__(self, common_data, init=False):
			self.image = None

	def init(self, data, ren_layer, message, font=0, color=graphics.Color(1, 1, 1, 1), duration=0):
		data.ren_layer = ren_layer
		# data.message = message
		data.color = color
		data.duration = duration
		data.message = message
		data.font = font
		data.duration = duration
		data.fade = 0
		data.fade_direction = 1

		# actually draw message
		self._renderMessage(data)

	def _renderMessage(self, data):
		# draw message and add to/replace in render layer's images
		if not data.image:
			data.image = data.ren_layer.addImageFromString(string = data.message,
																										 font=data.font,
																										 color=data.color
																											 )
		else:
			data.ren_layer.replaceImageFromString(old_image = data.image,
																				string=data.message,
																				font=data.font,
																				color=data.color
																				)


		def setMessage(self, data, message):
			data.message = message
			self._renderMessage(data)

	def setMessage(self, data, message):
		data.message = message
		self._renderMessage(data)

	def __init__(self,game, data):
		super(MessageBox, self).__init__(game)

	def draw(self, data, common_data):
		return data.ren_layer.queueImage(
			image = data.image,
			x = common_data.pos.x,
			y = common_data.pos.y,
			z = common_data.pos.z,
			color = data.color*graphics.Color(1,1,1,data.fade)
		)

	def update(self, data, common_data, dt):
		data.fade+=dt*data.fade_direction*2
		data.fade = vector.clamp(0,data.fade,1)
		data.duration -=dt
		if data.duration<1:
			data.fade_direction=-1
		if data.duration<0:
			common_data.entity.setState(entity.eStates.dead)



def makeGraphics(manager, render_layer):
	return manager.makeTemplate({
		"Name": "Message",
		"Template": MessageBox,
		"RenderLayer": render_layer,
	})



# end graphics ####################################################

def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(controller.Controller):
	class Data(object):
		def __init__(self, common_data, init=False):
			pass

	def __init__(self, game, data):
		super(Controller, self).__init__(game)

	def update(self, data, common_data, dt):
		pass

# end controller ####################################################