import sdl2
import sdl2.sdlimage as sdl_image
import sdl2.ext
import math


def runLengthEncode(image, max_bits):
	output_string=""
	last=image[0]
	accum=1
	max_allowed_count = 2**max_bits-1
	counts=[]
	values=[]
	max_count=0
	for i in range(len(image)):
		if image[i]==last and accum<max_allowed_count: # hacked to not exceed 3 bits atm todo: make more generic
			accum+=1
		else:
			values.append(last)
			values.append(accum)
			output_string+=f"{accum}{last}"	# -1 because never going to have count of 0
			last=image[i]
			max_count=max(accum,max_count)
			accum = 1
	return values, max_count, output_string

def squeeze1to64(image):
	# 1 bit to 6 bits (64 values) so 6 values per character
	pass
def squeeze2to64(image):
	# 2 bits to 6 bits (64 values) so 3 values per character
	pass
def squeeze3to64(image):
	# 3 bits to 6 bits (64 values) so 2 values per character
	output_string=""
	output_values=[]
	for i in range(int(len(image)/2)):
		if image[i*2]>7:
			print(f"Bad value {i*2} {image[i*2]}")
		if image[i*2+1]>7:
			print(f"Bad value {i*2+1} {image[i*2+1]}")
		output_values.append(image[i*2+1]*8+image[i*2] + 35)
		output_string+= chr(output_values[-1])
	return output_values,output_string

def squeeze4to64(image):
	# 4 bits to 6 bits (64 values) so 1.5 values per character
	# i.e. do 3 values into 12/2 characters
	pass

def standardPaletteImage(p8_image):
	output=""
	for i in range(0, int(len(p8_image) / 2)):
		output+=f"{p8_image[i * 2 + 1]:x}{p8_image[i * 2]:x}"
		if p8_image[i] > 15:
			print("-- bad pixel")
	return(output)

def customPaletteImage(p8_custpal_image):
	output=""
	for i in range(0, int(len(p8_custpal_image) / 2)):
		output+=f"{p8_custpal_image[i * 2 + 1]:x}{p8_custpal_image[i * 2]:x}"
		if p8_custpal_image[i] > 15:
			print("-- bad pixel")
	return(output)

