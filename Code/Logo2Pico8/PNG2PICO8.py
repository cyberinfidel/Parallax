# -*- coding: UTF-8 -*-
import sdl2
import sdl2.sdlimage as sdl_image
import sdl2.ext
import math

char_table=["\\0","¹","²","³","⁴","⁵","⁶","⁷","⁸","\\t","\\n","ᵇ","ᶜ","\\r","ᵉ","ᶠ","▮","■","□","⁙","⁘","‖","◀","▶","「","」","¥","•","、","。","゛","゜"," ","!","\\\"","#","$","%","&","'","(",")","*","+",",","-",".","/","0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","?","@","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","[","\\\\","]","^","_","`","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","{","|","}","~","○","█","▒","🐱","⬇️","░","✽","●","♥","☉","웃","⌂","⬅️","😐","♪","🅾️","◆","…","➡️","★","⧗","⬆️","ˇ","∧","❎","▤","▥","あ","い","う","え","お","か","き","く","け","こ","さ","し","す","せ","そ","た","ち","つ","て","と","な","に","ぬ","ね","の","は","ひ","ふ","へ","ほ","ま","み","む","め","も","や","ゆ","よ","ら","り","る","れ","ろ","わ","を","ん","っ","ゃ","ゅ","ょ","ア","イ","ウ","エ","オ","カ","キ","ク","ケ","コ","サ","シ","ス","セ","ソ","タ","チ","ツ","テ","ト","ナ","ニ","ヌ","ネ","ノ","ハ","ヒ","フ","ヘ","ホ","マ","ミ","ム","メ","モ","ヤ","ユ","ヨ","ラ","リ","ル","レ","ロ","ワ","ヲ","ン","ッ","ャ","ュ","ョ","◜","◝",]

# uses the above table to encode a list of int values between 0 and 255 inclusive
# into a string from which a value with index can be retrieved on PICO-8 via a
# simple ord(str,index) command
# Only thing to remember is lua's dumb count from 1 for tables
def encode8bitDataAsPICO8String(data):
	str=''
	for i,d in enumerate(data):
		if (d+80)%256==0:
			if i+1<len(data) and 255-data[i+1]>=48 and 255-data[i+1]<=57:
				str+='\\000'
			else:
				str+='\\0'
		else:
			str+=char_table[(d+80)%256]
	return str

disable_slash_workaround = False # only needed for 6 bit
# zep's own pico-8 code for binary strings
# function escape_binary_str(s)
#  local out=""
#  for i=1,#s do
#   local c  = sub(s,i,i)
#   local nc = ord(s,i+1)
#   local pr = (nc and nc>=48 and nc<=57) and "00" or ""
#   local v=c
#   if(c=="\"") v="\\\""
#   if(c=="\\") v="\\\\"
#   if(ord(c)==0) v="\\"..pr.."0"
#   if(ord(c)==10) v="\\n"
#   if(ord(c)==13) v="\\r"
#   out..= v
#  end
#  return out
# end

# my version
def escape_binary_str(s):
	out=""
	for i in range(len(s)):
		c=s[i]
		if i+1<len(s):
			nc=ord(s[i+1])
			if nc>=48 and nc<=57:
				pr='00'
			else:
				pr=''
		v=c
		if(c=='\"'): v='\\\"'
		if(c=="\\"): v="\\\\"
		if(ord(c)==0): v="\\"+pr+"0"
		if(ord(c)==10): v="\\n"
		if(ord(c)==13): v="\\r"
		out+=v
	return out


def runLengthEncode(image, max_bits):
	output=[]
	last=image[0]
	accum=-1
	max_allowed_count = 2**max_bits-1
	max_count=0
	pairs=0
	for i in range(len(image)):
		if image[i]==last and accum<max_allowed_count:
			accum+=1
		else:
			output.append(accum)
			output.append(last)
			last=image[i]
			max_count=max(accum,max_count)
			accum = 0
			pairs+=1
	if accum>0:
		output.append(accum)
		output.append(last)
	else:
		output.append(0)
		output.append(image[-1])
	pairs += 1
	return output, max_count,pairs

