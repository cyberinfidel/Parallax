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

class Block(object):
	def __init__(self):
		self.blist=[]
		self.count=0
		self.hash=-1

	@classmethod
	def fromPixels(cls,pixels,x,y):
		block=cls()
		block.blist=[0]*8
		for by in range(0, 8):
			val=block.blist[by]
			pix=pixels[y * 8 + by]
			for bx in range(0, 8):
				val=val<<1
				if pix[x * 8 + 7-bx] == 0xffffffff:
					val+=1
			block.blist[by]=val
		block.count=1
		block.calcHash()
		return block

	def __eq__(self, other):
		if self.hash!=other.hash:
			return
		for row in self.blist:
			for other_row in other.blist:
				if row!=other_row:
					return False
		return True

	def __gt__(self, other):
		return self.count>other.count

	def diff(self, other):
		ret=0
		for index in range(8):
			if self.blist[index]!=other.blist[index]:
				ret+=1
		return ret

	# def append(self,thing):
	# 	self.blist.append(thing)
	# 	self.calcHash()

	def calcHash(self):
		# if len(self.blist)!=8:
		# 	self.hash=-1
		# 	print("Bad block")
		# else:
			self.hash=0
			for pix in self.blist:
				if pix==1:
					self.hash+=1

	@classmethod
	def black(cls):
		ret = cls()
		ret.blist=[0]*8
		ret.calcHash()
		return ret

	@classmethod
	def white(cls):
		ret = cls()
		ret.blist=[1]*8
		ret.calcHash()
		return ret

	# count diff between blocks with tolerance cut off
	# returns count or tolerance if hit
	def diffWithTolerance(self,other,tol):
		if abs(self.hash-other.hash)>tol:
			return tol+1 # hash is out by more than tol itself
		ret=0
		for index in range(8):
			if self.blist[index]!=other.blist[index]:
				ret+=1
				if ret==tol:
					return ret
		return ret

	def __str__(self):
		ret=''
		return "TBD"

	def __getitem__(self, item):
		return self.blist[item]

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
			this_block = Block.fromPixels(pixels,x,y)

			# check if this block has been used already
			found = False
			num_blocks=len(blocks)
			for index in range(num_blocks):
				# if this_block.diffWithTolerance(blocks[index],5)<5:
				if this_block==blocks[index]:
					found = True
					# store record of which block this is in output
					image.append(index) # storing images on first pass isn't needed, but let's me draw preview
					blocks[index].count+=1
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

def reprocessImage(file,ren,all_blocks):
	surface = sdl_image.IMG_Load(file.encode("utf-8"))
	pixels = sdl2.ext.PixelView(surface.contents)
	image = Image()
	texture = sdl2.SDL_CreateTextureFromSurface(ren.sdlrenderer, surface)
	for y in range(0, 12):
		for x in range(0, 16):
			this_block = Block.fromPixels(pixels,x,y)
			# find match for block
			best_match=64
			match_index=-1
			for index in range(len(all_blocks)):
				match = this_block.diffWithTolerance(all_blocks[index],best_match)
				if match<best_match:	# found best match so far
					match_index=index
					best_match=match
					if best_match == 0:  # perfect match found so
						break  # don't look further
			if match_index>=0:
				image.append(match_index)  # store best match
			else:
				print("no match found within tolerance - problem")
				exit(1)

	# draw source image
	sdl2.SDL_RenderCopy(ren.sdlrenderer, texture, sdl2.SDL_Rect(0, 0, 128, 96), sdl2.SDL_Rect(0, 0, 128, 96))
	return image

