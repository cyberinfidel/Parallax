import sdl2

import px_entity
# import text
import px_graphics
import px_controller
import px_vector



# stub for sounds
def makeSounds(manager, mixer):
	return None
	# return manager.makeTemplate()

# end sounds ####################################################

# graphics component for displaying a message
class MessageBox(px_entity.Component):
	def initEntity(self, entity, data=False):
		entity.image = None
		entity.ren_layer = data['ren_layer']
		# data.message = message
		entity.color = data['color']
		entity.duration = data['duration']
		entity.message = data['message']
		entity.font = data['font']
		entity.duration = data['duration']
		if entity.duration<0:
			entity.permanent = 0
			entity.duration = 1
		else:
			entity.permanent = 1

		entity.fade = 0
		entity.fade_direction = 1
		entity.fade_speed = data['fade_speed']
		entity.align = data['align']
		# actually draw message
		self._renderMessage(entity)

	def _renderMessage(self, data):
		# draw message and add to/replace in render layer's images
		if not data.image:
			data.image = data.ren_layer.addImageFromString(string = data.message,
																										 font=data.font,
																										 color=data.color,
																											 )
		else:
			data.ren_layer.replaceImageFromString(old_image = data.image,
																				string=data.message,
																				font=data.font,
																				color=data.color,
																						)


		def setMessage(self, data, message):
			data.message = message
			self._renderMessage(data)

	def setMessage(self, data, message):
		data.message = message
		self._renderMessage(data)

	def __init__(self, game, data):
		super(MessageBox, self).__init__(game)

	def draw(self, entity):
		offset_x=0
		offset_y=0
		if entity.align==px_graphics.eAlign.centre:
			offset_x,offset_y = entity.ren_layer.getImageDimensions(entity.image)
			offset_x/=2
			offset_y/=2
		elif entity.align==px_graphics.eAlign.centre:
			offset_x,offset_y = entity.ren_layer.getImageDimensions(entity.image)

		return entity.ren_layer.queueImage(
			image = entity.image,
			x = entity.pos.x-offset_x,
			y = entity.pos.y-offset_y,
			z = entity.pos.z,
			color = entity.color * px_graphics.Color(1, 1, 1, entity.fade)
		)

	def update(self, entity, dt):
		entity.fade+=dt*entity.fade_direction*(1/entity.fade_speed)
		entity.fade = px_vector.clamp(0, entity.fade, 1)
		entity.duration -=dt*entity.permanent
		if entity.duration<1:
			entity.fade_direction=-1
		if entity.duration<0:
			entity.setState(px_entity.eStates.dead)

	def process(self, entity, command, args):
		if command=='fade out':
			entity.fade_direction = -1
			entity.duration = args[0]


def makeGraphics(manager, render_layer):
	return manager.makeTemplate({
		"Name": "Message",
		"Template": MessageBox,
		"RenderLayer": render_layer,
	})



# end graphics ####################################################

# todo: remove this? doesn't seem to do anything
def makeController(manager):
	return manager.makeTemplate({"Template": Controller})
class Controller(px_controller.Controller):
	class Data(object):
		def __init__(self, entity, init=False):
			pass

	def __init__(self, game, data):
		super(Controller, self).__init__(game)

	def update(self, entity, dt):
		pass

# end controller ####################################################