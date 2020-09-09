# external lib import
import os
import ctypes

# import sdl libs
import sdl2.ext
import sdl2.sdlimage as sdl_image

# initialise for loading PNGs and JPGs
sdl_image.IMG_Init(sdl_image.IMG_INIT_PNG)
sdl_image.IMG_Init(sdl_image.IMG_INIT_JPG)

# import my files
import px_entity
import px_vector
from px_vector import Vec3, rand_num
from px_log import log

# globals
graphics_debug = False


class eAlign:
	left, centre, right = range(0,3)


# color class where components are between 0 and 1
# as intended by nature
class Color(object):
	def __init__(self, r,g,b,a=1):
		self.r = r
		self.g = g
		self.b = b
		self.a = a

	# accept 0-255 values as well
	@classmethod
	def fromInts(cls, r, g, b, a=255):
		return cls(r/255,g/255,b/255,a/255)

	def toSDLColor(self):
		return sdl2.SDL_Color(int(self.r*255),
													int(self.g * 255),
													int(self.b * 255),
													int(self.a * 255))

	def __mul__(self, other):
		return Color(
			self.r*other.r,
			self.g * other.g,
			self.b * other.b,
			self.a * other.a
		)

	def __add__(self, other):
		return Color(
			self.r+other.r,
			self.g + other.g,
			self.b + other.b,
			self.a + other.a,
		)

	def __str__(self):
		return f"(r{self.r}, g{self.g}, b{self.b}, a{self.a})"

import px_text

