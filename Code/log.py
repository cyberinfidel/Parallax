from datetime import datetime

log_data = []

# disable to remove logging
def log(msg, new_line=True, log_time=True):
	eol = '\n' if new_line else ''
	if log_time:
		entry = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f ")} {msg}{eol}'
	else:
		entry = msg+eol

	log_data.append(entry)
	print(entry, end='')

def flushToFile(file):
	with open(file,'w') as log_file:
			log_file.writelines(log_data)
