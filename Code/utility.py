

def getDictDataFromFile(file, dict_name):
	data = {}
	ldic = locals()
	with open(file) as data_file:
		code = compile(source=data_file.read(), filename='<string>', mode='exec')
		exec(code, globals(), ldic)
		return ldic[dict_name]


def getListDataFromFile(file, list_name):
	data = []
	ldic = locals()
	with open(file) as data_file:
		code = compile(source=data_file.read(), filename='<string>', mode='exec')
		exec(code, globals(), ldic)
		return ldic[list_name]
