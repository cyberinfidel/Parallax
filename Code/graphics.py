# external lib import
import enum
import os
import ctypes

# import sdl libs
import sdl2.ext
import sdl2.sdlimage as sdl_image
# import sdl2.sdlgfx as sdl_gfx


# initialise for loading PNGs and JPGs
sdl_image.IMG_Init(sdl_image.IMG_INIT_PNG)
sdl_image.IMG_Init(sdl_image.IMG_INIT_JPG)

# import my files
from entity import eStates, Component
from vector import Vec3, rand_num
from log import log
import text

# globals
graphics_debug = False

# Individual images for use as frames for animations or as part of the background etc.
# Based on SDL images for the moment with no atlassing etc.
class Image(object):
	def __init__(self, ren, texture, width, height, file=None, src=None):
		self.renderer = ren
		self.file = file
		self.width = width
		self.height = height
		if src:
			self.src = src
		else:
			self.src = sdl2.SDL_Rect(0, 0, self.width, self.height)
		self.texture = texture
		self.ref_count = 1

	@classmethod
	def fromFile(cls, ren, file, width=None, height=None):

		# get image into surface (don't need to keep this though)
		surface = sdl_image.IMG_Load(file.encode("utf-8"))

		# make a texture from the apple surface (for HW rendering)
		texture = sdl2.SDL_CreateTextureFromSurface(ren.renderer, surface)

		if not (width and height):
			width = surface.contents.w
			height = surface.contents.h

		sdl2.SDL_FreeSurface(surface)
		return cls(ren.renderer, texture, width, height, file)

	@classmethod
	def fromTexture(cls, ren, texture, width, height):
		cls.file = None
		return cls(ren.renderer, texture, width, height)

	############################################################

	def draw(self, x, y, debug=graphics_debug):

		sdl2.SDL_RenderCopy(self.renderer, self.texture, self.src,
												sdl2.SDL_Rect(int(x), int(y), self.width, self.height))

		if debug:
			# draw the outline of the image for debugging purposes
			sdl2.SDL_SetRenderDrawColor(self.renderer,255,255,255,50)
			sdl2.SDL_SetRenderDrawBlendMode(self.renderer,sdl2.SDL_BLENDMODE_ADD)

			sdl2.SDL_RenderDrawRect(self.renderer,sdl2.SDL_Rect(int(round(x)), int(round(y)), self.width, self.height))

	############################################################

	# try to delete (with ref counting)
	# if actually deleted returns True
	def release(self):
		self.ref_count -=1
		if self.ref_count<=0:
			self.delete()
			return True
		return False


	# actually delete, no ref counting
	def delete(self):
		sdl2.SDL_DestroyTexture(self.texture)
		self.ref_count=0


############################################################
# end Image
############################################################

class Shape(object):
	def __init__(self, ren, origin_x=0, origin_y=0, colour=False):
		self.renderer = ren
		self.colour = colour
		self.origin_x = origin_x
		self.origin_y = origin_y

class Circle(Shape):

	def draw(self, x, y):
		pass


class Drawable(object):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def getY(self):
		return self.y

	def getZ(self):
		return self.z

	def getZThenY(self):
		return self.z*1000+self.y

	def getDrawDepth(self):
		return self.z

class RenderImage(Drawable):
	def __init__(self, image, x, y, z):
		super(RenderImage, self).__init__(x,y,z)
		self.image = image

	# draws an image paying attention to the passed origin (should be the render layer origin, not the image's)
	def draw(self, origin, screen_height):
		self.image.draw(self.x - origin.x, screen_height - (self.y + self.z - origin.y - origin.z))

class RenderShape(Drawable):
	def __init__(self, shape, x, y, z):
		super(RenderShape, self).__init__(x,y,z)
		self.shape = shape

	# draws a shape paying attention to the passed origin (should be the render layer origin, not the shape's)
	def draw(self, origin):
		self.shape.draw(self.x - origin.x, self.y + self.z - origin.y - origin.z)

class RenderText(Drawable):
	def __init__(self, message_text, x, y, z):
		super(RenderText, self).__init__(x,y,z)