# Individual images for use as frames for animations or as part of the background etc.
# Based on SDL images for the moment with no atlassing etc.
class Image(object):
	def __init__(self, ren, texture, width, height, trim_x=0, trim_y=0, file=None, src=None):
		self.renderer = ren
		self.file = file
		self.width = width
		self.height = height
		self.trim_x = trim_x
		self.trim_y = trim_y
		if src:
			self.src = src
		else:
			self.src = sdl2.SDL_Rect(0, 0, self.width, self.height)
		self.texture = texture
		self.ref_count = 1

	# factories ###########################################################

	@classmethod
	def fromFile(cls, ren, file, width=None, height=None, trim=False):

		# get image into surface (don't need to keep this though)
		surface = sdl_image.IMG_Load(file.encode("utf-8"))

		texture=None
		trim_x=0
		trim_y=0

		if trim:
			# grab the pixel values
			# scrub through them
			# set the left to be the least value of x that isn't empty by
			# setting the initial value to the far right
			# and updating it every time we hit a non-zero pixel that has
			# has a further left i.e. lower x value
			# set the top to be the least value of y that isn't empty
			# set the right to be the highest value of y that isn't empty
			# by setting the initial value to be the left (0)
			# set the bottom to be the highest value of y that isn't empty
			h = surface.contents.h
			w = surface.contents.w
			top=h-1
			bottom=0
			right = 0
			left = w-1
			pixels = sdl2.ext.PixelView(surface.contents)
			# top
			for y in range(0,h):
				for x in range(0,w):
					if pixels[y][x]!=0:
						if top>y: top=y
						if bottom<y: bottom=y
						if left>x: left=x
						if right<x: right = x

			# print(f"file: {file}")
			# print(f"top {top}, bottom {bottom}")
			# print(f"left {left}, right {right}")

			new_w = right-left+1
			new_h = bottom-top+1
			if not( new_w>=w and new_h>=h):
				width = min(new_w,w)
				height = min(new_h,h)
				trim_x = max(0,left)
				trim_y = max(0,top)
				# there's space around the sprite so trim it
				trim_surface = sdl2.SDL_CreateRGBSurfaceFrom(surface.contents.pixels+left*4+top*w*4,
																			new_w,
																			new_h,
																			32,
																			w*4,
																			0xff0000,0xff00,0xff,0xff000000
																			)
				if not trim_surface:
					print("SDL_CreateRGBSurfaceFrom failed")
					exit(1)
				texture = sdl2.SDL_CreateTextureFromSurface(ren.sdlrenderer, trim_surface)

		# make a texture from the sdl surface (for HW rendering)
		if not texture:
			texture = sdl2.SDL_CreateTextureFromSurface(ren.sdlrenderer, surface)

		if not (width and height):
			width = surface.contents.w
			height = surface.contents.h

		if not trim: sdl2.SDL_FreeSurface(surface)
		return cls(ren=ren.sdlrenderer, texture=texture, width=width, height=height, file=file, trim_x=trim_x, trim_y=trim_y)

	@classmethod
	def fromTexture(cls, ren, texture, width, height):
		cls.file = None
		return cls(ren.renderer, texture, width, height)

	# get/sets ###########################################################
	# only really for sorting
	def getHeight(self):
		return self.height

	# draw ###########################################################

	def draw(self, x, y, color=Color(1, 1, 1, 1), debug=graphics_debug):

		sdl_color = color.toSDLColor()
		sdl2.SDL_SetTextureColorMod(self.texture, sdl_color.r, sdl_color.g, sdl_color.b)
		sdl2.SDL_SetTextureAlphaMod(self.texture, sdl_color.a)

		sdl2.SDL_RenderCopy(self.renderer, self.texture, self.src,
												sdl2.SDL_Rect(int(x), int(y), self.width, self.height))

		if debug:
			# draw the outline of the image for debugging purposes
			sdl2.SDL_SetRenderDrawColor(self.renderer,255,255,255,50)
			sdl2.SDL_SetRenderDrawBlendMode(self.renderer,sdl2.SDL_BLENDMODE_ADD)

			sdl2.SDL_RenderDrawRect(self.renderer,sdl2.SDL_Rect(int(round(x)), int(round(y)), self.width, self.height))

	# destructors ###########################################################

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
	def __init__(self, ren, origin_x=0, origin_y=0, color=False):
		self.renderer = ren
		self.color = color
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
	def __init__(self, image, x, y, z, color_cast=Color(1, 1, 1, 1)):
		super(RenderImage, self).__init__(x,y,z)
		self.image = image
		self.color_cast = color_cast

	# draws an image paying attention to the passed origin (should be the render layer origin, not the image's)
	def draw(self, origin, screen_height):
		self.image.draw(x=self.x - origin.x,
										y=screen_height - (self.y + self.z - origin.y - origin.z),
										color=self.color_cast
										)

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

		self.font_manager = px_text.FontManager(self.ren)
		self.default_font=0

		# Color cast used for fading and other effects
		self.color_cast = Color(1, 1, 1, 1)


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

	def addImageFromString(self,
												 string,
												 font=0,
												 color=Color(1, 1, 1, 1)):
		message = px_text.Message.withRender(font_manager=self.font_manager, font=font, string=string, color=color)
		index = self._getNextEmptySlot()
		self.images[index] = Image.fromTexture(self.ren,message.texture, message.width, message.height)
		return index

	def replaceImageFromMessage(self, old_image,  message):
		self.images[old_image].delete()
		self.images[old_image] = Image.fromTexture(self.ren,message.texture, message.width, message.height)

	def replaceImageFromString(self,
														 old_image,
														 string,
														 font=0,
														 color=Color(1, 1, 1, 1)):
		message = px_text.Message.withRender(font_manager=self.font_manager, string=string, font=font, color=color)
		self.images[old_image].delete()
		self.images[old_image] = Image.fromTexture(self.ren,message.texture, message.width, message.height)

	# add to the store of images available in this render layer
	def addImageFromFile(self, file, trim=False):
		# find if this file has been loaded before and return that if so
		# also check if there's an index that is empty and can be re-used
		filepath = os.path.abspath(file)
		for index, image in enumerate(self.images):
			if image:
				if image.file == filepath:
					image.ref_count+=1
					return index, image.trim_x, image.trim_y

		# otherwise find next empty slot (or append)
		index = self._getNextEmptySlot()
		try:
			self.images[index] = Image.fromFile(self.ren, filepath, width=None, height=None, trim=trim)
			return index, self.images[index].trim_x, self.images[index].trim_y
		except Exception as e:
			log("Problem loading image for frame: " + str(e) + " file:" + filepath)

	def getImageDimensions(self, index):
		return self.images[index].width,self.images[index].height

	# empty the list of drawables for this layer so nothing is set to be drawn on a render event
	def clear(self):
		self.drawables = []  # note this replaces list with empty list and doesn't delete any of the contents of list

	# add an image to the list of drawables to be drawn on a render
	def queueImage(self, image, x, y, z, color=Color(1, 1, 1, 1)):
		self.drawables.append(RenderImage(self.images[image], x, y, z, self.color_cast*color))


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

	def setColorCast(self,color):
		self.color_cast = color

	# releases an image with ref counting
	def releaseImage(self, index):
		self.images[index].release()

	# kills whole render layer and all images, dead
	def delete(self):
		for image in self.images:
			image.delete()