def run():
	sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_EVERYTHING)
	sdl_image.IMG_Init(sdl_image.IMG_INIT_PNG)


	p8pal=[
		# basic
		0xff000000,  # black
		0xff1D2B53,  # dark-blue
		0xff7E2553,  # dark-purple
		0xff008751,  # dark-green
		0xffAB5236,  # brown
		0xff5F574F,  # dark-grey
		0xffC2C3C7,  # light-grey
		0xffFFF1E8,  # white
		0xffFF004D,  # red
		0xffFFA300,  # orange
		0xffFFEC27,  # yellow
		0xff00E436,  # green
		0xff29ADFF,  # blue
		0xff83769C,  # lavender
		0xffFF77A8,  # pink
		0xffFFCCAA,  # light-peach
		# extended
		0xff291814, #darkest-grey
		0xff111D35, #darker-blue
		0xff422136, #darker-purple
		0xff125359, #blue-green
		0xff742F29, #dark-brown
		0xff49333B, #darker-grey
		0xffA28879, #medium-grey
		0xffF3EF7D, #light-yellow
		0xffBE1250, #dark-red
		0xffFF6C24, #dark-orange
		0xffA8E72E, #light-green
		0xff00B543, #medium-green
		0xff065AB5, #medium-blue
		0xff754665, #mauve
		0xffFF6E59, #dark peach
		0xffFF9D81, #peach
	]

	p8_image = [] # output image data for palette using standard 16 colours
	p8_custpal_image = [] # output image data for only palette used - indexes into image_pal
	p8_mismatches = [] # colours that don't match ones in p8pal - can't be displayed by pico-8
	image_pal = [] # output image palette
	standard_colours=True
	surface = sdl_image.IMG_Load("BowieP8.png".encode("utf-8"))
	pixels = sdl2.ext.PixelView(surface.contents)
	w=surface.contents.w
	h=surface.contents.h

	window = sdl2.ext.Window("PNG2PICO-8", size=(w*16, h*8))
	window.show()
	ren = sdl2.ext.Renderer(window, flags=sdl2.SDL_RENDERER_ACCELERATED)
	# makes zoomed graphics blocky (for retro effect)
	sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"nearest")
	# makes the graphics look and act like the desired screen size, even though they may be rendered at a different one
	sdl2.SDL_RenderSetLogicalSize(ren.sdlrenderer, w*2, h)
	ren.clear()


	texture = sdl2.SDL_CreateTextureFromSurface(ren.sdlrenderer, surface)

	# draw source image
	sdl2.SDL_RenderCopy(ren.sdlrenderer, texture, sdl2.SDL_Rect(0, 0, w*2, h), sdl2.SDL_Rect(0, 0, w, h))



	print(f"Opened image - width:{w}, height:{h}.")
	print("Processing image...")
	for y in range(0,h):
		for x in range(0,w):
			col=-1
			output=0
			pix=pixels[y][x]
			if pix==0: pix=0xff000000 # transparent pixels all go to black
			# look for pixel value in p8 colours
			for index, pcol in enumerate(p8pal):
				if pix==pcol:
					col=index
					if col>15:
						col+=112	# extended palette is from 128 for some reason
						standard_colours=False
					# check if we've added this to the image custom palette
					if col not in image_pal:
						output_index=len(image_pal) # col will be last in palette so far
						image_pal.append(col)
					else:
						output_index=image_pal.index(col)
					output_index_standard=index # standard palette

			if col==-1 and pix not in p8_mismatches:
				p8_mismatches.append(pix)
				output_index=0	# set as black for output
			p8_image.append(output_index_standard)
			p8_custpal_image.append(output_index)

	if len(p8_mismatches)>0:
		print("Warning: mismatches with pico-8 palette:")
		for col in p8_mismatches:
			print(f"0x{col:02x}")
	else:
		print("No colour mismatches with pico-8 palette (this is good).")
	if standard_colours:
		print("Image uses only standard colours.")
	else:
		print("Image uses extended palette")

	print(f"Image has {len(image_pal)} colours.")
	if len(image_pal)>16:
		print("Warning: displaying more than 16 colours on pico-8 may be tricky.")

	print("= Standard palette image =")
	standard_palette_image = standardPaletteImage(p8_image)
	print(standard_palette_image)
	print(f"Length: {len(standard_palette_image)} characters")

	# output tables for pico-8
	print("= Custom palette image =")
	custom_palette_image = standardPaletteImage(p8_custpal_image)
	print(custom_palette_image)
	print(f"Length: {len(custom_palette_image)} characters")

	print("Custom palette")
	print("{",end="")
	for col in image_pal:
		print(f"{col},",end='')
	print("}")

	# squeeze image
	length=len(image_pal)-1
	min_bits=0
	while length>0:
		min_bits+=1
		length=math.floor(length/2)

	print(f"Could be squeezed to {min_bits} bits per pixel")

	image_64,image_64_string=[None,squeeze1to64,squeeze2to64,squeeze3to64,squeeze4to64][min_bits](p8_custpal_image)
	print("= Squeezed to base64 ascii from character 35: =")
	print(image_64_string)
	print(f"Length: {len(image_64_string)} characters")

	print("Unencoded to base64 RLE:")
	RLE_values, max_count, RLEraw = runLengthEncode(p8_custpal_image,min_bits)
	# for i in range(len(counts)):
	#  print(f"Found {counts[i]} of {values[i]}")
	# print(f"Max count is {max_count}")
	print(RLEraw)
	print(f"Length: {len(RLEraw)} characters")

	print("= RLE squeezed to base64 ascii from character 35: =")
	RLE_64,RLE_64_string=[None,squeeze1to64,squeeze2to64,squeeze3to64,squeeze4to64][min_bits](RLE_values)
	# for i in range(len(counts)):
	#  print(f"Found {counts[i]} of {values[i]}")
	# print(f"Max count is {max_count}")
	print(RLE_64_string)
	print(f"Length: {len(RLE_64_string)} characters")
	print(f"Squeezing vs raw: {len(image_64_string)/len(p8_custpal_image)*100}%")
	print(f"RLE and squeezing size vs raw: {len(RLE_64_string)/len(p8_custpal_image)*100}%")

	while True:
		events = sdl2.ext.get_events()
		for event in events:
			if event.type == sdl2.SDL_QUIT:
				exit(0)

		sdl2.SDL_RenderPresent(ren.sdlrenderer)
		window.refresh()



if __name__ == "__main__":
	run()