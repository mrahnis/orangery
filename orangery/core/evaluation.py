from __future__ import print_function

import numpy as np
import pandas as pnd

import orangery.ops.geometry as og

class Change:
	"""
	An analysis of the change between two Section objects.

	Parameters
	----------
	section1 (Section) : the initial condition.
	section2 (Section) : the final condition.
	close_ends (bool) : True indicates dangles should be closed with a vertical line.

	"""
	def __init__(self, section1, section2, close_ends=False):
		self.section1 = section1
		self.section2 = section2

		try:
			self.intersections, self.polygons, self.cutfill = og.difference(self.section1.line, self.section2.line, close_ends=close_ends)
		except:
			print('Error calculating cut and fill')
			raise

	def segment(self, materials):
		"""
		Prompt the user to assign material from the materials dict to each polygon in the Change objects

		Parameters
		----------
		materials (dict) : a dict containing possible materials
		"""

		def __assign_material(p, low, high):
			try:
				input = raw_input
			except NameError:
				pass

			prompt = 'Enter a material no. for area {0}: '.format(p)
			err = 'Input must be an integer number between {0} and {1}.'.format(low, high)
			while True:
				try:
					m = int(input(prompt))
					if low <= m <= high:
						return m
					else:
						print(err)
				except ValueError:
					print(err)

		# materials list and array to track assignment of material to polygon
		materials = materials['materials']
		assignments = []

		# -----------------------------------------------
		# calculate cut-fill amounts
		print('\n')
		print('Areas')
		print('--------------------')
		print(self.cutfill)
		print('-------------------')
		print("Fill: ", self.cutfill[self.cutfill > 0].sum())
		print("Cut:  ", self.cutfill[self.cutfill < 0].sum())
		print("Net:  ", self.cutfill.sum())

		print('\n')
		print("No.   Material")
		print('-------------------')
		for i, material in enumerate(materials):
			print(i, "   ", material['name'])

		print('\n')
		print("Assign a material, by number, to each area")
		print('-------------------')
		
		for i, poly in enumerate(self.cutfill):
			# m = int(raw_input('Enter material no. for area {0}: '.format(i)))
			m = __assign_material(i, 0, len(materials)-1)
			assignments.append([i, m, materials[m]['name'], materials[m]['density'], materials[m]['fines']])
		assignments_df = pnd.DataFrame(assignments, columns=['polygon', 'material', 'name', 'density', 'fines'])

		self.results = assignments_df.join(self.cutfill)
		self.results['mass_fines'] = self.results['density']*self.results['fines']/100*self.results['area']
		print('\n')
		print('Results ')
		print('-------------------')
		print(self.results)
		print('-------------------')
		print('Net change in mass of fines: ', self.results['mass_fines'].sum())
		
		print('\n')

		try:
			input = raw_input
		except NameError:
			pass

		input("Press Enter to exit")		

	def save(self, filename=None):
		# save polygon cut-fill areas to csv
		self.results.to_csv('{0}.csv'.format(filename))

# add plot method
import orangery.tools.plotting as _gfx

#Change.plot = _gfx.change_plot
Change.polygon_plot = _gfx.polygon_plot
Change.annotate_plot = _gfx.annotate_plot

