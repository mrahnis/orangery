import numpy as np
from shapely.geometry import asLineString

import orangery.ops.geometry as og


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