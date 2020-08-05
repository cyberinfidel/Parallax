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
	def __init__(self, font, text, color=sdl2.SDL_Color(255, 255, 255, 255), size=12):
		self.text = text
		self.font = font
		self.color = color
		self.size = size

	@classmethod
	def withRender(cls, font, text, color=sdl2.SDL_Color(255, 255, 255, 255), size=12):
		message = Message(font, text, color, size)
		message.renderToTexture()
		return message

	def renderToTexture(self):
		self.texture, self.width, self.height = self.font.renderText(self.text, color=self.color, size=self.size)

# wrapper for SDL font manager
class FontManager(object):
	def __init__(self, renderer):
		self.ren = renderer
		self.current_font = 0
		self.sdl_fontmanager = None
		self.font_count = 0

	def addFontFromFile(self, font_file, defaultFontSize=12):
		self.font_file = os.path.abspath(font_file)
		# Open the font
		sdl2.SDL_ClearError()
		if not self.sdl_fontmanager:
			self.sdl_fontmanager = sdl2.ext.FontManager(font_file, defaultFontSize)
		else:
			self.sdl_fontmanager.add(font_file, defaultFontSize)
		p = sdl2.SDL_GetError()
		if len(p) != 0:
			print(f"TTF_OpenFont error: {str(p)}\nFont file: {font_file}")
			return -1
		self.font_count+=1
		return self.font_count-1

	def replaceFont(self, font_file, index_to_replace=None, defaultFontSize=12):
		pass # todo

	def setCurrentFont(self, font_index):
		self.current_font = font_index

	def renderText(self, message, color=sdl2.SDL_Color(255,255,255,255), size=12, bgcolor=sdl2.SDL_Color(0,0,0,255) ):
		#We need to first render to a surface as that's what TTF_RenderText
		#returns, then load that surface into a texture
		surf = self.sdl_fontmanager.render(alias=self.current_font, text=message, color=color, size=size, bgcolor=bgcolor)
		if surf is None:
			sdl2.sdlttf.TTF_CloseFont(self.sdl_fontmanager[self.current_font])
			log(f"TTF_RenderText failed: {message}")
			return None
		texture = sdl2.SDL_CreateTextureFromSurface(self.ren.sdlrenderer, surf)
		if texture is None:
			print("CreateTexture")
		#Clean up the surface and font
		width = surf.w
		height = surf.h
		sdl2.SDL_FreeSurface(surf)
		# sdl2.sdlttf.TTF_CloseFont(font)
		return texture, width, height
	##################################################

	def delete(self):
		# fontmanager should clean itself up, really
		pass
