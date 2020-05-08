# import python libs
import time

# import sdl files
import sdl2.ext

# import my files
import graphics
import entity
import collision
import vector

# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')

class Game(object):

	def __init__(self):
		# Initialize the video system - this implicitly initializes some
		# necessary parts within the SDL2 DLL used by the video module.
		#
		# You SHOULD call this before using any video related methods or
		# classes.
		sdl2.ext.init()

		# Create a new window (like your browser window or editor window,
		# etc.) and give it a meaningful title and size. We definitely need
		# this, if we want to present something to the user.
		self.window = sdl2.ext.Window("Feed the Duck", size=(1280, 800))  # ,flags=sdl2.SDL_WINDOW_FULLSCREEN)

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
		sdl2.SDL_RenderSetLogicalSize(self.ren.renderer, 320, 200)

		self.running = True

		self.renlayer = graphics.RenderLayer(self.ren)

		self.input = entity.Input()

		self.drawables = []
		self.updatables = []

		self.graphics_manager = entity.ComponentManager()
		self.controller_manager = entity.ComponentManager()
		self.entity_manager = entity.EntityManager()




	def render(self):
		self.ren.color = sdl2.ext.Color(100, 200, 250)
		self.ren.clear()

		self.draw()


		# present graphics and actually display
		sdl2.SDL_RenderPresent(self.ren.renderer)
		self.window.refresh()


	def tick(self, dt):
		self.input.update(sdl2.ext.get_events())
		self.update(dt)
		if self.input.quit:
			self.running = False

	def interpolate(self, alpha):
		pass
		if alpha>0.0001:
			self.interp(alpha)
#			self.pos_int[0] = self.pos[0]* alpha + self.pos_old[0] * (1.0 - alpha)
#			self.pos_int[1] = self.pos[1]* alpha + self.pos_old[1] * (1.0 - alpha)


	def run(self):
		# uses a fixed time step for physics - see article about "Fixing Your Time Step"

		self.lastTime = time.time()

		t = 0.0
		dt = 0.016
		self.render()
		currentTime = time.time()
		accum = 0.0

		while self.running:
			newTime = time.time()
			frameTime = newTime - currentTime
			currentTime = newTime

			accum += frameTime

			while accum>=dt:
				self.tick(dt)
				accum -= dt
				t += dt

			self.interpolate(accum/dt)

			self.render()

		# Clear up and exit
		sdl2.ext.quit()

	def runTests(self):
		result = 0
		if(vector.runTests()!=0):
			log("vector tests failed.")
			result+=1
		#elif()
		return result