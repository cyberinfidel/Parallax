import os
from sys import exit
from ctypes import c_long, pointer
import ctypes

sdlpath = os.path.join(os.path.dirname(__file__), 'libs')
os.environ['PYSDL2_DLL_PATH'] = sdlpath

import sdl2
import sdl2.ext
import sdl2.sdlttf

def renderTexture(tex, ren, x, y):
	"""
	:type ren: SDL_Renderer
	:type tex: SDL_Texture
	"""

	#Setup the destination rectangle to be at the position we want
	dst = sdl2.SDL_Rect(x, y)
	w = ctypes.c_int()
	h = ctypes.c_int()
	#Query the texture to get its width and height to use
	sdl2.SDL_QueryTexture(tex, None, None, w, h)
	dst.w = w.value
	dst.h = h.value
	sdl2.SDL_RenderCopy(ren.sdlrenderer, tex, None, dst)

def initFont(fontFile, renderer, defaultFontSize=10):
	# Open the font
	sdl2.SDL_ClearError()
	font = sdl2.ext.FontManager(fontFile, defaultFontSize)
	p = sdl2.SDL_GetError()
	if font is None or len(p)!=0:
		print("TTF_OpenFont error: " + str(p))
		return None
	return font

def renderText(message, font, renderer, color, size=10 ):

	#We need to first render to a surface as that's what TTF_RenderText
	#returns, then load that surface into a texture
	surf = font.render(text = message, color=color, size=size)

	if surf is None:
		sdl2.sdlttf.TTF_CloseFont(font)
		print("TTF_RenderText")
		return None

	texture = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, surf)
	if texture is None:
		print("CreateTexture")

	#Clean up the surface and font
	sdl2.SDL_FreeSurface(surf)
	# sdl2.sdlttf.TTF_CloseFont(font)
	return texture

sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
#Create an application window with the following settings:
window = sdl2.ext.Window(title="SDL2 TTF Test", size=(640, 480), position=(sdl2.SDL_WINDOWPOS_CENTERED,sdl2.SDL_WINDOWPOS_CENTERED), flags=sdl2.SDL_WINDOW_RESIZABLE)

renderer = sdl2.ext.Renderer(window, flags = sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC)

# TTF
tfi = sdl2.sdlttf.TTF_Init()
if tfi != 0:
	print("TTF_Init")
	exit(1)

#We'll render the string "TTF fonts are cool!" in white
#Color is in RGB format
color = sdl2.SDL_Color(255, 255, 255)
fontpath = os.path.join(os.path.dirname(__file__), 'space-mono', 'SpaceMono-Bold.ttf')
font = initFont(fontpath, renderer)
image = renderText("TTF fonts are cool!", font, renderer,
									 color, 64 )

if image is None:
	exit(1)

screen_width = ctypes.c_int(0)
screen_height = ctypes.c_int(0)
sdl2.SDL_GetRendererOutputSize(renderer.sdlrenderer, ctypes.byref(screen_width), ctypes.byref(screen_height))
#
# #Get the texture w/h so we can center it in the screen
iW = ctypes.c_int(0)
iH = ctypes.c_int(0)
sdl2.SDL_QueryTexture(image, None, None, iW, iH)
x = screen_width.value / 2 - iW.value / 2
y = screen_height.value / 2 - iH.value / 2

r = True
event = sdl2.SDL_Event()
while r:
	if sdl2.SDL_PollEvent(event):
		if event.type == sdl2.SDL_QUIT:
			r = False
		elif event.type == sdl2.SDL_WINDOWEVENT:
			if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
				sdl2.SDL_GetRendererOutputSize(renderer.sdlrenderer, ctypes.byref(screen_width), ctypes.byref(screen_height))
				x = screen_width.value / 2 - iW.value / 2
				y = screen_height.value / 2 - iH.value / 2
		if r:
			sdl2.SDL_RenderClear(renderer.sdlrenderer)
			#We can draw our message as we do any other texture, since it's been
			#rendered to a texture
			renderTexture(image, renderer, int(x), int(y))
			sdl2.SDL_RenderPresent(renderer.sdlrenderer)

sdl2.SDL_DestroyTexture(image)
# sdl2.SDL_DestroyRenderer(renderer)
# sdl2.SDL_DestroyWindow(window)
sdl2.SDL_Quit()