def runLengthDecode(image):
	output=[]
	for i in range(int(len(image)/2)):
		for j in range(int(image[i*2])+1):
			output.append(image[i*2+1])
	# 		print(f"{int(image[i*2])+1}{image[i*2+1]},",end="")
	# print("")
	return output

##################################################################
# Run Length Encode only zeros

def runLengthEncodeOnlyZeros(image, max_bits):
	output=[]
	last=image[0]
	if last==0: output.append(0)
	accum=-1
	max_allowed_count = 2**max_bits-1
	max_count=0
	zero_blocks=0
	for i in range(len(image)):
		if image[i]==0:
			if output[-1]!=0: # were we already counting zeros?
				# is first zero so output and reset count
				output.append(0)
				accum=-1
				zero_blocks+=1
			elif accum>=max_allowed_count:
				output.append(accum)
				output.append(0)
				accum=-1
				zero_blocks+=1
			accum+=1
			max_count=max(accum,max_count)
		elif image[i]>0:
			if output[-1]==0: # were we counting zeros?
				output.append(accum) # store count of zeros
			# non-zeros passed straight through
			output.append(image[i])
			last=image[i] # i.e. non-zero
		else: # found first zero
			output.append(0)
			last=0
			accum = 0
	if output[-1]==0:
		output.append(accum)
	return output, max_count, zero_blocks

def runLengthDecodeOnlyZeros(image):
	output=[]
	i=0
	while i in range(int(len(image))):
		if image[i]==0:
			for j in range(int(image[i+1])+1):
				output.append(0)
			i+=2
		else:
			output.append(image[i])
			i+=1
	return output

##################################################################
# 64 value 6 bit conversions
def squeeze1to8bit(image):
	pass

def squeeze2to8bit(image):
	pass

def squeeze3to8bit(image):
	# 3 bits to 6 bits (64 values) so 2 values per character
	#000111222333444555666777
	#000000001111111122222222
	length = len(image)
	out=[]
	# 2x8=16 bits of how long the data actually is
	if(length>2**16):
		print(f"Data too large {length}")
		return []
	out.append((length>>8)&0xff)
	out.append((length)&0xff)
	val=0
	rem=0
	for i in range(len(image)):
		val=(val<<3)+image[i]	# shove away 3 bits of value 8 times for 24 bits of data
		rem+=3
		if i % 8 == 7:  # dump 24 bits into 3 bytes
			out.append((val >> 16) & 0xff)
			out.append((val >> 8) & 0xff)
			out.append(val & 0xff)
			val = 0 # reset
			rem=0
	while rem>0: # dump out any remaining values
		if rem>=8:
			out.append(val>>(rem-8) & 0xff)
		else:
			out.append(val<<(8-rem) & 0xff)
		rem-=8

	return out

def squeeze4to8bit(image,length):
	pass


def inflate8bitto1(image,length):
	pass

def inflate8bitto2(image,length):
	pass

def inflate8bitto3(image,length):
	out=[]
	val=0
	rem=(image[0]<<8)+image[1] # remaining values to extract
	for i in range(2,len(image)):
		val=(val<<8)+image[i] # collect 3*8bit=24bits of data
		if i%3==1:
			for j in range(8): # dump out 8*3bit=24bits of data
				out.append((val>>((7-j)*3))&0x7)
				rem -= 1
			# val=0
			# if out[-1]>15:print("bad value decoding 8bit data")
	if rem>0:
		# trim any trailing 0s from remaining data
		val=val>>(((i+2)%3)*8-rem*3)
	while rem>0:
		out.append((val>>(rem*3-3))&0x7)
		rem-=1

	return out
def inflate8bitto4(image):
	pass


##################################################################
# 64 value 6 bit conversions
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
			out+=int(image[i])*16
			output_string+=encodeChar(out)
	if out>0:	# add any leftovers from non-multiples of 3 input
		output_string += encodeChar(out)
		# pad with zeros for anything still missing (happens when last values were 0)
		# todo: consider trimming 0 values routinely and pad on expand to save data (why not?)
	while(len(output_string)*3<len(image)):
		output_string+=chr(35)

	return output_string

