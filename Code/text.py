import os

import sdl2
import sdl2.ext
import sdl2.sdlttf

from log import log

# example
# self.font = text.Font(self.ren, "Fonts/space-mono/SpaceMono-Bold.ttf")
# self.message = text.Message.withRender(self.font, "Hello Anna, would you like a snuggle?")
# self.image = self.overlay_renlayer.addImageFromMessage(self.message)


class Message(object):
	def __init__(self, font_manager, string, font=0, color=sdl2.SDL_Color(255, 255, 255, 255), size=12):
		self.string = string
		self.font_manager = font_manager
		self.font = font
		self.color = color
		self.size = size

	@classmethod
	def withRender(cls, font_manager, string, font=0, color=sdl2.SDL_Color(255, 255, 255, 255), size=12):
		message = Message(font_manager, string, font, color, size)
		message.renderToTexture()
		return message

	def renderToTexture(self):
		self.texture, self.width, self.height = self.font_manager.renderText(self.string, font=self.font, color=self.color)

class SDLFont(object):
	def __init__(self, path, size):
		self.path = path
		self.size = size

	def __eq__(self, other):
		return self.path==other.path and self.size==other.size

	def open(self):
		# Open the font
		sdl2.SDL_ClearError()
		self.font = (sdl2.sdlttf.TTF_OpenFont(self.path.encode('utf-8'), self.size))
		p = sdl2.SDL_GetError()
		if len(p) != 0:
			print(f"TTF_OpenFont error: {str(p)}\nFont file: {self.path} size: {self.size}")
			return -1

	def close(self):
		sdl2.sdlttf.TTF_CloseFont(self.font)


# wrapper for SDL TTF fonts
class FontManager(object):
	def __init__(self, renderer):
		self.ren = renderer
		self.current_font = 0
		self.sdl_fonts = []
		tfi = sdl2.sdlttf.TTF_Init()
		if tfi != 0:
			print("TTF_Init failed in FontManager")


# each size of font has to be opened separately
# kinda dumb I know
	def addFontFromFile(self, font_file, font_size=12):
		new_font = SDLFont(os.path.abspath(font_file),font_size)

		# check if this really is a new font or and return the existing one if it isn't
		for font in self.sdl_fonts:
			if font == new_font:
				return font

		new_font.open()
		self.sdl_fonts.append(new_font)
		return len(self.sdl_fonts)-1

	def replaceFontFromFile(self, font_file, index_to_replace, font_size=12):
		self.removeFont(index_to_replace)
		new_font = SDLFont(os.path.abspath(font_file),font_size)
		new_font.open()
		self.sdl_fonts[index_to_replace]= new_font

	def removeFont(self, font_index):
		self.sdl_fonts[font_index].close()
		self.sdl_fonts[font_index]=None

	def setCurrentFont(self, font_index):
		self.current_font = font_index

	def renderText(self, string, font=False, color=sdl2.SDL_Color(255,255,255,255)):
		#We need to first render to a surface as that's what TTF_RenderText
		#returns, then load that surface into a texture

		surf = sdl2.sdlttf.TTF_RenderUTF8_Blended(self.sdl_fonts[font].font, string.encode('utf-8'), color)
		if surf is None:
			log(f"TTF_RenderText failed: {string}")
			return None
		texture = sdl2.SDL_CreateTextureFromSurface(self.ren.sdlrenderer, surf)
		if texture is None:
			print("CreateTexture")
		#Clean up the surface and font
		width = surf.contents.w
		height = surf.contents.h
		sdl2.SDL_FreeSurface(surf)
		# sdl2.sdlttf.TTF_CloseFont(font)
		return texture, width, height
	##################################################

	def delete(self):
		# fontmanager should clean itself up, really
		for font in self.sdl_fonts:
			if font:
				font.close()