# easier on pico8 I suspect
def renderImage(image,blocks,ren):
	# create all the blocks
	ren_blocks=[]
	for block in blocks:
		pixels=bytearray()
		for row in range(8):
			val=block[row]
			for digit in range(8):
				if val&1==1:
					pixels.append(0xff)
					pixels.append(0xff)
					pixels.append(0xff)
					pixels.append(0xff)
				else:
					pixels.append(0)
					pixels.append(0)
					pixels.append(0)
					pixels.append(0)
				val=val>>1
		ren_block = sdl2.SDL_CreateTexture(ren.sdlrenderer, sdl2.SDL_PIXELFORMAT_ABGR8888,
																			 sdl2.SDL_TEXTUREACCESS_STATIC,
																			 8, 8)
		pointer = (ctypes.c_char * len(pixels)).from_buffer(pixels)
		sdl2.SDL_UpdateTexture(ren_block, None, pointer, 8*4);
		ren_blocks.append(ren_block)

	# draw the image from the blocks
	for y in range(12):
		for x in range(16):
			texture=ren_blocks[image[y*16+x]]
			# texture=ren_blocks[0]
			sdl2.SDL_RenderCopy(ren.sdlrenderer, texture, sdl2.SDL_Rect(0, 0, 8, 8), sdl2.SDL_Rect(128+x*8, y*8, 8, 8))

	for ren_block in ren_blocks:
		sdl2.SDL_DestroyTexture(ren_block)


def run():
	out_blocks=""
	out_images=""
	all_blocks=[]

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
	limit=4000

	# pass 1 - gather all the blocks
	for i in range(0, int(6565 / 2)):
		count+=1
		if count>limit: # stop early
			break
		events = sdl2.ext.get_events() # otherwise window doesn't update
		ren.clear()
		file = f"image-{i*2+1:03}.png"
		sdl2.SDL_SetWindowTitle(window.window,file.encode('utf-8'))
		image, blocks = processImage(file,ren) # also draws left hand side pre-processed

		# add blocks to master list
		for i,block in enumerate(blocks):
			found=False
			for j,b in enumerate(all_blocks):
				if block==b: # better match found update existing record
					all_blocks[j].count+=blocks[i].count
					found=True # found a match of some sort
			if not found: # totally new block
				all_blocks.append(block)

		num_blocks= len(blocks)
		total_blocks+=num_blocks
		if max_blocks<num_blocks:
			max_blocks=num_blocks
		renderImage(image,blocks,ren) # right hand side post-process
		sdl2.SDL_RenderPresent(ren.sdlrenderer)
		window.refresh()


	print(f"Max blocks: {max_blocks}")
	print(f"Total blocks: {total_blocks}")
	print(f"Average blocks: {total_blocks/count}")
	print(f"Processed {count} frames.")

	# sort and choose top blocks
	all_blocks.sort(reverse=True)

	# 1024 is currently all you're planning to store
	# todo: choose final number of blocks to use
	all_blocks=all_blocks[0:1024]
	for i,b in enumerate(all_blocks):
		print(f"Block {i}: {b.count}")

	# pass 2 - build new images with top blocks
	all_images=[]
	count=0
	for i in range(0, int(6565 / 2)):
		count+=1
		if count>limit: # stop early
			break
		ren.clear()
		file = f"image-{i*2+1:03}.png"
		sdl2.SDL_SetWindowTitle(window.window,file.encode('utf-8'))
		image = reprocessImage(file,ren,all_blocks) # also draws left hand side pre-processed
		all_images.append(image)
		renderImage(image,all_blocks,ren) # right hand side post-process
		events = sdl2.ext.get_events() # otherwise window doesn't update
		sdl2.SDL_RenderPresent(ren.sdlrenderer)
		window.refresh()

	fr=0
	while True:
		fr=(fr+1)%len(all_images)
		events = sdl2.ext.get_events() # otherwise window doesn't update
		ren.clear()
		file = f"image-{i*2+1:03}.png"
		sdl2.SDL_SetWindowTitle(window.window,file.encode('utf-8'))
		renderImage(all_images[fr],all_blocks,ren)
		sdl2.SDL_RenderPresent(ren.sdlrenderer)
		window.refresh()
		sdl2.SDL_Delay(10)

	# profit - I mean output it all

if __name__ == "__main__":
	run()