# add a font that this Render Layer can use
	def addFont(self, font_path, size):
		return self.font_manager.addFontFromFile(font_path, size)

	def queueMessageFromText(self, message_text, x, y, font=None, size= None):
		if not font:
			font = self.default_font
		self.addImageFromMessage(px_text.Message.withRender(font, message_text))

	# takes all textures already submitted and makes into an atlas
	# uses dumbest algorithm possible atm
	# speed up success by giving the correct start size for the atlas
	# will add 64 on each attempt until success
	def makeAtlas(self, start_size=256):
		# tries this size and increases dimensions until the images all fit
		atlas_dim=start_size
		while not self._renderAtlas(atlas_dim, dry_run=True):
			atlas_dim=int( atlas_dim + 64)
			if atlas_dim>4096:
				log("WARNING: a texture atlas dimension bigger than 4K may not work on some machines")

		# actually render atlas - do again with rendering and updating the image records
		self._renderAtlas(atlas_dim, dry_run=False)
		self.atlas_dim = atlas_dim
		log(f"Graphics|RenderLayer:Atlas created at size: {self.atlas_dim}")

	# adds all existing images to a texture atlas. Updates the image objects to point to the
	# atlas texture and their src variables to where in the texture they are
	def _renderAtlas(self, atlas_dim, dry_run, gap=0):
		if not dry_run:
			# make the atlas texture
			self.TA = sdl2.SDL_CreateTexture(self.ren.renderer,
																			 sdl2.SDL_PIXELFORMAT_RGBA8888,
																			 sdl2.SDL_TEXTUREACCESS_TARGET,
																			 atlas_dim,
																			 atlas_dim)
			# point drawing at the atlas and clear it
			sdl2.SDL_SetRenderTarget(self.ren.renderer, self.TA)
			sdl2.SDL_SetRenderDrawColor(self.ren.renderer, 0, 0, 0, 0)
			sdl2.SDL_RenderClear(self.ren.renderer)
			sdl2.SDL_SetRenderDrawColor(self.ren.renderer,255,255,255,255)

		# draws textures in rows, left to right, then top to bottom
		accum_x=0 # where we've got to across TA
		max_y = 0 # how tall the row is so we know where to start the next one
		accum_y=0	# how far down the current row is
		for image in sorted(self.images, key = Image.getHeight, reverse=True):
			if accum_x+image.width+gap>atlas_dim:	# will this image go off right of atlas?
				accum_x=0
				# push down
				accum_y+=max(max_y,image.height)+gap # in case this is the tallest image
				max_y=0

			if not dry_run:
				# draw into atlas and kill old texture
				image.draw(accum_x, accum_y)
				sdl2.SDL_DestroyTexture(image.texture)
				# and update the image to point to where it went in the atlas
				# update in place to avoid re-doing indexes
				image.texture =  self.TA
				image.src = sdl2.SDL_Rect(accum_x, accum_y, image.width, image.height)

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

