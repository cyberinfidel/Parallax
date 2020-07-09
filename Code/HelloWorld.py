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


	# Audio
	if sdl2.SDL_Init(sdl2.SDL_INIT_AUDIO) != 0:
		raise RuntimeError("Cannot initialize audio system: {}".format(sdl2.SDL_GetError()))

	# int Mix_OpenAudio(int frequency, Uint16 format, int channels, int chunksize)
	if sdlmixer.Mix_OpenAudio(44100, sdlmixer.MIX_DEFAULT_FORMAT, 2, 1024):
		raise RuntimeError("Cannot open mixed audio: {}".format(sdlmixer.Mix_GetError()))
	sdlmixer.Mix_AllocateChannels(64)

	sound_file = RESOURCES.get_path("Cat.wav")
	sample = sdlmixer.Mix_LoadWAV(sdl2.ext.compat.byteify(sound_file, "utf-8"))
	if sample is None:
		raise RuntimeError("Cannot open audio file: {}".format(sdlmixer.Mix_GetError()))

	count = 5
	while count>0:
		channel = sdlmixer.Mix_PlayChannel(channel=-1, chunk=sample, loops=0)
		sdlmixer.Mix_SetPosition(channel,270,100)
		print(channel)
		if channel == -1:
			raise RuntimeError("Cannot play sample: {}".format(sdlmixer.Mix_GetError()))

		# while sdlmixer.Mix_Playing(channel):
		sdl2.SDL_Delay(800)
		count -=1

	sdlmixer.Mix_CloseAudio()
	sdl2.SDL_Quit(sdl2.SDL_INIT_AUDIO)




