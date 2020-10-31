# encodes scanlines into alternating black and white values
# potentially with spill over to next line or even frame


import sdl2
import sdl2.sdlimage as sdl_image
import sdl2.ext
import ctypes


class Image(list):
	def __str__(self):
		ret = '"'
		for v in self:
			ret+=str(v)+","
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

	@classmethod
	def fromData(cls,data):
		block=cls()
		block.count=int(data[1])
		block.hash=int(data[0])
		for val in data[2:]:
			block.blist.append(int(val))
		print(block)
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
		self.hash=0
		for pix in self.blist:
			self.hash+=pix

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
		ret=0
		for index in range(8):
			if self.blist[index]!=other.blist[index]:
				# mismatch so calc how big diff is
				this = self.blist[index]
				oth = other.blist[index]
				for i in range(8):
					if this%2!=oth%2:
						ret+=1
						if ret==tol:
							return ret
					this=int(this/2)
					oth=int(oth/2)
		return ret

	def __str__(self):
		ret=''
		return self.serialize()

	def __getitem__(self, item):
		return self.blist[item]

	def serialize(self):
		ret= f"{self.hash},{self.count},"
		for b in self.blist:
			ret+=f"{b},"
		return ret[0:-1]

# looks for all 8x8 blocks present in frames
# checks for matches and stores only unique blocks
def processImage(file,ren):
	surface = sdl_image.IMG_Load(file.encode("utf-8"))
	pixels = sdl2.ext.PixelView(surface.contents)
	image = Image()
	# w = surface.contents.w
	# h = surface.contents.h

	# print(f"Opened image - width:{w}, height:{h}.")
	# print("Processing image...")
	texture = sdl2.SDL_CreateTextureFromSurface(ren.sdlrenderer, surface)

	max_count=0
	count=0
	col=(pixels[0]==0xffffffff)
	image.append(col)	# store whether frame starts with black or white
	image.append(0)	# for bits count
	for y in range(0, 48):
		for x in range(0, 64):
			pix= (pixels[y][x]==0xffffffff)
			if col==pix:
				count+=1
			else:
				image.append(count)
				max_count=max(count,max_count)
				count=0
				col=pix
	if count>0:
		image.append(count)

	max_count = max(count, max_count)

	bits=0
	while 2**bits<max_count:
		bits+=1
	image[1]=bits

	# draw source image
	sdl2.SDL_RenderCopy(ren.sdlrenderer, texture, sdl2.SDL_Rect(0, 0, 64, 48), sdl2.SDL_Rect(0, 0, 128, 96))
	sdl2.SDL_DestroyTexture(texture)

	# output
	# print(f"Image: {file}")
	# for y in range(0, 12):
	# 	for x in range(0, 16):
	# 		print(f" {image[x + y * 16]}", end="")
	# 	print("")

	# print("Blocks:",len(blocks))
	return image

# looks through 8x8 blocks in frames for best match with
# "palette" of blocks passed to it
# returns list of best matches for each frame
def reprocessImage(file,ren,all_blocks):
	surface = sdl_image.IMG_Load(file.encode("utf-8"))
	pixels = sdl2.ext.PixelView(surface.contents)
	image = Image()
	texture = sdl2.SDL_CreateTextureFromSurface(ren.sdlrenderer, surface)
	for y in range(0, 6):
		for x in range(0, 8):
			this_block = Block.fromPixels(pixels,x,y)
			# find match for block
			best_match=64
			match_index=-1
			for index in range(len(all_blocks)):
				match = this_block.diffWithTolerance(all_blocks[index],best_match)
				if match<=best_match:	# found best match so far
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
	sdl2.SDL_RenderCopy(ren.sdlrenderer, texture, sdl2.SDL_Rect(0, 0, 64, 48), sdl2.SDL_Rect(0, 0, 128, 96))
	return image