######################################################
	def dumpImageToFile(self, image, image_file):
		format = sdl2.SDL_PIXELFORMAT_RGBA8888
		width = self.images[image].width
		height = self.images[image].height

		surface = sdl2.SDL_CreateRGBSurfaceWithFormat(0, width, height, 32, format)
		sdl2.SDL_LockSurface(surface)
		sdl2.SDL_SetRenderTarget(self.ren.renderer, self.images[image].texture)
		sdl2.SDL_RenderReadPixels(self.ren.renderer,
																			 sdl2.SDL_Rect(0,0,width,height),
																			 format,
																			 surface.contents.pixels,
																			 surface.contents.pitch)
		sdl2.SDL_UnlockSurface(surface)


		sdl_image.IMG_SavePNG(surface.contents, image_file.encode("utf-8"))
		sdl2.SDL_SetRenderTarget(self.ren.renderer, None)
		return True

	# todo
	def loadAtlasFromFiles(self, image_file, data_file):
		pass

####################################################
# end of RenderLayer
####################################################

# Types of graphics components available
class GraphicsTypes:
	single_image, \
	single_anim, \
	multi_anim, \
	text_message, \
	num_graphics_types = range(0,5)

# graphics component for a single static image
# template data should look like:
# {
# "Name" : "xxx picture",
# "Template" : graphics.SingleImage,
# "Image" : ["path/to/image.png", x-origin, y-origin, z-origin]
# }

class SingleImage(px_entity.Component):
	def __init__(self, game, data):
		super(SingleImage, self).__init__(game)
		self.rl = data['RenderLayer']
		self.name = data["Name"]
		self.image, trim_x, trim_y = self.rl.addImageFromFile(data["Image"][0])
		self.origin_x = data["Image"][1]-trim_x
		self.origin_y = data["Image"][2]-trim_y
		self.origin_z = data["Image"][3]

	def getImage(self):
		return self.image

	def draw(self, entity):
		return self.rl.queueImage(self.image, entity.pos.x - self.origin_x, entity.pos.y + self.origin_y, entity.pos.z + self.origin_z)

	def hasShadow(self):
		return False

	def update(self, data, entity, time):
		pass

# graphics component for multiple static images
class MultiImage(px_entity.Component):
	def __init__(self, game, data):
		super(MultiImage, self).__init__(game)
		self.rl = data['RenderLayer']
		self.images = []
		for image in data["Images"]:
			image_object, trim_x, trim_y = self.rl.addImageFromFile(image[0])
			self.images.append(AnimFrame(image_object, image[1]-trim_x, image[2]-trim_y, image[3], 0))

	def getImage(self):
		return self.image

	def draw(self, entity):
		for image in self.images:
			self.rl.queueImage(image.image, entity.pos.x - image.origin_x, entity.pos.y + image.origin_y, entity.pos.z + image.origin_z)
		return True

	def hasShadow(self):
		return False

	def update(self, entity, time):
		pass


# graphics component for a single animation only
class SingleAnim(px_entity.Component):
	class Data(object):
		def __init__(self, entity):
			self.current_frame = 0
			self.current_time = 0

	def __init__(self, game, data):
		super(SingleAnim, self).__init__(game)
		self.rl = data['RenderLayer']
		self.anim = data['Anims'][0]['AnimType'](self.rl, data["Anims"][0]["Frames"])
		self.name = data["Name"]

	def getAnim(self):
		return self.anim

	def update(self, entity, time):
		self.anim.advanceAnim(entity, time)

	def draw(self, entity):
		frame = self.anim[0]
		return self.rl.queueImage(frame.image, entity.pos.x - frame.origin_x, entity.pos.y + frame.origin_y, entity.pos.z + frame.origin_z)

	def hasShadow(self):
		return False


