import json

class Configuration:
	"""
	Loads a JSON file to produce a dict.

	Parameters
	----------
	filename : string, the path to the JSON file to load

	"""
	def __init__(self, filename):
		try:
			self.data = json.load(open(filename, 'r'))
		except:
			print 'Decoding JSON Failed. Check the configuration file: ', filename
			raise