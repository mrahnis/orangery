import numpy as np
import pandas as pnd

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

import orangery.ops.geometry as og

# http://pypi.python.org/pypi/descartes/1.0
from orangery.util.descartes import PolygonPatch

def _assign_material(p, low, high):
	prompt = 'Enter a material no. for area {0}: '.format(p)
	err = 'Input must be an integer number between %d and %d.' % (low, high)
	while True:
		try:
			m = int(raw_input(prompt))
			if low <= m <= high:
				return m
			else:
				print err
		except ValueError:
			print err

class Change:
	"""
	An analysis of the change between two Section objects.

	Parameters
	----------
	section1 : Section, the initial condition
	section2 : Section, the final condition
	analysis : dict, describes the analysis to perform

	"""
	def __init__(self, section1, section2, analysis):
		self.section1 = section1
		self.section2 = section2
		self.analysis = analysis

		try:
			self.intersections, self.polygons, self.cutfill = og.difference(self.section1.line, self.section2.line, self.analysis['plot']['close'])
		except:
			print 'Error calculating cut and fill'
			raise

	def segment(self):
		# -----------------------------------------------
		# calculate cut-fill amounts
		print
		print "Areas"
		print '--------------------'
		print self.cutfill
		print '-------------------'
		print "Fill: ", self.cutfill[self.cutfill > 0].sum()
		print "Cut:  ", self.cutfill[self.cutfill < 0].sum()
		print "Net:  ", self.cutfill.sum()

		materials = self.analysis['materials']
		assignments = []

		print
		print "No.   Material"
		print '-------------------'
		for i, material in enumerate(materials):
			print i, "   ", material['name']

		# SHOULD VALIDATE INPUT HERE
		print
		print "Assign a material, by number, to each area"
		print '-------------------'
		
		for i, poly in enumerate(self.cutfill):
			# m = int(raw_input('Enter material no. for area {0}: '.format(i)))
			m = _assign_material(i, 0, len(materials)-1)
			assignments.append([i, m, materials[m]['name'], materials[m]['density'], materials[m]['fines']])
		assignments_df = pnd.DataFrame(assignments, columns=['polygon', 'material', 'name', 'density', 'fines'])

		self.results = assignments_df.join(self.cutfill)
		self.results['mass_fines'] = self.results['density']*self.results['fines']/100*self.results['area']
		print
		print 'Results '
		print '-------------------'
		print self.results
		print '-------------------'
		print 'Net change in mass of fines: ', self.results['mass_fines'].sum()

		#self.save()
		
		print
		raw_input("Press Enter to exit")	
	
	def plot(self):
		# -----------------------------------------------
		# make the figure
		fig = plt.figure(figsize=(9.5,3))

		ax = fig.add_subplot(111)
		ax.set_title('Cross-section {0}'.format(self.analysis['plot']['name']))
		ax.set_xlabel('Distance (ft)')
		ax.set_ylabel('Elevation (ft)')
		ax.grid(True)

		ax.plot(self.section1.projection['d'], self.section1.projection['z'], marker='o', markersize = 4, markerfacecolor='none', linestyle='-', color='black')
		ax.plot(self.section2.projection['d'], self.section2.projection['z'], marker='o', markersize = 4, markerfacecolor='black', linestyle='-', color='black')
		#dates = (self.section1.xs_info['start'].strftime("%Y-%b-%d"), self.section2.xs_info['start'].strftime("%Y-%b-%d"))
		#ax.legend(dates, 'lower right', shadow=False)

		# make and fill patches
		if self.analysis['plot']['fill'] == True:
			for i, poly in enumerate(self.polygons):
				patch = PolygonPatch(poly, fc='None', ec='None', alpha=0.5)
				if self.cutfill[i] > 0:
					patch.set_facecolor('none')
					patch.set_edgecolor('black')
					patch.set_hatch('...')
				elif self.cutfill[i] < 0:
					patch.set_facecolor('none')
					patch.set_edgecolor('black')
					patch.set_hatch('x')
				ax.add_patch(patch)

		# add annotation
		if self.analysis['plot']['annotate'] ==True:
			ylim = ax.get_ylim()
			for i, intersection in enumerate(self.intersections):
				verts = [(intersection.x, ylim[0]), (intersection.x, ylim[0]+0.05*(ylim[1]-ylim[0]))]
				codes = [ Path.MOVETO, Path.LINETO ]
				path = Path(verts, codes)
				patch = patches.PathPatch(path, color='red', alpha=0.7)
				ax.add_patch(patch)
				if i < len(self.intersections)-1:
					ax.text((intersection.x + self.intersections[i+1].x)/2, ylim[0]+0.02*(ylim[1]-ylim[0]), i, color='red', fontsize=8, ha='center')

		plt.show(block=False)

	def save(self):
		# save polygon cut-fill areas to csv; save figure to png file
		self.results.to_csv('{0}.csv'.format(self.analysis['plot']['name']))
		# fig.savefig('{0}.png'.format(self.analysis['plot']['xsname']), figsize=(9,4.5), dpi=240, bbox_inches='tight')