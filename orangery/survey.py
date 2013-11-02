import pandas as pnd

import matplotlib.pyplot as plt

import orangery.ops.text as ot

class Survey:
	"""
	A Survey dataset.

		Parameters
		----------
		filename : string, the path to the file to read
		format : dict, describes the survey data
		kwargs: dict, keyword arguments passed to pandas.read_csv

	"""
	def __init__(self, filename, format, **kwargs):
		self.filename = filename
		self.format = format
		try:
			self.data = pnd.read_csv(filename, **kwargs)
			# get inverse map of the column names, then rename for internal use
			inv_col_map = {v:k for k, v in self.format['column_map'].items()}
			self.data.rename(columns=inv_col_map, inplace=True)
		except:
			print 'Error: Failed to read CSV file: ', filename
			raise
		try:
			self.code_table = ot.parse(self.data, self.format['codes'])
		except:
			print 'Error: Failed to parse CSV file: ', filename
			raise

	def plot(self, **kwargs):
		"""
		Plot the x, y values of the data. Keyword arguments are passed to Pandas.
		"""
		return self.data.plot('x','y', **kwargs)