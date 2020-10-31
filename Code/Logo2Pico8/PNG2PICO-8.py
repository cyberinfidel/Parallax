import sdl2
import sdl2.sdlimage as sdl_image
import sdl2.ext
import math


def runLengthEncode(image, max_bits):
	output_string=""
	last=image[0]
	accum=-1
	max_allowed_count = 2**max_bits-1
	max_count=0
	pairs=0
	for i in range(len(image)):
		if image[i]==last and accum<max_allowed_count:
			accum+=1
		else:
			output_string+=f"{accum}{last}"
			last=image[i]
			max_count=max(accum,max_count)
			accum = 0
			pairs+=1
	if accum>0:
		output_string += f"{accum}{last}"
		pairs+=1
	return output_string, max_count,pairs

def runLengthDecode(image, max_bits):
	output_string=""
	output_values=[]
	for i in range(int(len(image)/2)):
		for j in range(int(image[i*2])+1):
			output_string+=image[i*2+1]
	# 		print(f"{int(image[i*2])+1}{image[i*2+1]},",end="")
	# print("")
	return output_values, output_string

def squeeze1to64(image):
	# 1 bit to 6 bits (64 values) so 6 values per character
	pass
def squeeze2to64(image):
	# 2 bits to 6 bits (64 values) so 3 values per character
	output_string=""
	for i in range(len(image)):
		if i%3==0:
			out=int(image[i])
		elif i%3==1:
			out+=int(image[i])*4
		else:
			output_string+=chr(out+int(image[i])*16 + 35)
	if out>0:	# add any leftovers from non-multiples of 3 input
		output_string += chr(out+ 35)
		# pad with zeros for anything still missing (happens when last values were 0)
		# todo: consider trimming 0 values routinely and pad on expand to save data (why not?)
	while(len(output_string)*3<len(image)):
		output_string+=chr(35)

	return output_string

def squeeze3to64(image):
	# 3 bits to 6 bits (64 values) so 2 values per character
	output_string=""
	for i in range(int(len(image)/2)):
		if int(image[i*2])>7:
			print(f"Bad value {i*2} {image[i*2]}")
		if int(image[i*2+1])>7:
			print(f"Bad value {i*2+1} {image[i*2+1]}")
		output_string+= chr(int(image[i*2+1])*8+int(image[i*2]) + 35)
	return output_string

def squeeze4to64(image):
	# 4 bits to 6 bits (64 values) so 1.5 values per character
	# i.e. do 3 values into 12/2 characters
	pass

def inflate64to1(image):
	pass

def inflate64to2(image,length):
	output_string=""
	for i in range(len(image)):
		raw=ord(image[i])-35
		output_string += str(raw % 4)
		output_string += str(int(raw / 4)%4)
		output_string += str(int(raw / 16) % 4)
	# remove any extra 0s from the end due to image not being multiple of 3 in length
	while(len(output_string)>length):
		output_string=output_string[:-1]
	return output_string

def inflate64to3(image,length):
	output_string=""
	for i in range(len(image)):
		raw=ord(image[i])-35
		output_string += str(raw % 8)
		output_string += str(int(raw / 8))
	while(len(output_string)>length):
		output_string=output_string[:-1]
	return output_string

def inflate64to4(image):
	pass


def standardPaletteImage(p8_image):
	output=""
	bad=False
	for i in range(0, int(len(p8_image) / 2)):
		output+=f"{p8_image[i * 2 + 1]:x}{p8_image[i * 2]:x}"
		if p8_image[i] > 15 and not bad:
			print("-- found at least one bad pixel")
			bad=True
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
	surface = sdl_image.IMG_Load("64x64Monster.png".encode("utf-8"))
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
	custom_palette_image = customPaletteImage(p8_custpal_image)
	print(custom_palette_image)
	print(f"Length: {len(custom_palette_image)} characters")

	print(f"Custom palette ({len(image_pal)} colours)")
	print("{",end="")
	for col in image_pal:
		print(f"{col},",end='')
	print("}")

	# try to make image data smaller
	length=len(image_pal)-1
	min_bits=0
	while length>0:
		min_bits+=1
		length=math.floor(length/2)

	print(f"Could be squeezed to {min_bits} bits per pixel")

	image_64_string=[None,squeeze1to64,squeeze2to64,squeeze3to64,squeeze4to64][min_bits](custom_palette_image)
	print("= Squeezed to base64 ascii from character 35: =")
	print(image_64_string)
	print(f"Length: {len(image_64_string)} characters")
	# verify by inflating again
	infl_string=[None,inflate64to1,inflate64to2,inflate64to3,inflate64to4,][min_bits](image_64_string,w*h)
	if infl_string!=custom_palette_image:
		print("Warning: problem with base64 encoding of non-RLE image.")
		print("org:"+custom_palette_image)
		print("out:"+infl_string)
	else:
		print("inflation matches")

	print("Raw image RLE:")
	RLE_string, max_count, pairs = runLengthEncode(custom_palette_image,min_bits)
	# for i in range(len(counts)):
	#  print(f"Found {counts[i]} of {values[i]}")
	# print(f"Max count is {max_count}")
	print(RLE_string)
	print(f"Length: {len(RLE_string)} characters")
	print(f"Max count: {max_count} duplicates")
	print(f"Pairs: {pairs} count/values")

	# verify by decoding
	decoded,decoded_string=runLengthDecode(RLE_string,min_bits)
	if decoded_string!=custom_palette_image:
		print("Warning: problem with RLE.")
		print("org:"+custom_palette_image)
		print("out:"+decoded_string)
	else:
		print("decode matches")
	# for i in range(int(len(RLE_string)/2)):
		# 	print(f"{RLE_string[i*2]}{RLE_string[i*2+1]},", end="")


	print("= RLE squeezed to base64 ascii from character 35: =")
	RLE_64_string=[None,squeeze1to64,squeeze2to64,squeeze3to64,squeeze4to64][min_bits](RLE_string)
	print(RLE_64_string)
	print(f"Length: {len(RLE_64_string)} characters")

	# verify by inflating again
	infl_string=[None,inflate64to1,inflate64to2,inflate64to3,inflate64to4,][min_bits](RLE_64_string,len(RLE_string))
	if infl_string!=RLE_string:
		print("Warning: problem with base64 encoding.")
		print("org:"+RLE_string)
		print("out:"+infl_string)
	else:
		print("inflation matches")

	decoded,decoded_string=runLengthDecode(infl_string,min_bits)
	if decoded_string!=custom_palette_image:
		print("Warning: problem with RLE.")
		print("org:"+custom_palette_image)
		print("out:"+decoded_string)
	else:
		print("decode matches")

	# for i in range(len(counts)):
	#  print(f"Found {counts[i]} of {values[i]}")
	# print(f"Max count is {max_count}")
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