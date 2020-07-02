from entity import ComponentManager



class SoundManager(ComponentManager):
	def __init__(self, game):
		super(SoundManager, self).__init__(game)
		mute = False

	def loadSound(self, path):
		pass

	def mute(self, mute):
		self.mute = mute


class Sound(Component):
	def __init__(self, game):
		super(Sound, self).__init__(game)
		sounds = []

	def playSound(self, index):
		if not self.mute:
			pass

	def stopSound