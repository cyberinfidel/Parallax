try:
	import sys
	import sdl2
	import sdl2.ext
	import sdl2.sdlmixer as sdlmixer
	#RESOURCES = sdl2.ext.Resources(__file__, "resources")

	import GameControllerDB

except ImportError:
	import traceback
	traceback.print_exc()
	sys.exit(1)


if __name__ == "__main__":
	RESOURCES = sdl2.ext.Resources(__file__, "")

class Cont(object):
	def __init__(self, handler, joy_number):
		self.handler = handler
		self.joy_number = joy_number
		self.name = sdl2.SDL_GameControllerName(self.handler)


class Game(object):
	def __init__(self):
		self.controllers={}

		# Initialize the video system - this implicitly initializes some
		# necessary parts within the SDL2 DLL used by the video module.
		#
		# You SHOULD call this before using any video related methods or
		# classes.
		sdl2.ext.init()

		sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_JOYSTICK | sdl2.SDL_INIT_GAMECONTROLLER)
		# GameControllerDB.init_game_controller()

		self.title = "Controller Test"
		self.res_x = 640
		self.res_y = 480
		self.zoom = 1

		self.window = sdl2.ext.Window(self.title, size=(self.res_x*self.zoom, self.res_y*self.zoom))

		# By default, every Window is hidden, not shown on the screen right
		# after creation. Thus we need to tell it to be shown now.
		self.window.show()

		# set up a renderer to draw stuff. This is a HW accelerated one.
		# Switch on VSync to avoid running too fast
		# and wasting power and keep graphics nice and clean
		self.ren = sdl2.ext.Renderer(self.window, flags=sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC)
		# makes zoomed graphics blocky (for retro effect)
		sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"nearest")
		# makes the graphics look and act like Atari ST screen size, even though rendered much larger
		sdl2.SDL_RenderSetLogicalSize(self.ren.renderer, self.res_x, self.res_y)








		if sdl2.SDL_NumJoysticks()>0:
			for joy in range(sdl2.SDL_NumJoysticks()):
				if sdl2.SDL_IsGameController(joy):
					self.controllers[joy]=(Cont(handler=sdl2.SDL_GameControllerOpen(joy), joy_number=joy))


		print("Initialised.")


	def update(self):
		events = sdl2.ext.get_events()
		for event in events:
			if event.type == sdl2.SDL_CONTROLLERBUTTONDOWN:
				if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_A:
					print(f"Button press on controller {event.cbutton.which}: A")
				if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_B:
					print(f"Button press on controller {event.cbutton.which}: B")
				if event.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_DPAD_UP:
					print(f"Button press on controller {event.cbutton.which}: UP")

			if event.type == sdl2.SDL_QUIT:
				# Clear up and exit
				sdl2.ext.quit()
				return False

		# for index, controller in enumerate(self.controllers.values()):
		# 	if sdl2.SDL_GameControllerGetButton(controller.handler, sdl2.SDL_CONTROLLER_BUTTON_A):
		# 		print(f"A {index}")
		# 	if sdl2.SDL_GameControllerGetButton(controller.handler, sdl2.SDL_CONTROLLER_BUTTON_B):
		# 		print(f"B {index}")

		# print("End of update")

		return True

if __name__ == "__main__":
	game = Game()
	import sys
	while game.update():
		pass
	print("Finished.")
	sys.exit(0)
