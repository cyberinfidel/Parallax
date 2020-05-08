# external lib import
import enum
import os
import ctypes

# import sdl libs
import sdl2.ext
import sdl2.sdlimage as sdl_image
import sdl2.sdlgfx as sdl_gfx


# initialise for loading PNGs and JPGs
sdl_image.IMG_Init(sdl_image.IMG_INIT_PNG)
sdl_image.IMG_Init(sdl_image.IMG_INIT_JPG)

# import my files
from entity import *
from vector import *


# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')

# globals

glob_debug = False


class Image(object):
	def __init__(self, ren, file, origin_x=0, origin_y=0, width=False, height=False):
		self.renderer = ren
		# cache screen height for calculation later
		screen_width = ctypes.c_int(0)
		screen_height = ctypes.c_int(0)
		sdl2.SDL_RenderGetLogicalSize(ren.renderer,ctypes.byref(screen_width),ctypes.byref(screen_height))
		self.screen_height = int(screen_height.value)

		self.file = file

		# get image (don't need to keep this though)
		surface = sdl_image.IMG_Load(file.encode("ascii"))

		# make a texture from the apple surface (for HW rendering)
		self.texture = sdl2.SDL_CreateTextureFromSurface(self.renderer.renderer, surface)

		if not (width and height):
			self.width = surface.contents.w
			self.height = surface.contents.h
		else:
			self.width = width
			self.height = height

#		self.src = sdl2.SDL_Rect(0, 0, self.width, self.height)
		self.src = sdl2.SDL_Rect(0, 0, self.width, self.height)

		self.origin_x = origin_x
		self.origin_y = origin_y

	def draw(self, x, y, debug=glob_debug):
		sdl2.SDL_RenderCopy(self.renderer.renderer, self.texture, self.src,
												sdl2.SDL_Rect(int(round(x))-self.origin_x, self.screen_height-int(round(y))-self.origin_y, self.width, self.height))

		if debug:
			sdl2.SDL_SetRenderDrawColor(self.renderer.renderer,255,255,255,50)
			sdl2.SDL_SetRenderDrawBlendMode(self.renderer.renderer,sdl2.SDL_BLENDMODE_ADD)

			sdl2.SDL_RenderDrawRect(self.renderer.renderer,sdl2.SDL_Rect(int(round(x))-self.origin_x, self.screen_height-int(round(y))-self.origin_y, self.width, self.height))

			# collision debugging - TODO: get collision radii into here
			sdl_gfx.filledCircleRGBA(self.renderer.renderer, int(round(x)), self.screen_height-int(round(y)), 10, 255,255,1,100 )


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

	def draw(self, origin):
		self.image.draw(self.x - origin.x, self.y - origin.y + origin.z + self.z)

class RenderShape(Drawable):
	def __init__(self, shape, x, y, z):
		super(RenderShape, self).__init__(x,y,z)
		self.shape = shape

	def draw(self, origin):
		self.shape.draw(self.x - origin.x, self.y - origin.y + origin.z + self.z)

class RenderLayer(object):
	def __init__(self, ren):
		self.ren = ren

		self.images = []
		self.drawables = []

		self.origin = Vec3(0,0,0)

	def addImage(self, file, origin_x=0, origin_y=0):
		# find if this file has been loaded before and return that if so
		filepath = os.path.abspath(file)
		for index, image in enumerate(self.images):
			if image.file == filepath:
				return index

		# haven't seen this file before so add it and return new index
		try:
			self.images.append(Image(self.ren, filepath, origin_x, origin_y))
		except Exception as e:
			log("Problem loading image for frame: "+str(e))
		return len(self.images) - 1

	def clear(self):
		self.drawables = []  # note this replaces list with empty list and doesn't delete any of the contents of list


	def queueImage(self, image, x, y, z):
		self.drawables.append(RenderImage(self.images[image], x, y, z))

	# draws the drawables queue and clears it
	def render(self):
		for d in self.drawables:
			d.draw(self.origin)
		self.drawables = []

	def renderSorted(self):
		for d in sorted(self.drawables, key = Drawable.getY, reverse=True):
			d.draw(self.origin)
		self.drawables = []

	def setOriginX(self, x):
		self.origin_x = x

	def setOriginZ(self, z):
		self.origin_z = z

	def getOriginX(self):
		return self.origin_x

	def getOriginZ(self):
		return self.origin_z


class GraphicsTypes(enum.IntEnum):
	single_image = 0,
	single_anim = 1,
	multi_anim = 2,
	num_graphics_types = 3






class SingleImage(Component):

	def __init__(self, data):
		super(SingleImage, self).__init__()
		self.rl = data['RenderLayer']
		self.image = self.rl.addImage(data["Image"][0], data["Image"][1],data["Image"][2])

	def getImage(self):
		return self.image

	def draw(self, data, common_data):
		return self.rl.queueImage(self.image, common_data.pos.x, common_data.pos.y, common_data.pos.z)



class SingleAnim(Component):
	class Data(object):
		def __init__(self, common_data):
			self.current_frame = 0
			self.current_time = 0

	def __init__(self, data):
		super(SingleAnim, self).__init__()
		self.rl = data['RenderLayer']
		self.anim = data['Anims'][0]['AnimType'](self.rl, data["Anims"][0]["Frames"])
		self.name = data["Name"]

	def getAnim(self):
		return self.anim

	def update(self, data, common_data, time):
		self.anim.advanceAnim(data, time)

	def draw(self, data, common_data):
		return self.rl.queueImage(self.anim.getCurrentImage(data), common_data.pos.x, common_data.pos.y, common_data.pos.z)



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

	def __init__(self, data):
		super(MultiAnim, self).__init__()
		self.rl = data['RenderLayer']
		self.anims = {}

		# parse data for single pass initialisation
		self.name = data["Name"]
		for anim in data["Anims"]:
			self.anims[anim["State"]] = anim['AnimType'](self.rl, anim["Frames"])

	def update(self, data, common_data, time):
		if common_data.new_state:
			common_data.new_state=False
			data.current_anim = common_data.state
			data.current_state = common_data.state
			data.current_time = 0
			data.current_frame = 0	# TODO allow some anims to begin from different frame
		self.anims[data.current_anim].advanceAnim(data, time)

	def draw(self, data, common_data):
		try:
			return self.rl.queueImage(self.anims[data.current_anim].getCurrentImage(data), common_data.pos.x, common_data.pos.y, common_data.pos.z)
		except Exception as e:
			log(e)
			exit(1)



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
			self.frames.append(AnimFrame(render_layer.addImage(frame[0], frame[1], frame[2]), frame[3]))

	def getCurrentImage(self, data):
		return self.frames[data.current_frame].image


# trivial, single frame animation
class AnimSingle(Anim):
	def __init__(self):
		super(AnimSingle, self).__init__()

	def advanceAnim(self, time):
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
	def __init__(self):
		super(AnimRandom, self).__init__()

	def advanceAnim(self, anim_instance, time):
		anim_instance.current_time += time
		while anim_instance.current_time > self.frames[anim_instance.current_frame].time:
			anim_instance.current_time -= self.frames[anim_instance.current_frame].time
			anim_instance.current_frame = rand_num(len(self.frames))


class AnimFrame:
	def __init__(self, image, time):
		self.image = image
		self.time = time
