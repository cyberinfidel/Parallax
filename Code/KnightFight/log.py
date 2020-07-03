# disable to remove logging
def log(msg, new_line=True):
	if new_line:
		print(msg)
	else:
		print(msg, end='')
