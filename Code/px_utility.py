def getDataFromFile(file):
	ldic = locals()
	with open(file) as data_file:
		code = compile(source=data_file.read(), filename='<string>', mode='exec')
		exec(code, globals(), ldic)
		for item in ['file']:
			ldic.pop(item)
		return ldic

def getDictDataFromFile(file, dict_name):
	ldic = locals()
	with open(file) as data_file:
		code = compile(source=data_file.read(), filename='<string>', mode='exec')
		exec(code, globals(), ldic)
		return ldic[dict_name]


def getListDataFromFile(file, list_name):
	ldic = locals()
	with open(file) as data_file:
		code = compile(source=data_file.read(), filename='<string>', mode='exec')
		exec(code, globals(), ldic)
		return ldic[list_name]

import collections
class OrderedDict(collections.OrderedDict):
	def index(self, item):
		return list(self.values())[item]
