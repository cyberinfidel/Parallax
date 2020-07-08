try:
	import sys
	import sdl2
	import sdl2.ext
	import sdl2.sdlmixer as sdlmixer
#RESOURCES = sdl2.ext.Resources(__file__, "resources")

except ImportError:
	import traceback
	traceback.print_exc()
	sys.exit(1)


if __name__ == "__main__":
	RESOURCES = sdl2.ext.Resources(__file__, "")

def main():
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

	ren.color = sdl2.ext.Color(0, 0, 0)
	ren.clear()

	sdl2.SDL_RenderPresent(ren.renderer)

	window.refresh()

	sdl2.SDL_Delay(2)




