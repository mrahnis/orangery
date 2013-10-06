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

	"""
	def __init__(self, filename, format):
		self.filename = filename
		self.format = format
		try:
			self.data = pnd.read_csv(filename, parse_dates=True, header=self.format['options']['header'])
			# get inverse map of the column names, then rename for internal use
			inv_col_map = {v:k for k, v in self.format['column_map'].items()}
			self.data.rename(columns=inv_col_map, inplace=True)
		except:
			print 'Error: Failed to read CSV file: ', filename
			raise
		try:
			self.chains = ot.parse(self.data, self.format['codes'])
		except:
			print 'Error: Failed to parse CSV file: ', filename
			raise

	def plot(self):
		# -----------------------------------------------
		# make the figure
		fig = plt.figure()

		ax = fig.add_subplot(111)
		ax.set_title('Survey')
		ax.set_xlabel(self.format['column_map']['x'])
		ax.set_ylabel(self.format['column_map']['y'])
		ax.set_aspect(1)
		ax.grid(True)
		
		ax.plot(self.data['x'], self.data['y'], marker='o', markersize = 4, markerfacecolor='none', linestyle='None')

		plt.show(block=False)

	def save(self):
		print 'not implemented'