# easier on pico8 I suspect
def renderImage(image,ren):
	# create all the blocks
	frame = sdl2.SDL_CreateTexture(ren.sdlrenderer, sdl2.SDL_PIXELFORMAT_ABGR8888,
																		 sdl2.SDL_TEXTUREACCESS_STATIC,
																		 64, 48)
	pixels = bytearray()
	col=image[0] # first value is whether black or not
	for val in image[2:]:
		for count in range(val+1):
				if col:
					pixels.append(0xff)
					pixels.append(0xff)
					pixels.append(0xff)
					pixels.append(0xff)
				else:
					pixels.append(0)
					pixels.append(0)
					pixels.append(0)
					pixels.append(0)
		col=not col
	pointer = (ctypes.c_char * len(pixels)).from_buffer(pixels)
	sdl2.SDL_UpdateTexture(frame, None, pointer, 64*4);

	# draw the frame
	sdl2.SDL_RenderCopy(ren.sdlrenderer, frame, sdl2.SDL_Rect(0, 0, 64, 48), sdl2.SDL_Rect(128, 0, 128, 96))

	sdl2.SDL_DestroyTexture(frame)


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

	frames=[]
	count=0
	limit=8000 # only deal with this many frames

	pass1=True # True means calculate blocks, False means load from pre-calculated file

	if pass1:
		# pass 1 - gather all the blocks
		for i in range(0, int(6565 / 4)):
		# for i in range(43, int(600 / 4)):
			count+=1
			if count>limit: # stop early
				break
			events = sdl2.ext.get_events() # otherwise window doesn't update
			for event in events:
				if event.type == sdl2.SDL_QUIT:
					exit(0)
			ren.clear()
			file = f"image-{i*4+1:03}.png"
			sdl2.SDL_SetWindowTitle(window.window,file.encode('utf-8'))
			frame = processImage(file,ren) # also draws left hand side pre-processed
			frames.append(frame)

			renderImage(frame,ren) # right hand side post-process
			sdl2.SDL_RenderPresent(ren.sdlrenderer)
			window.refresh()


		print(f"Processed {count} frames.")

		values=0
		size=0
		for frame in frames:
			values+=len(frame)
			size+=frame[1]*(len(frame)-2)+1
			print(frame)

		print(f"Raw values: {values}")
		print(f"Average values per frame: {values/len(frames)}")
		print(f"Theoretical size: {size/8}")

		exit(0)


		# store blocks in file
		file_lines=[]
		for block in all_blocks:
			file_lines.append(block.serialize())

		with open("data_file.txt", "w") as write_file:
			write_file.writelines("\n".join(file_lines))
	else:
		# read in blocks from file (quicker)
		with open("data_file.txt", "r") as read_file:
			file_lines=read_file.readlines()
			all_blocks=[]
			for line in file_lines:
				all_blocks.append(Block.fromData(line.split(",")))

	# sort and choose top blocks
	all_blocks.sort(reverse=True)

	# 1024 is currently all you're planning to store
	# todo: choose final number of blocks to use
	# all_blocks=all_blocks[0:1024]
	for i,b in enumerate(all_blocks):
		print(f"Block {i}: {b.count}")

	# pass 2 - build new images with top blocks
	all_images=[]
	count=0
	# for i in range(43, int(6509 / 4)):
	for i in range(0, int(6565 / 4)):
	# for i in range(43, int(600 / 4)):
		count+=1
		if count>limit: # stop early
			break
		ren.clear()
		file = f"image-{i*4+1:03}.png"
		sdl2.SDL_SetWindowTitle(window.window,file.encode('utf-8'))
		image = reprocessImage(file,ren,all_blocks) # also draws left hand side pre-processed
		all_images.append(image)
		renderImage(image,all_blocks,ren) # right hand side post-process
		events = sdl2.ext.get_events() # otherwise window doesn't update
		sdl2.SDL_RenderPresent(ren.sdlrenderer)
		window.refresh()

	# play back final frames in loop
	fr=0
	while True:
		fr=(fr+1)%len(all_images)
		events = sdl2.ext.get_events() # otherwise window doesn't update
		for event in events:
			if event.type == sdl2.SDL_QUIT:
				exit(0)
		ren.clear()
		file = f"image-{i*2+1:03}.png"
		sdl2.SDL_SetWindowTitle(window.window,file.encode('utf-8'))
		renderImage(all_images[fr],all_blocks,ren)
		sdl2.SDL_RenderPresent(ren.sdlrenderer)
		window.refresh()
#		sdl2.SDL_Delay(10)

	# profit - I mean output it all

if __name__ == "__main__":
	run()