# a collection of images that can be added to a list of drawables that will be drawn when told to render
class RenderLayer(object):
	def __init__(self, ren):
		self.ren = ren

		self.images = []
		self.drawables = []

		self.origin = Vec3(0,0,0)

		self.fontmanager = text.FontManager(self.ren)
		self.default_font=0



	def _getNextEmptySlot(self):
		for index, image in enumerate(self.images):
			if not image:			# empty slot
				return index
		self.images.append(None)
		return len(self.images)-1


	# add an image from something rendered in the program
	# e.g. text from a font
	# note: not so much error checking - this needs to be quick
	# also: this is intended for text that will be shown more than once
	def addImageFromMessage(self, message):
		index = self._getNextEmptySlot()
		self.images[index] = Image.fromTexture(self.ren,message.texture, message.width, message.height)
		return index

	def addImageFromString(self, font_manager, string, font=0, color=sdl2.SDL_Color(255,255,255,255)):
		message = text.Message.withRender(font_manager=font_manager, font=font, string=string, color=color)
		index = self._getNextEmptySlot()
		self.images[index] = Image.fromTexture(self.ren,message.texture, message.width, message.height)
		return index

	def replaceImageFromMessage(self, old_image,  message):
		self.images[old_image].delete()
		self.images[old_image] = Image.fromTexture(self.ren,message.texture, message.width, message.height)

	def replaceImageFromString(self, old_image, font_manager, string, font=0, color=sdl2.SDL_Color(255,255,255,255)):
		message = text.Message.withRender(font_manager=font_manager, string=string, font=font, color=color)
		self.images[old_image].delete()
		self.images[old_image] = Image.fromTexture(self.ren,message.texture, message.width, message.height)

	# add to the store of images available in this render layer
	def addImageFromFile(self, file):
		# find if this file has been loaded before and return that if so
		# also check if there's an index that is empty and can be re-used
		filepath = os.path.abspath(file)
		for index, image in enumerate(self.images):
			if image:
				if image.file == filepath:
					image.ref_count+=1
					return index

		# otherwise find next empty slot (or append)
		index = self._getNextEmptySlot()
		try:
			self.images[index] = Image.fromFile(self.ren, filepath)
		except Exception as e:
			log("Problem loading image for frame: " + str(e) + " file:" + filepath)

		return index

	# empty the list of drawables for this layer so nothing is set to be drawn on a render event
	def clear(self):
		self.drawables = []  # note this replaces list with empty list and doesn't delete any of the contents of list

	# add an image to the list of drawables to be drawn on a render
	def queueImage(self, image, x, y, z):
		self.drawables.append(RenderImage(self.images[image], x, y, z))

	def getScreenHeight(self):
		# get screen dimensions entirely so can draw from bottom left instead of top left
		# increasing z or y should go up...
		screen_width = ctypes.c_int(0)
		screen_height = ctypes.c_int(0)
		sdl2.SDL_RenderGetLogicalSize(self.ren.renderer,ctypes.byref(screen_width),ctypes.byref(screen_height))
		return int(screen_height.value)

	# draws the drawables queue and clears it
	def render(self):
		screen_height = self.getScreenHeight()
		for d in self.drawables:
			d.draw(origin=self.origin, screen_height=screen_height)
		self.drawables = []

	# renders the drawables queue, but in an order: lower Y last (illusion of front to back)
	# TODO: pass in comparison and allow different orders - not as easy as first thought
	def renderSorted(self):
		screen_height = self.getScreenHeight()
		for d in sorted(self.drawables, key = Drawable.getDrawDepth, reverse=True):
			d.draw(origin=self.origin, screen_height=screen_height)
		self.drawables = []

	def renderSortedByZThenY(self):
		screen_height = self.getScreenHeight()
		for d in sorted(self.drawables, key = Drawable.getZThenY, reverse=True):
			d.draw(origin=self.origin, screen_height=screen_height)
		self.drawables = []

	# sets the origin of where the renderlayer draws from i.e. position of layer
	def setOriginX(self, x):
		self.origin.x = x
	def setOriginZ(self, z):
		self.origin.z = z
	def setOriginY(self, y):
		self.origin.y = y
	def setOrigin(self, x, y, z):
		self.origin.x = x
		self.origin.y = y
		self.origin.z = z
	def setOriginByVec3(self, vec):
		self.origin = vec


	def getOriginX(self):
		return self.origin.x
	def getOriginY(self):
		return self.origin.y
	def getOriginZ(self):
		return self.origin.z
	def getOrigin(self):
		return self.origin

	# releases an image with ref counting
	def releaseImage(self, index):
		self.images[index].release()

	# kills whole render layer and all images, dead
	def delete(self):
		for image in self.images:
			image.delete()