def squeeze3to64(image):
	# 3 bits to 6 bits (64 values) so 2 values per character
	output_string=""
	for i in range(int(len(image)/2)):
		# if int(image[i*2])>7:
		# 	print(f"Bad value {i*2} {image[i*2]}")
		# if int(image[i*2+1])>7:
		# 	print(f"Bad value {i*2+1} {image[i*2+1]}")
		out=int(image[i*2+1])*8+int(image[i*2])
		output_string+= encodeChar(out)
	return output_string

# encodes a value as an ASCII character
# skipping the awkward \ character (92)
def encodeChar(val):
	val+=35
	if disable_slash_workaround:
		return chr(val)
	if val>=92:	# skip \
		val+=1
	return chr(val)

# decodes a value stored as an ASCII character
# skipping the awkward \ character (92)
def decodeChar(c):
	v=ord(c)
	return v - (35 if v<92 else 36)

def listToString(list):
	out=''
	for l in list:
		out+=str(l)
	return out

def stringToList(string):
	list=[]
	for i in range(len(string)):
		list.append(int(string[i]))
	return list

def squeeze4to64(image):
	# 4 bits to 6 bits (64 values) so 1.5 values per character
	# i.e. do 3 values into 12/2 characters
	# 001122334455 i
	# 000111222333 out
	# 001122001122 i%3
	output_string=''
	for i in range(len(image)):
		if (i%3)==0:
			out=int(image[i],16)<<2 # store this pixel in upper bits, but don't output
		elif (i%3)==1:
			# add half of this pixel to stored value from last and output
			out+=int(int(image[i],16)>>2)
			output_string+=encodeChar(out)
			# store other half ready for next
			out=int((int(image[i],16)&0x3)<<4)
		else: # 2
			out+=int(image[i],16)
			output_string += encodeChar(out)

	# dump out last value if length of image isn't multiple of 3
	if len(image)%3==1 or len(image)%3==2:
		output_string+=encodeChar(out)


	return output_string

def inflate64to1(image):
	pass

def inflate64to2(image,length):
	output_string=""
	for i in range(len(image)):
		val=ord(image[i])
		if val>92:
			val-=1 # unskip \ character
		raw=val-35
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
		val=ord(image[i])
		if val>92:
			val-=1 # unskip \ character
		raw=val-35
		output_string += str(raw % 8)
		output_string += str(int(raw / 8))
	while(len(output_string)>length):
		output_string=output_string[:-1]
	return output_string

def inflate64to4(image,length):
	output_string=""
	for i in range(len(image)):
		val=ord(image[i])
		if val>92:
			val-=1 # unskip \ character
		val-=35
		if (i%2)==0:
			# output upper 4 bits
			output_string+=hex((val>>2)&0xf)[2:]
			# store lower 2 bits for next output
			store= (val&0x3)<<2
		else:
			# add upper 2 bits to stored and output
			output_string+=hex(store+(val>>4))[2:]
			# output lower 4 bits
			output_string+=hex(val&0xf)[2:]

	while(len(output_string)>length):
		output_string=output_string[:-1]
	return output_string

def standardPaletteImage(p8_image):
	output=""
	bad=False
	for i in range(0, int(len(p8_image) / 2)):
		output+=f"{p8_image[i * 2 + 1]:x}{p8_image[i * 2]:x}"
		if p8_image[i] > 15 and not bad:
			print("-- found at least one pixel with non-standard colours")
			bad=True
	return(output)

def customPaletteImage(p8_custpal_image):
	output=""
	for i in range(0, int(len(p8_custpal_image) / 2)):
		output+=f"{p8_custpal_image[i * 2 + 1]:x}{p8_custpal_image[i * 2]:x}"
		if p8_custpal_image[i] > 15:
			print("-- pixel outside 16 colour palette")
	return(output)

def analyseRect(pixels,ox,oy,w,h):
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

	for y in range(oy,h):
		for x in range(ox,w):
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
				output_index_standard=0
			p8_image.append(output_index_standard)
			p8_custpal_image.append(output_index)

	return p8_image, p8_custpal_image, image_pal, standard_colours, p8_mismatches


