import sys


# import Parallax files
# 	add path to Parallax
sys.path.append('../')

import sdl2

import text
import game
import graphics




class Font2Sprite(game.Game):

	def __init__(self):
		super(Font2Sprite, self).__init__("Font2Sprite", res_x= 320, res_y= 320, zoom = 3, fullscreen= False)
		self.renlayer = graphics.RenderLayer(self.ren)
		self.font_manager = text.FontManager(self.ren)
		self.font = self.font_manager.addFontFromFile("Fonts/Adventurer/Adventurer.ttf", 15)

		self.i = 33

	def update(self, dt):
		pass

	def draw(self):
		if self.i <127:
			self.i+=1
			sdl2.SDL_SetRenderDrawColor(self.ren.sdlrenderer, 255,255,255,255)
			width, height = self.font_manager.renderTextToSurfaceAndSave(f"Output/char_{self.i}.png", chr(self.i), self.font)

		else:
			exit(0)


	def interp(self, alpha):
		pass

def run(tests=False):
	game = Font2Sprite()
	game.run()
	return 0


	return True

if __name__ == "__main__":
	sys.exit(run(tests=True))