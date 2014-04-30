from __future__ import print_function

import collections

import pandas as pnd

from shapely.geometry import asLineString

import orangery.ops.text as ot
import orangery.ops.geometry as og
import orangery.ops.correction as oc


class Survey:
	"""
	A Survey dataset.

	Parameters
	----------
	filename (str) : the path to the file to read.
	format (str) : a string of characters that describes the survey data. Accepts:
		p    - point
		x, e - x coord, easting
		y, n - y coord, northing
		z, h - z coord
		d, s - distance, station
		o    - offset
		t    - timestamp
		c    - code
		r    - remark
		q    - quality
		f    - foresight
		a    - attribute
		The string may contain the characters in any order, without duplicates, except for 'a' which may occur multiple times. The string must contain x/e,y/n,z/h or d/s,z/h.
		Examples: 'pyxzctnff', 'pnezfrf'
	codebook (dict) : a dict that describes the codes used in the survey.
	header (int) : the row number of the header. As in pandas it is 0 by default. If there is no header row specify 'None'.
	kwargs (dict) : keyword arguments passed to pandas.read_csv.

	"""
	def __init__(self, filename, columns, codebook, header=0, **kwargs):
		self.filename = filename
		self.codebook = codebook

		try:
			self.data = pnd.read_csv(filename, header=header, **kwargs)

			known_columns = set(('p','x','y','z','n','e','s','o','z','t','d','c','r','q','f','a'))
			columns = list(columns.lower())

			if set(columns).issubset(known_columns) == False:
				unrecognized = set(columns).difference(known_columns)
				print('Warning: Unrecognized column entry ', unrecognized)

			columns = [c.replace('a', 'a'+str(i)) for i,c in enumerate(columns)]

			if len(set(columns)) < len(columns):
				duplicates = [i for i, c in collections.Counter(columns).items() if c > 1]
				print('Warning: Duplicate columns ', duplicates)

			columns = [c.replace('n', 'y') for c in columns]
			columns = [c.replace('e', 'x') for c in columns]
			columns = [c.replace('h', 'z') for c in columns]
			columns = [c.replace('s', 'd') for c in columns]

			# get inverse map of the dataframe column names, then rename columns for internal use
			self.format = collections.OrderedDict(zip(columns,self.data.columns))
			inv_col_map = {v:k for k, v in self.format.items()}
			self.data.rename(columns=inv_col_map, inplace=True)
		except:
			print('Error: Failed to read CSV file: ', filename)
			raise
		try:
			self.code_table = ot.parse(self.data, self.codebook)
		except:
			print('Error: Failed to parse CSV file: ', filename)
			raise

	def translate(self, deltas):
		self.data = oc.translate(self.data, deltas)

	def plot(self, **kwargs):
		"""
		Plot the x, y values of the data.

		Parameters
		----------
			kwargs (dict) : Keyword arguments to be passed to Pandas and matplotlib.

		Returns
		-------
		ax (Axis) : a matplotlib Axis.

		"""
		if {'x','y','z'}.issubset(self.data.columns):
			ax = self.data.plot('x','y', **kwargs)
		else:
			print('Warning: x,y columns not available in this data')
			ax = None
		return ax

class Section:
	"""
	A Section view of a set of x,y,z coordinates.

	Parameters
	----------
	data (pandas.DataFrame) : contains the data to project.
	p1 (shapely.Point) : the start of a line of section.
	p2 (shapely.Point) : the end of a line of section.
	reverse (bool) : reverse the order of points in the section.
	z_adjustment (float) : adjust the elevation of the data.

	"""
	def __init__(self, data, p1, p2, reverse=False, z_adjustment=None):
		self.data = data
		self.p1, self.p2 = p1, p2

		self.projection = None
		self.line = None

		if reverse == True:
			self.data.sort(ascending=False, inplace=True) # flip sections shot right to left
		if z_adjustment != None:
			self.data['z'] = self.data['z'] + z_adjustment

		self.projection = og.project_points(self.data, self.p1, self.p2)
		self.line = asLineString(list(zip(self.projection['d'],self.projection['z'])))

	def plot(self, view='section', **kwargs):
		"""
		Plot the d, z values of the projected data.

		Parameters
		----------
		view (str) : Valid entries are 'section' and 'map'. Default is 'section' view.
		kwargs (dict) : Keyword arguments to be passed to Pandas and matplotlib.

		Returns
		-------
		ax (Axis) : a matplotlib Axis.

		"""
		if view=='section':
			ax = self.projection.plot('d','z',**kwargs)
		elif view=='map':
			ax = self.data.plot('x','y',**kwargs)
		else:
			print('Warning:', view, 'is not a valid view option.')
			ax=None
		return ax

class LevelSection:
	"""
	A Section view of a set of d,z coordinates. Z values may be calculated based on backsight, foresight and datum elevation.
	"""
	def __init__(self, data, p1, p2, backsight=0.0, datum=0.0, reverse=False, z_adjustment=None):
		self.data = data
		self.datum = datum
		self.backsight = backsight

		self.location = None # this will assign x,y values to the data based on p1, p2 coordinates
		self.line = None

		if {'f'}.isin(self.data.columns):
			print('calculate elevations')

		if reverse == True:
			self.data.sort(ascending=False, inplace=True) # flip sections shot right to left
		if z_adjustment != None:
			self.data['z'] = self.data['z'] + z_adjustment

		if p1 != None and p2 != None:
			# calculate locations, but instead of dou, calculate xyz
			# xyzdou
			self.location = og.locate_points(self.data, self.p1, self.p2)
			
		self.line = asLineString(list(zip(self.data['d'],self.data['z'])))

	def plot(self, view='section', **kwargs):
		"""
		Plot the d, z values of the data.

		Parameters
		----------
		view (str) : Valid entries are 'section' and 'map'. Default is 'section' view.
		kwargs (dict) : Keyword arguments to be passed to Pandas and matplotlib.

		Returns
		-------
		ax (Axis) : a matplotlib Axis.

		"""
		if view=='section':
			ax = self.data.plot('d','z',**kwargs)
		elif view=='map':
			ax = self.location.plot('x','y',**kwargs)
		else:
			print('Warning:', view, 'is not a valid view option.')
			ax=None
		return ax