# add a font that this Render Layer can use
	def addFont(self, font_path):
		self.fonts.append(text.Font(self.ren, "Fonts/space-mono/SpaceMono-Bold.ttf"))
		return len(self.fonts)-1

	def queueMessageFromText(self, message_text, x, y, font=None, size= None):
		if not font:
			font = self.default_font
		self.addImageFromMessage(text.Message.withRender(font, message_text))

	# takes all textures already submitted and makes into an atlas
	# uses dumbest algorithm possible atm
	# speed up success by giving the correct start size for the atlas
	def makeAtlas(self, start_size=256):
		# tries this size and increases dimensions until the images all fit
		atlas_dim=start_size
		while not self._renderAtlas(atlas_dim, dry_run=True):
			atlas_dim=int( atlas_dim + 256)

		# actually render atlas - do again with rendering and updating the image records
		self._renderAtlas(atlas_dim, dry_run=False)
		self.atlas_dim = atlas_dim
		log(f"Graphics|RenderLayer:Atlas created at size: {self.atlas_dim}")

	# adds all existing images to a texture atlas. Updates the image objects to point to the
	# atlas texture and their src variables to where in the texture they are
	def _renderAtlas(self, atlas_dim, dry_run, gap=0):
		if not dry_run:
			# make the atlas texture
			self.TA = sdl2.SDL_CreateTexture(self.ren.renderer, sdl2.SDL_PIXELFORMAT_RGBA8888, sdl2.SDL_TEXTUREACCESS_TARGET, atlas_dim, atlas_dim)
			# point drawing at the atlas and clear it
			sdl2.SDL_SetRenderTarget(self.ren.renderer, self.TA)
			sdl2.SDL_SetRenderDrawColor(self.ren.renderer, 0, 0, 0, 0)
			sdl2.SDL_RenderClear(self.ren.renderer)
			sdl2.SDL_SetRenderDrawColor(self.ren.renderer,255,255,255,255)

		# draws textures in rows, left to right, then top to bottom
		accum_x=0 # where we've got to across TA
		max_y = 0 # how tall the row is so we know where to start the next one
		accum_y=0	# how far down the current row is
		for index, image in enumerate(self.images):
			if accum_x+image.width+gap>atlas_dim:	# will this image go off right of atlas?
				accum_x=0
				# push down
				accum_y+=max(max_y,image.height)+gap # in case this is the tallest image
				max_y=0

			if not dry_run: # draw into atlas
				# and update the image to point to where it went in the atlas
				image.draw(accum_x, accum_y)
				# replace Image object with one that points to TA
				# could just update in place, but this seems as easy
				self.images[index]= Image(self.ren.renderer,
																		self.TA,
																		width=image.width,
																		height=image.height,
																		file=image.file,
																		src=sdl2.SDL_Rect(accum_x, accum_y, image.width, image.height))
				image.delete()	# kill off old image

			accum_x+=image.width+gap
			max_y=max(max_y,image.height)
			if accum_y+max_y>atlas_dim:
				log(f"Atlas overflow at size {atlas_dim}")
				return False

		if not dry_run:
			# point drawing at screen again
			sdl2.SDL_SetRenderTarget(self.ren.renderer, None)
			sdl2.SDL_SetTextureBlendMode(self.TA, sdl2.SDL_BLENDMODE_BLEND)
		return True

	def dumpAtlasToFiles(self, image_file, data_file):
		format = sdl2.SDL_PIXELFORMAT_RGBA8888

		surface = sdl2.SDL_CreateRGBSurfaceWithFormat(0, self.atlas_dim, self.atlas_dim, 32, format)
		sdl2.SDL_LockSurface(surface)
		sdl2.SDL_SetRenderTarget(self.ren.renderer, self.TA)
		sdl2.SDL_RenderReadPixels(self.ren.renderer,
																			 sdl2.SDL_Rect(0,0,self.atlas_dim,self.atlas_dim),
																			 format,
																			 surface.contents.pixels,
																			 surface.contents.pitch)
		sdl2.SDL_UnlockSurface(surface)


		sdl_image.IMG_SavePNG(surface.contents, image_file.encode("utf-8"))
		sdl2.SDL_SetRenderTarget(self.ren.renderer, None)
		return True

	def loadAtlasFromFiles(self, image_file, data_file):
		pass

####################################################
# end of RenderLayer
####################################################

# Types of graphics components available
class GraphicsTypes(enum.IntEnum):
	single_image = 0,
	single_anim = 1,
	multi_anim = 2,
	text_message = 3,
	num_graphics_types = 4

# graphics component for a single static image
class SingleImage(Component):
	def __init__(self, game, data):
		super(SingleImage, self).__init__(game)
		self.rl = data['RenderLayer']
		self.image = self.rl.addImageFromFile(data["Image"][0])
		self.origin_x = data["Image"][1]
		self.origin_y = data["Image"][2]
		self.origin_z = data["Image"][3]
		self.name = data["Name"]

	def getImage(self):
		return self.image

	def draw(self, data, common_data):
		return self.rl.queueImage(self.image, common_data.pos.x - self.origin_x, common_data.pos.y + self.origin_y, common_data.pos.z + self.origin_z)

	def hasShadow(self):
		return False

	def update(self, data, common_data, time):
		pass