def run():
	sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_EVERYTHING)
	sdl_image.IMG_Init(sdl_image.IMG_INIT_PNG)

	surface = sdl_image.IMG_Load("64x64Monster.png".encode("utf-8"))
	pixels = sdl2.ext.PixelView(surface.contents)
	w=surface.contents.w
	h=surface.contents.h

	# rect to analyse
	start_x=0	# note: inclusive
	start_y=0
	end_x=w	# note: not inclusive
	end_y=h

	num_pixels=(end_y-start_y)*(end_x-start_x)
	print(f"Opened image - width:{w}, height:{h}.")
	print("Processing image...")

	p8_standpal_image, p8_custpal_image, image_pal, standard_colours, p8_mismatches = analyseRect(pixels,start_x,start_y,end_x,end_y)

	standard_colours_override = False
	if len(p8_mismatches)>0:
		print("Warning: mismatches with pico-8 palette:")
		for col in p8_mismatches:
			print(f"0x{col:02x}")
	else:
		print("No colour mismatches with pico-8 palette (this is good).")
	if standard_colours or standard_colours_override:
		print("Image uses only standard colours.")
		print("= Standard palette image =")
		standard_palette_image = standardPaletteImage(p8_standpal_image)
		print(standard_palette_image)
		print(f"Length: {len(standard_palette_image)} characters")
	else:
		print("Image uses extended palette")

	print(f"Image has {len(image_pal)} colours.")
	if len(image_pal)>16:
		print("Warning: displaying more than 16 colours on pico-8 may be tricky.")


	# output tables for pico-8
	print("= Custom palette image =")
	print(listToString(p8_custpal_image))
	print(f"Length: {len(p8_custpal_image)} characters")

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

	print(f"{len(image_pal)} colours could be encoded in {min_bits} bits per pixel")

	##################################################################
	# Run Length Encode
	print("Raw image RLE:")
	RLE_data, max_count, pairs = runLengthEncode(p8_custpal_image,min_bits)
	# for i in range(len(counts)):
	#  print(f"Found {counts[i]} of {values[i]}")
	# print(f"Max count is {max_count}")
	print(listToString(RLE_data))
	print(f"Length: {len(RLE_data)} characters")
	print(f"Max count: {max_count} duplicates")
	print(f"Pairs: {pairs} count/values")
	print(f"Compression {len(RLE_data)/len(p8_custpal_image)*100}%")

	# verify by decoding
	decoded_data=listToString(runLengthDecode(RLE_data))
	if listToString(decoded_data)!=listToString(p8_custpal_image):
		print("Warning: problem with RLE.")
		print("org:"+listToString(p8_custpal_image))
		print("out:"+listToString(decoded_data))
	else:
		print("	(decode matches)")
	# for i in range(int(len(RLE_string)/2)):
		# 	print(f"{RLE_string[i*2]}{RLE_string[i*2+1]},", end="")

	##################################################################
	# Run Length Encode only zeros
	print("Raw image RLE, zeros only (RLE0):")
	RLE0_data, max_count, zero_blocks = runLengthEncodeOnlyZeros(p8_custpal_image,min_bits)
	print(listToString(RLE0_data))
	print(f"Length: {len(RLE0_data)} characters")
	print(f"Max count: {max_count} duplicates")
	print(f"Zero blocks: {zero_blocks}")
	print(f"Compression: {len(RLE0_data)/len(p8_custpal_image)*100}%")
	print(f"After estimate of growth due to zero blocks:{len(RLE0_data)/len(p8_custpal_image)*100}")

	# verify by decoding
	decoded_data=listToString(runLengthDecodeOnlyZeros(RLE0_data))
	if listToString(decoded_data)!=listToString(p8_custpal_image):
		print("Warning: problem with RLE0.")
		print("org:"+listToString(p8_custpal_image))
		print("out:"+listToString(decoded_data))
	else:
		print("	(decode matches)")
	# for i in range(int(len(RLE_string)/2)):
		# 	print(f"{RLE_string[i*2]}{RLE_string[i*2+1]},", end="")

	##################################################################
	# Squeeze to different encodings: 6bit and 8bit chars

	# encode to base64 as standard colours if possible
	if min_bits==4 and standard_colours or standard_colours_override:
		image_64_standard_string = squeeze4to64(standard_palette_image)
		print("= Squeezed to base64 ascii from character 35 with standard palette: =")
		print(image_64_standard_string)
		print(f"Length: {len(image_64_standard_string)} characters")

		# verify by inflating again
		infl_string=inflate64to4(image_64_standard_string,num_pixels)
		if infl_string!=standard_palette_image:
			print("Warning: problem with base64 encoding of non-RLE image.")
			print("org:"+standard_palette_image)
			print("out:"+infl_string)
		else:
			print("	(inflation matches)")

	image_64_data=[None,squeeze1to64,squeeze2to64,squeeze3to64,squeeze4to64][min_bits](p8_custpal_image)
	print("= Squeezed to base64 ascii from character 35: =")
	print(listToString(image_64_data))
	print(f"Length: {len(image_64_data)} characters")
	# verify by inflating again
	infl_data=[None,inflate64to1,inflate64to2,inflate64to3,inflate64to4,][min_bits](image_64_data,num_pixels)
	if listToString(infl_data)!=listToString(p8_custpal_image):
		print("Warning: problem with base64 encoding of non-RLE image.")
		print("org:"+listToString(p8_custpal_image))
		print("out:"+listToString(infl_data))
	else:
		print("	(inflation matches)")



	print("= RLE squeezed to base64 ascii from character 35: =")
	RLE_64_string=[None,squeeze1to64,squeeze2to64,squeeze3to64,squeeze4to64][min_bits](RLE_data)
	print(RLE_64_string)
	print(f"Length: {len(RLE_64_string)} characters")

	# verify by inflating again
	infl_data=[None,inflate64to1,inflate64to2,inflate64to3,inflate64to4,][min_bits](RLE_64_string,len(RLE_data))
	if listToString(infl_data)!=listToString(RLE_data):
		print("Warning: problem with base64 encoding.")
		print("org:"+listToString(RLE_data))
		print("out:"+listToString(infl_data))
	else:
		print("	(inflation matches)")

	decoded_data=runLengthDecode(infl_data)
	if listToString(decoded_data)!=listToString(p8_custpal_image):
		print("Warning: problem with RLE.")
		print("org:"+listToString(p8_custpal_image))
		print("out:"+listToString(decoded_data))
	else:
		print("	(decode matches)")

	# for i in range(len(counts)):
	#  print(f"Found {counts[i]} of {values[i]}")
	# print(f"Max count is {max_count}")
	print(f"Squeezing vs raw: {len(image_64_data)/num_pixels*100}%")
	print(f"RLE and squeezing size vs raw: {len(RLE_64_string)/num_pixels*100}%")

	esc_string = escape_binary_str(RLE_64_string)
	print(f"Escaped string (length {len(esc_string)}):")
	print(esc_string)

	print("###################################################")
	print("# 8 bit                                           #")
	print("###################################################")

	print("= Raw squeezed to 8bit (base 256) characters: =")
	raw_8bit_data=[None,squeeze1to8bit,squeeze2to8bit,squeeze3to8bit,squeeze4to8bit][min_bits](p8_custpal_image)
	dumpP8File(encode8bitDataAsPICO8String(raw_8bit_data),"raw8bit")

	# verify by inflating again
	infl_data=[None,inflate8bitto1,inflate8bitto2,inflate8bitto3,inflate8bitto4,][min_bits](raw_8bit_data,len(p8_custpal_image))
	if listToString(infl_data)!=listToString(p8_custpal_image):
		print("Warning: problem with 8bit encoding.")
		print("org:"+listToString(p8_custpal_image))
		print("out:"+listToString(infl_data))
	else:
		print("	(inflation matches)")



	print("= RLE squeezed to 8bit (base 256) characters: =")
	RLE_8bit_data=[None,squeeze1to8bit,squeeze2to8bit,squeeze3to8bit,squeeze4to8bit][min_bits](RLE_data)
	dumpP8File(encode8bitDataAsPICO8String(RLE_8bit_data),"RLE8bit")

	# verify by inflating again
	infl_data=[None,inflate8bitto1,inflate8bitto2,inflate8bitto3,inflate8bitto4,][min_bits](RLE_8bit_data,len(RLE_data))
	if listToString(infl_data)!=listToString(RLE_data):
		print("Warning: problem with 8bit encoding.")
		print("org:"+listToString(RLE_data))
		print("out:"+listToString(infl_data))
	else:
		print("	(inflation matches)")

	print("= RLE0 squeezed to 8bit (base 256) characters: =")
	RLE0_8bit_data=[None,squeeze1to8bit,squeeze2to8bit,squeeze3to8bit,squeeze4to8bit][min_bits](RLE0_data)
	dumpP8File(encode8bitDataAsPICO8String(RLE0_8bit_data),"RLE0_8bit")

	# verify by inflating again
	infl_data=[None,inflate8bitto1,inflate8bitto2,inflate8bitto3,inflate8bitto4,][min_bits](RLE0_8bit_data,len(RLE0_data))
	if listToString(infl_data)!=listToString(RLE0_data):
		print("Warning: problem with 8bit encoding.")
		print("org:"+listToString(RLE0_data))
		print("out:"+listToString(infl_data))
	else:
		print("	(inflation matches)")


	# window = sdl2.ext.Window("PNG2PICO-8", size=(w*16, h*8))
	# window.show()
	# ren = sdl2.ext.Renderer(window, flags=sdl2.SDL_RENDERER_ACCELERATED)
	# # makes zoomed graphics blocky (for retro effect)
	# sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"nearest")
	# # makes the graphics look and act like the desired screen size, even though they may be rendered at a different one
	# sdl2.SDL_RenderSetLogicalSize(ren.sdlrenderer, w*2, h)
	# ren.clear()
	#
	#
	# texture = sdl2.SDL_CreateTextureFromSurface(ren.sdlrenderer, surface)
	#
	# # draw source image
	# sdl2.SDL_RenderCopy(ren.sdlrenderer, texture, sdl2.SDL_Rect(0, 0, w*2, h), sdl2.SDL_Rect(0, 0, w, h))
	#
	#
	# # todo: cycle through outputs rendered so can eyeball it's def working/quality etc.
	# while True:
	# 	events = sdl2.ext.get_events()
	# 	for event in events:
	# 		if event.type == sdl2.SDL_QUIT:
	# 			exit(0)
	#
	# 	sdl2.SDL_RenderPresent(ren.sdlrenderer)
	# 	window.refresh()

