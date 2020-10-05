import sdl2
import sdl2.sdlimage as sdl_image
import sdl2.ext
import ctypes

header="""pico-8 cartridge // http://www.pico-8.com
version 29
__lua__

local fr_num=0
function _update() end
function _draw()
 cls()
-- fr_num=(fr_num+1)%num_frames
 fr_num+=1
 if fr_num==num_frames then
  load('badbadapple$$.p8')
 end
 --update sprites
 for b=1,#blocks[fr_num] do --0 is always black
  for row=0,7 do
   local st=sub(blocks[fr_num][b],row*2+1,row*2+2)
   local val=tonum("0x"..st)
   for col=0,7 do
    sset((8+col+b*8)%128,
        row+((b+1)\\16)*8,
        (val%2==1) and 7 or 0)
    val=flr(val>>>1)
   end
  end
 end
 for i=0,191 do
  local fr=ord(sub(frames[fr_num],i+1,i+1))
  spr(fr-35,i%16*8,i\\16*8+18)
 end
end
function _init()
for x=8,15 do
for y=0,8 do
 sset(x,y,7)
end
end

frames={[0]=
"""

middle="""
}
blocks={[0]=
"""

footer="""
}
num_frames=#frames
end
"""

class Image(list):
	def __str__(self):
		ret = '"'
		for v in self:
			ret+=str(v)
		return ret+'"'

class Block(list):
	def __eq__(self, other):
		for pix in self:
			for other_pix in other:
				if pix!=other_pix:
					return False
		return True

	def diff(self, other):
		ret=0
		for index in range(len(self)):
			if self[index]!=other[index]:
				ret+=1
		return ret

	@classmethod
	def black(cls):
		return cls([0]*64)

	@classmethod
	def white(cls):
		return cls([1]*64)

	# count diff between blocks with tolerance cut off
	# returns count or tolerance if hit
	def diffWithTolerance(self,other,tol):
		ret=0
		for index,pix in enumerate(self):
			if pix!=other[index]:
				ret+=1
				if ret==tol:
					return ret
		return ret

	def __str__(self):
		ret=''
		return "TBD"



def processImage(file,ren):
	surface = sdl_image.IMG_Load(file.encode("utf-8"))
	pixels = sdl2.ext.PixelView(surface.contents)
	image = Image()
	blocks = [
		Block.black(),
		Block.white()
	]
	# w = surface.contents.w
	# h = surface.contents.h

	# print(f"Opened image - width:{w}, height:{h}.")
	# print("Processing image...")
	texture = sdl2.SDL_CreateTextureFromSurface(ren.sdlrenderer, surface)

	new_block = 0
	for y in range(0, 12):
		for x in range(0, 16):
			this_block = Block()
			# get the next block from image
			for by in range(0, 8):
				for bx in range(0, 8):
					#					print(f"0x{pixels[y][x]:01x}")
					if pixels[y * 8 + by][x * 8 + bx] == 0xffffffff:
						this_block.append(1)
#						print("1", end='')
					else:
						this_block.append(0)
#						print("0", end='')
#				print('')
			#				this_block.append(pixels[y][x])
			# check if this block has been used already
			found = False
			for index in range(len(blocks)):
				if this_block.diffWithTolerance(blocks[index],5)<5:
				# if this_block==old_block:
					found = True
					# store record of which block this is in output
					image.append(index)
					break
			if not found:
				# if not store it
				image.append(len(blocks))
				# store record of which block this is in output
				blocks.append(this_block)

	# draw source image
	sdl2.SDL_RenderCopy(ren.sdlrenderer, texture, sdl2.SDL_Rect(0, 0, 128, 96), sdl2.SDL_Rect(0, 0, 128, 96))

	# output
	# print(f"Image: {file}")
	# for y in range(0, 12):
	# 	for x in range(0, 16):
	# 		print(f" {image[x + y * 16]}", end="")
	# 	print("")

	# print("Blocks:",len(blocks))
	return image, blocks