# graphics component for multiple static images
class MultiImage(Component):
	def __init__(self, game, data):
		super(MultiImage, self).__init__(game)
		self.rl = data['RenderLayer']
		self.images = []
		for image in data["Images"]:
			self.images.append(AnimFrame(self.rl.addImageFromFile(image[0]), image[1], image[2], image[3], 0))

	def getImage(self):
		return self.image

	def draw(self, data, common_data):
		for image in self.images:
			self.rl.queueImage(image.image, common_data.pos.x - image.origin_x, common_data.pos.y + image.origin_y, common_data.pos.z + image.origin_z)
		return True

	def hasShadow(self):
		return False

	def update(self, data, common_data, time):
		pass


# graphics component for a single animation only
class SingleAnim(Component):
	class Data(object):
		def __init__(self, common_data):
			self.current_frame = 0
			self.current_time = 0

	def __init__(self, game, data):
		super(SingleAnim, self).__init__(game)
		self.rl = data['RenderLayer']
		self.anim = data['Anims'][0]['AnimType'](self.rl, data["Anims"][0]["Frames"])
		self.name = data["Name"]

	def getAnim(self):
		return self.anim

	def update(self, data, common_data, time):
		self.anim.advanceAnim(data, time)

	def draw(self, data, common_data):
		frame = self.anim[0]
		return self.rl.queueImage(frame.image, common_data.pos.x - frame.origin_x, common_data.pos.y + frame.origin_y, common_data.pos.z + frame.origin_z)

	def hasShadow(self):
		return False


# graphics component for multiple animations
class MultiAnim(Component):
	class Data(object):
		def __init__(self, common_data, init=False):
			if init:
				self.current_frame = init.current_frame
				self.current_time = init.current_time
				self.current_anim = init.current_anim
				self.current_state = init.current_anim
			else:
				self.current_frame = 0
				self.current_time = 0
				self.current_anim =  eStates.stationary
				self.current_state = eStates.stationary

	def delete(self, data):
		for anim in self.anims:
			self.anims[anim].delete()

	def __init__(self, game, data):
		super(MultiAnim, self).__init__(game)
		self.rl = data['RenderLayer']
		self.anims = {}

		# parse data for single pass initialisation
		self.name = data["Name"]
		for anim in data["Anims"]:
			for state in anim["States"]:
				self.anims[state] = anim['AnimType'](self.rl, anim["Frames"])

	def update(self, data, common_data, time):
		if common_data.new_state:
			common_data.new_state=False
			data.current_anim = common_data.state
			data.current_state = common_data.state
			self.startAnim(data, 0) # TODO allow some anims to begin from different frame
		self.anims[data.current_anim].advanceAnim(data, time)

	def startAnim(self, data, frame=0):
		data.current_time = 0
		data.current_frame = frame

	def draw(self, data, common_data):
		frame = self.anims[data.current_anim].getCurrentFrame(data)
		return self.rl.queueImage(frame.image, common_data.pos.x - frame.origin_x, common_data.pos.y + frame.origin_y, common_data.pos.z + frame.origin_z)

	def hasShadow(self):
		return eStates.shadow in self.anims

	def drawShadow(self, data, common_data, shadow_height=0):

		# todo: work out why y=0 doesn't work
		# todo: shrink shadow the higher y is
		# todo: allow shadows that aren't all at y=0
		frame = self.anims[eStates.shadow].getCurrentFrame(data)
		return self.rl.queueImage(frame.image, common_data.pos.x - frame.origin_x + shadow_height, frame.origin_y, common_data.pos.z)

# graphics component for a single static image
class TextMessage(Component):
	def __init__(self, game, data):
		super(TextMessage, self).__init__(game)
		self.rl = data['RenderLayer']
		self.image = self.rl.addImageFromFile(data["Image"][0])
		self.origin_x = data["Image"][1]
		self.origin_y = data["Image"][2]
		self.origin_z = data["Image"][3]
		self.name = data["Name"]

	def getImage(self):
		return self.image

	def draw(self, data, common_data):
		return self.rl.queueImage(self.image, common_data.pos.x - self.origin_x, common_data.pos.y + self.origin_y, common_data.pos.z + self.origin_z)

	def hasShadow(self):
		return False

	def update(self, data, common_data, time):
		pass

#####################################################################
# Animation code																										#
#####################################################################

