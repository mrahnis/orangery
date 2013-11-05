import pandas as pnd

from shapely.geometry import asLineString

import orangery.ops.text as ot
import orangery.ops.geometry as og


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



class Section:
	"""
	A Section view of a set of points.

	Parameters
	----------
	data : DataFrame, containing the data to project
	p1 : Point, the start of a line of section
	p2 : Point, the end of a line of section
	adjustments : dict, describes adjustments to the data

	"""
	def __init__(self, data, p1, p2, reverse=False, z_adjustment=None):
		self.data = data
		self.p1, self.p2 = p1, p2

		self.projection = None
		self.line = None

		if reverse == True:
			# flip sections shot right to left
			self.data.sort(ascending=False, inplace=True)
		if z_adjustment != None:
			# adjust the section z values
			self.data['z'] = self.data['z'] + z_adjustment
		# project the data
		self.projection = og.project_points(self.data, self.p1, self.p2)
		# convert to LineString
		self.line = asLineString(zip(self.projection['d'],self.projection['z']))

	def plot(self, **kwargs):
		return self.projection.plot('d','z',**kwargs)