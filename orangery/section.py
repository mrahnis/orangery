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
	def __init__(self, data, p1, p2, adjustments):
		self.data = data
		self.p1, self.p2 = p1, p2
		self.adjustments = adjustments

		self.projection = None
		self.line = None

		#self.excludes = self.config['excludes']
		#self.decorations = self.config['decorations']

		if self.adjustments['reverse'] == True:
			self.reverse()

		self.adjust()
		self.project()
		self.convert()

	def plot():
		print 'not implemented'
	def save():
		print 'not implemented'

	def reverse(self):
		# flip sections shot right to left
		self.data.sort(ascending=False, inplace=True)

	def adjust(self):
		# adjust the section z values
		self.data['z'] = self.data['z'] + self.adjustments['z_adjust']

	def project(self):
		# project the data
		self.projection = og.project_points(self.data,
			self.p1, self.p2)

	def convert(self):
		# convert to LineString
		self.line = asLineString(
			self.projection[['d','z']].view(np.float).reshape((self.projection.size, 2)))
