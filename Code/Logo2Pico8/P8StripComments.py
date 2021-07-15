

def run(input, output):
	outstr = ''
	with open(input, 'r') as infile:
		for line in infile:
			outstr += strip(line)
	lines=outstr.split('\n')
	for i,line in enumerate(lines):
		if line.find('printh')>=0:
			print(f"found printh outside comment (stripped line {i}): {line}")

	with open(output, 'w') as outfile:
		outfile.write(outstr)
	return 0


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

	return line+"\n"


if __name__ == "__main__":
	exit(run("space.p8","spacestripped.p8"))

