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

# globals
graphics_debug = False

# Individual images for use as frames for animations or as part of the background etc.
# Based on SDL images for the moment with no atlassing etc.
class Image(object):
	def __init__(self, ren, file, width=False, height=False):
		self.renderer = ren.renderer
		self.file = file

		# get image into surface (don't need to keep this though)
		surface = sdl_image.IMG_Load(file.encode("ascii"))

		# make a texture from the apple surface (for HW rendering)
		self.texture = sdl2.SDL_CreateTextureFromSurface(self.renderer, surface)

		if not (width and height):
			self.width = surface.contents.w
			self.height = surface.contents.h
		else:
			self.width = width
			self.height = height

		self.src = sdl2.SDL_Rect(0, 0, self.width, self.height)


	def draw(self, x, y, debug=graphics_debug):

		sdl2.SDL_RenderCopy(self.renderer, self.texture, self.src,
												sdl2.SDL_Rect(int(round(x)), int(round(y)), self.width, self.height))

		if debug:
			# draw the outline of the image for debugging purposes
			sdl2.SDL_SetRenderDrawColor(self.renderer,255,255,255,50)
			sdl2.SDL_SetRenderDrawBlendMode(self.renderer,sdl2.SDL_BLENDMODE_ADD)

			sdl2.SDL_RenderDrawRect(self.renderer,sdl2.SDL_Rect(int(round(x)), int(round(y)), self.width, self.height))


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

# a collection of images that can be added to a list of drawables that will be drawn when told to render
class RenderLayer(object):
	def __init__(self, ren):
		self.ren = ren

		self.images = []
		self.drawables = []

		self.origin = Vec3(0,0,0)

	# add to the store of images available in this render layer
	def addImage(self, file):
		# find if this file has been loaded before and return that if so
		filepath = os.path.abspath(file)
		for index, image in enumerate(self.images):
			if image.file == filepath:
				return index

		# haven't seen this file before so add it and return new index
		try:
			self.images.append(Image(self.ren, filepath))
		except Exception as e:
			log("Problem loading image for frame: "+str(e)+" file:"+filepath)
		return len(self.images) - 1

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
		for d in sorted(self.drawables, key = Drawable.getY, reverse=True):
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


# Types of graphics components available
class GraphicsTypes(enum.IntEnum):
	single_image = 0,
	single_anim = 1,
	multi_anim = 2,
	num_graphics_types = 3

# graphics component for a single static image
class SingleImage(Component):
	def __init__(self, game, data):
		super(SingleImage, self).__init__(game)
		self.rl = data['RenderLayer']
		self.image = self.rl.addImage(data["Image"][0])
		self.origin_x = data["Image"][1]
		self.origin_y = data["Image"][2]

	def getImage(self):
		return self.image

	def draw(self, data, common_data):
		return self.rl.queueImage(self.image, common_data.pos.x - self.origin_x, common_data.pos.y, common_data.pos.z + self.origin_y)

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
		return self.rl.queueImage(frame.image, common_data.pos.x - frame.origin_x, common_data.pos.y, common_data.pos.z + frame.origin_y)

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
		try:
			frame = self.anims[data.current_anim].getCurrentFrame(data)
			return self.rl.queueImage(frame.image, common_data.pos.x - frame.origin_x, common_data.pos.y, common_data.pos.z + frame.origin_y)
		except Exception as e:
			log(e)
			exit(1)

	def hasShadow(self):
		return eStates.shadow in self.anims

	def drawShadow(self, data, common_data):

		# todo: work out why z=0 doesn't work
		# todo: shrink shadow the higher z is
		# todo: allow shadows that aren't all at z=0
		frame = self.anims[eStates.shadow].getCurrentFrame(data)
		return self.rl.queueImage(frame.image, common_data.pos.x - frame.origin_x, common_data.pos.y, frame.origin_y)


#####################################################################
# Animation code																										#
#####################################################################

class Anim(object):
	def __init__(self):
		self.frames = []

	def addFrame(self, image, duration):
		self.frames.append(AnimFrame(image, duration))

	def addFrames(self, render_layer, frames):
		for frame in frames:
			self.frames.append(AnimFrame(render_layer.addImage(frame[0]), frame[1], frame[2], frame[3]))

	def getCurrentFrame(self, data):
		return self.frames[data.current_frame]


# trivial, single frame animation
class AnimSingle(Anim):
	def __init__(self, rl, frames):
		super(AnimSingle, self).__init__()
		self.addFrames(rl, frames)

	def getCurrentFrame(self, data):
		return self.frames[0]

	def advanceAnim(self,anim_instance, time):
		pass


# simple looping animation
class AnimLoop(Anim):
	def __init__(self, rl, frames):
		super(AnimLoop, self).__init__()
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
		super(AnimNoLoop, self).__init__()
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
		super(AnimRandom, self).__init__()
		self.addFrames(rl, frames)

	def advanceAnim(self, anim_instance, time):
		anim_instance.current_time += time
		while anim_instance.current_time > self.frames[anim_instance.current_frame].time:
			anim_instance.current_time -= self.frames[anim_instance.current_frame].time
			anim_instance.current_frame = rand_num(len(self.frames))

# container for a single frame of animation
class AnimFrame:
	def __init__(self, image, origin_x, origin_y, time):
		self.image = image
		self.origin_x = origin_x
		self.origin_y = origin_y
		self.time = time

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