def dumpFile(data,filename):
	print(f"Dumping {len(data)} characters to file {filename}")
	with open(filename,'w') as file:
		file.write(data)

def dumpP8File(data,filename):
	print(f"Dumping {len(data)} characters to file {filename}.p8")
	p8data='''pico-8 cartridge // http://www.pico-8.com
version 29
__lua__
data="'''+data+'"'
	with open(filename+'.p8','w') as file:
		file.write(p8data)


def test():
	escstr='''pico-8 cartridge // http://www.pico-8.com
version 29
__lua__
data="'''
	binstr=[]
	for i in range(0,256):
		binstr.append(i)

	escstr+=encode8bitDataAsPICO8String(binstr)

	escstr+='''"
	printh("start")
matches=0
for i=1,#data do
 v=ord(data,i)
 if v!=i-1 then
  printh(i..":"..ord(data,i))
 else
  matches+=1
 end
end
printh("data length:"..#data)
printh("matches:"..matches)
printh("end")'''

	dumpFile(escstr,"test.p8")

	# for i in range(1,257):
	# 	v = ord(escstr[i])
	# 	if (v != i): print(f"mismatch {i}:{v}")


if __name__ == "__main__":
	# outputs a pico8 program that includes a binary string with all 256 values (0-255) and checks they can be read
	# i.e. checks encode8bitDataAsPICO8String() works as expected
	# test()
	# exit(0)

	run()