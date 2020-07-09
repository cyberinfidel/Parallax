import enum
import os

import sdl2
import sdl2.ext
import sdl2.sdlmixer as sdlmixer

from Parallax import entity

# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')


class SoundMixer(object):
	def __init__(self, game):
		super(SoundMixer, self).__init__()
		self.mute = False
		self.sounds = []

		if sdl2.SDL_Init(sdl2.SDL_INIT_AUDIO) != 0:
			raise RuntimeError("Cannot initialize audio system: {}".format(sdl2.SDL_GetError()))

		if sdlmixer.Mix_OpenAudio(44100, sdlmixer.MIX_DEFAULT_FORMAT, 2, 1024):
			raise RuntimeError("Cannot open mixed audio: {}".format(sdlmixer.Mix_GetError()))

		if sdlmixer.Mix_AllocateChannels(64) !=64:
			raise RuntimeError("Cannot allocate audio channels: {}".format(sdlmixer.Mix_GetError()))



	def loadSound(self, file):
		# find if this file has been loaded before and return that if so
		filepath = os.path.abspath(file)
		for index, sound in enumerate(self.sounds):
			if sound.path == filepath:
				return index
		# haven't seen this file before so add it and return new index
		try:
			sample = sdlmixer.Mix_LoadWAV(sdl2.ext.compat.byteify(filepath, "utf-8"))
			if sample is None:
				raise RuntimeError("Cannot open audio file: {}".format(sdlmixer.Mix_GetError()))
			self.sounds.append(Sample(filepath, sample))
		except Exception as e:
			log(f"Problem loading sound: {str(e)} file: {filepath}")

		return len(self.sounds) - 1

	def mute(self, mute):
		self.mute = mute

	def play(self, sample, loops):
		if not self.mute:
			return self.sounds[sample].play(loops)


class SoundTypes(enum.IntEnum):
	single_sound = 0,
	multi_sound = 1
	num_sound_types = 2

class MultiSound(entity.Component):
	class Data(object):
		def __init__(self, common_data, init=False):
			pass

	def __init__(self, game, data):
		super(MultiSound, self).__init__(game)
		self.state_sounds = {}
		self.event_sounds = {}

		# parse data
		self.mixer = data['Mixer']
		self.name = data['Name']
		for sound in data["StateSounds"]:
			for state in sound["States"]:
				self.state_sounds[state] = sound['Type'](self.mixer, sound["Samples"])
		for sound in data["EventSounds"]:
			for event in sound["Events"]:
				self.event_sounds[event] = sound['Type'](self.mixer, sound["Samples"])

	# plays state sounds as part of per tick update routines
	def play(self, data, common_data):
		if common_data.state in self.state_sounds:
			# log(f"{self.name} sound {common_data.state}")
			self.state_sounds[common_data.state].play(data, common_data)

	def playEvent(self, data, common_data, event):
		self.event_sounds[event].play(data, common_data)

class RandomSample(object):
	def __init__(self, path, sample):
		super(RandomSample, self).__init__()
		self.path = path

	def playSample(self, index):
			pass

class SingleNoLoopNoOverlapState(object):
	def __init__(self, mixer, samples):
		self.mixer = mixer
		self.sample = mixer.loadSound(samples[0])
		self.channel=-1

	def play(self, data, common_data):
		if common_data.new_state and not sdlmixer.Mix_Playing(self.channel):
			self.channel = self.mixer.play(self.sample, loops=0)

class Single(object):
	def __init__(self, mixer, samples):
		self.mixer = mixer
		self.sample = mixer.loadSound(samples[0])

	def play(self, data, common_data):
		self.mixer.play(self.sample, loops=0)


class Sample(object):
	def __init__(self, path, sample):
		super(Sample, self).__init__()
		self.path = path
		self.sample = sample

	def play(self, loops):
		channel = sdlmixer.Mix_PlayChannel(channel=-1, chunk=self.sample, loops=loops)
		if channel == -1:
			raise RuntimeError("Cannot play sample: {}".format(sdlmixer.Mix_GetError()))
		return channel

	def stopSample(self, channel):
		pass