# easier on pico8 I suspect
def renderImage(image,blocks,ren):
	# create all the blocks
	ren_blocks=[]
	for block in blocks:
		ren_block=sdl2.SDL_CreateTexture(ren.sdlrenderer,sdl2.SDL_PIXELFORMAT_ABGR8888,
																						 sdl2.SDL_TEXTUREACCESS_STATIC,
																						 8,8)
		pixels=bytearray()
		for p in range(64):
			if block[p]==1:
				pixels.append(0xff)
				pixels.append(0xff)
				pixels.append(0xff)
				pixels.append(0xff)
			else:
				pixels.append(0)
				pixels.append(0)
				pixels.append(0)
				pixels.append(0)

		pointer = (ctypes.c_char * len(pixels)).from_buffer(pixels)
		sdl2.SDL_UpdateTexture(ren_block, None, pointer, 8*4);
		ren_blocks.append(ren_block)

	# draw the image from the blocks
	for y in range(12):
		for x in range(16):
			texture=ren_blocks[image[y*16+x]]
			# texture=ren_blocks[0]
			sdl2.SDL_RenderCopy(ren.sdlrenderer, texture, sdl2.SDL_Rect(0, 0, 8, 8), sdl2.SDL_Rect(128+x*8, y*8, 8, 8))


def run():
	out_blocks=""
	out_images=""

	sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_EVERYTHING)
	sdl_image.IMG_Init(sdl_image.IMG_INIT_PNG)

	window = sdl2.ext.Window("BAConv", size=(1024, 384))
	window.show()
	ren = sdl2.ext.Renderer(window, flags=sdl2.SDL_RENDERER_ACCELERATED)
	# makes zoomed graphics blocky (for retro effect)
	sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"nearest")
	# makes the graphics look and act like the desired screen size, even though they may be rendered at a different one
	sdl2.SDL_RenderSetLogicalSize(ren.sdlrenderer, 256, 96)
	max_blocks=0
	total_blocks=0
	count=0
	cart=1

	for i in range(0,int(6565/2)):
		count+=1
	# for i in range(254, 355):
	# while True:
	# 	i=304
		events = sdl2.ext.get_events()
		ren.clear()
		file = f"image-{i*2+1:03}.png"
		sdl2.SDL_SetWindowTitle(window.window,file.encode('utf-8'))
		image, blocks = processImage(file,ren) # also draws left hand side pre-processed
		num_blocks= len(blocks)
		total_blocks+=num_blocks
		if max_blocks<num_blocks:
			max_blocks=num_blocks
			# print(f"New max:{num_blocks}")
		renderImage(image,blocks,ren) # right hand side post-process
		sdl2.SDL_RenderPresent(ren.sdlrenderer)
		window.refresh()

		# output encoded image
		out_images+='"'
		for i in range(0,192):
			if image[i]+35==92:
				out_images+='\\\\'
			else:
				out_images+=f"{chr(image[i]+35)}"
		out_images+='",\n'

		# output encoded blocks
		out_blocks+="{"
		for block in blocks[2:]:
			out_blocks+='"'
			for y in range(0,8):
				val = 0
				for x in range(0,8):
					if block[y*8+x]==1:
						val+=2**x
				out_blocks+=f"{val:02x}"
			out_blocks+='",'
		out_blocks+="},\n"

		if count%40==0:

			output=header.replace('$$',f"{(cart+1):02}")+out_images+middle+out_blocks+footer
			outfile=open(f"badbadapple{cart:02}.p8",'w')
			outfile.write(output)
			outfile.close()

			out_images=''
			out_blocks=''
			cart+=1


	print(out_images)


	print(f"Max blocks: {max_blocks}")
	print(f"Total blocks: {total_blocks}")
	print(f"Average blocks: {total_blocks/count}")
	print(f"Processed {count} frames.")

if __name__ == "__main__":
	run()