# graphics component for multiple animations
class MultiAnim(px_entity.Component):
	def __init__(self, game, data):
		super(MultiAnim, self).__init__(game)
		self.rl = data['RenderLayer']
		self.anims = {}

		# parse data for single pass initialisation
		self.name = data["Name"]
		for anim in data["Anims"]:
			for state in anim["States"]:
				self.anims[state] = anim['AnimType'](self.rl, anim["Frames"])

	def initEntity(self, entity, data=False):
		entity.current_frame = 0
		entity.current_time = 0
		entity.current_anim =  px_entity.eStates.stationary
		entity.current_state = px_entity.eStates.stationary

		for anim in self.anims:	# ie every anim in the multiAnim
			self.anims[anim].initInstance(entity=entity)

	def delete(self):
		for anim in self.anims:
			self.anims[anim].delete()


	def update(self, entity, time):
		if entity.new_state:
			entity.new_state=False
			if entity.state in self.anims:
				entity.current_anim = entity.state
				entity.current_state = entity.state
				self.anims[entity.current_anim].startAnim(entity) # TODO allow some anims to begin from different frame
			else:
				log(f"Warning: {entity.name} animation doesn't exist for requested state {entity.state}")
		self.anims[entity.current_anim].advanceAnim(entity, time)

	def draw(self, entity):
		frame = self.anims[entity.current_anim].getCurrentFrame(entity)
		return self.rl.queueImage(frame.image, entity.pos.x - frame.origin_x, entity.pos.y + frame.origin_y, entity.pos.z + frame.origin_z)

	def hasShadow(self):
		return px_entity.eStates.shadow in self.anims

	def drawShadow(self, entity, shadow_height=0):

		# todo: work out why y=0 doesn't work
		# todo: shrink shadow the higher y is
		# todo: allow shadows that aren't all at y=0
		frame = self.anims[px_entity.eStates.shadow].getCurrentFrame(entity)
		return self.rl.queueImage(frame.image, entity.pos.x - frame.origin_x + shadow_height, frame.origin_y, entity.pos.z)


#####################################################################
# Animation code																										#
#####################################################################

class Anim(object):
	def __init__(self, render_layer):
		self.frames = []
		self.render_layer = render_layer

	# override for specific instances and some anim types
	def initInstance(self, entity):
		pass

	def addFrame(self, image, duration):
		self.frames.append(AnimFrame(image, duration))

	def addFrames(self, render_layer, frames):
		for frame in frames:
			# frame:
			# 0: file path
			# 1: x origin
			# 2: y origin
			# 3: z origin
			# 4: frame time
			image, trim_x, trim_y = render_layer.addImageFromFile(frame[0], trim=True)
			self.frames.append(AnimFrame(image, frame[1]-trim_x, frame[2]-trim_y, frame[3], frame[4]))

	def getCurrentFrame(self, entity):
		return self.frames[entity.current_frame]

	def startAnim(self, entity, frame=0):
		entity.current_time = 0
		entity.current_frame = frame

	def delete(self):
		for frame in self.frames:
			self.render_layer.releaseImage(frame.image)

# trivial, single frame animation
class AnimSingle(Anim):
	def __init__(self, rl, frames):
		super(AnimSingle, self).__init__(rl)
		self.addFrames(rl, frames)

	def getCurrentFrame(self, entity):
		return self.frames[0]

	def advanceAnim(self, anim_instance, time):
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

# simple choose a frame at random and stay static
# note: frame is chosen every time the animation is started
# in a MultiAnim this means a random frame each time the state
# for this Anim is chosen - the frame will not persist
class AnimRandomStatic(Anim):
	def __init__(self, rl, frames):
		super(AnimRandomStatic, self).__init__(rl)
		self.addFrames(rl, frames)

	def startAnim(self, entity, frame=0):
		entity.current_time = 0
		entity.current_frame = rand_num(len(self.frames))

	def advanceAnim(self, anim_instance, time):
		pass	# don't animate and stay on the initially selected random frame

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
	# Switch on VSync to avoid running too fast, nasty artefacts
	# and wasting power and keep graphics nice and clean
	ren = sdl2.ext.Renderer(window, flags=sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC)
	# makes zoomed graphics blocky (for retro effect)
	sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"nearest")
	# makes the graphics look and act like the requested screen size, even though
	# they may be rendered much larger
	sdl2.SDL_RenderSetLogicalSize(ren.sdlrenderer, res_x, res_y)

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

	rl.addImageFromFile("GraphicsTest/test.png")


	return fails

if __name__ == "__main__":
	import sys
	sys.exit(runTests())
