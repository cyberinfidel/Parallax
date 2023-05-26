# flattens and strips comments, extra lines, indentation from p8/lua files (and prob others)

import os

# recursively flattens #include statements 
def flatten(input):
	out=''
	found_include=False
	infile=open(input, 'r')
	for line in infile:
		incl=line.find('#include')
		if incl>=0:
			new_include_file=line[incl+9:-1].strip()
			print(f"Flattening #include [{new_include_file}]")
			out+=flatten(new_include_file)
		else:
			out+=line
	return out

def run(input, output):
	os.chdir(os.path.dirname(input))
	# flatten
	try:
		flat=flatten(input)
	except Exception as e:
		print(f"Couldn't flatten {input}: {e}")
		return -1

	# strip
	try:
		outstr = ''
		for line in flat.splitlines():
			outstr += strip(line)
		lines=outstr.split('\n')
		for i,line in enumerate(lines):
			if line.find('printh')>=0:
				print(f"Found printh outside comment (stripped line {i}): {line}")
	except Exception as e:
		print(f"Couldn't strip {input}: {e}")
		return -1

	# write out the flattened file
	try:
		with open(output, 'w') as outfile:
			outfile.write(outstr)
	except Exception as e:
		print(f"Couldn't write {output}: {e}")
		return -1

	return 0

# basic stripper of white space and comments (-- only)
def strip(line):
	line=line.strip()
	if len(line)==0:
		return ''
	if line[0:2]=='--':
		return ''

	if line.find('_dbi=')<0:
		comm=line.find('--')
		if comm>=0:
			line=line[0:comm]

	return line.strip()+"\n"

# todo: take arguments
# I've written these things so many times you'd think I could do it in my sleep
# but no, I have to look it up from scratch every time and right now I can't be arsed
if __name__ == "__main__":
	exit(run(input="/Users/flash/GitHub/pico-8/carts/oust/oust.p8",output="/Users/flash/GitHub/pico-8/carts/oust/oust_stripped.p8"))