class Anim(object):
	def __init__(self, render_layer):
		self.frames = []
		self.render_layer = render_layer

	def addFrame(self, image, duration):
		self.frames.append(AnimFrame(image, duration))

	def addFrames(self, render_layer, frames):
		for frame in frames:
			self.frames.append(AnimFrame(render_layer.addImageFromFile(frame[0]), frame[1], frame[2], frame[3], frame[4]))

	def getCurrentFrame(self, data):
		return self.frames[data.current_frame]

	def delete(self):
		for frame in self.frames:
			self.render_layer.releaseImage(frame.image)

# trivial, single frame animation
class AnimSingle(Anim):
	def __init__(self, rl, frames):
		super(AnimSingle, self).__init__(rl)
		self.addFrames(rl, frames)

	def getCurrentFrame(self, data):
		return self.frames[0]

	def advanceAnim(self,anim_instance, time):
		pass


# simple looping animation
class AnimLoop(Anim):
	def __init__(self, rl, frames):
		super(AnimLoop, self).__init__(rl)
		self.addFrames(rl, frames)

	def advanceAnim(self, anim_instance, time):
		anim_instance.current_time += time
		while anim_instance.current_time > self.frames[anim_instance.current_frame].time:
			anim_instance.current_time -= self.frames[anim_instance.current_frame].time
			anim_instance.current_frame += 1
			if anim_instance.current_frame >= len(self.frames):
				anim_instance.current_frame = 0

# simple non-looping animation
class AnimNoLoop(Anim):
	def __init__(self, rl, frames):
		super(AnimNoLoop, self).__init__(rl)
		self.addFrames(rl, frames)

	def advanceAnim(self, anim_instance, time):
		anim_instance.current_time += time
		while anim_instance.current_time > self.frames[anim_instance.current_frame].time:
			anim_instance.current_time -= self.frames[anim_instance.current_frame].time
			anim_instance.current_frame += 1
			if anim_instance.current_frame >= len(self.frames):
				anim_instance.current_frame -= 1	# push back to last frame again

# simple choose a frame at random animation
class AnimRandom(Anim):
	def __init__(self, rl, frames):
		super(AnimRandom, self).__init__(rl)
		self.addFrames(rl, frames)

	def advanceAnim(self, anim_instance, time):
		anim_instance.current_time += time
		while anim_instance.current_time > self.frames[anim_instance.current_frame].time:
			anim_instance.current_time -= self.frames[anim_instance.current_frame].time
			anim_instance.current_frame = rand_num(len(self.frames))

# container for a single frame of animation
class AnimFrame:
	def __init__(self, image, origin_x, origin_y, origin_z, time):
		self.image = image
		self.origin_x = origin_x
		self.origin_y = origin_y
		self.origin_z = origin_z
		self.time = time


####################################################################################
def runTests():


	fails=[]

	res_x = 320
	res_y = 200
	zoom = 2

	# Initialize the video system - this implicitly initializes some
	# necessary parts within the SDL2 DLL used by the video module.
	#
	# You SHOULD call this before using any video related methods or
	# classes.
	sdl2.ext.init()

	# Create a new window (like your browser window or editor window,
	# etc.) and give it a meaningful title and size. We definitely need
	# this, if we want to present something to the user.

	window = sdl2.ext.Window("Graphics Tests", size=(res_x * zoom, res_y * zoom))  # ,flags=sdl2.SDL_WINDOW_FULLSCREEN)

	# By default, every Window is hidden, not shown on the screen right
	# after creation. Thus we need to tell it to be shown now.
	window.show()

	# set up a renderer to draw stuff. This is a HW accelerated one.
	# Switch on VSync to avoid running too fast
	# and wasting power and keep graphics nice and clean
	ren = sdl2.ext.Renderer(window, flags=sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC)
	# makes zoomed graphics blocky (for retro effect)
	sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"nearest")
	# makes the graphics look and act like Atari ST screen size, even though rendered much larger
	sdl2.SDL_RenderSetLogicalSize(ren.renderer, res_x, res_y)

	# test 1 example
	# if not (a+b)==Vec3(2,3,4):
	# 	log("Fail in test 1: a+b")
	# 	fails.append(1)

	rl = RenderLayer(ren)

	rl.setOrigin(1,2,3)
	if(rl.getOrigin()!=Vec3(1,2,3)):
		fails.append(1)

	rl.setOriginByVec3(Vec3(1,2,3))
	if(rl.getOrigin()!=Vec3(1,2,3)):
		fails.append(2)



	return fails

if __name__ == "__main__":
	import sys
	sys.exit(runTests())
