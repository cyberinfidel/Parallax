import sdl2
import sdl2.sdlimage as sdl_image
import sdl2.ext

sdl_image.IMG_Init(sdl_image.IMG_INIT_PNG)

sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)

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

p8_image = []
p8_mismatches = []
image_pal = []
surface = sdl_image.IMG_Load("LogoCroppedMore.png".encode("utf-8"))
pixels = sdl2.ext.PixelView(surface.contents)

w=surface.contents.w
h=surface.contents.h

print(f"Opened image - width:{w}, height:{h}.")
print("Processing image...")
for y in range(0,h):
	for x in range(0,w):
		col=-1
		pix=pixels[y][x]
		# print(f"Pixel: 0x{pix:02x}")
		for index, pcol in enumerate(p8pal):
			if pix==pcol:
				col=index
				if col>15:
					col+=112	# extended palette is from 128 for some reason
				if col not in image_pal:
					image_pal.append(col)

				break

		if col==-1 and pix not in p8_mismatches:
			p8_mismatches.append(pix)
		else:
			p8_image.append(col)

if len(p8_mismatches)>0:
	print("Warning: mismatches with pico-8 palette:")
	for col in p8_mismatches:
		print(f"0x{col:02x}")
else:
	print("No colour mismatches with pico-8 palette (this is good).")
print(f"Image has {len(image_pal)} colours.")
if len(image_pal)>16:
	print("Warning: displaying more than 16 colours on pico-8 may be tricky.")

line=0
print("p8_image={",end='')
for pix in p8_image:
	print(f"{pix},",end='')
	line+=1
	if line>=w:
		line=0
		print("")
print("}")

print("p8_image_pal={",end='')
for col in image_pal:
	print(f"{col},",end='')
print("}")
