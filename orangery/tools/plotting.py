def polygon_plot(self, ax=None, fill_ec='black', fill_fc='none', fill_hatch='...', fill_label=None, cut_ec='black', cut_fc='none', cut_hatch='x', cut_label=None):
	"""Adds two groups of polygon patches to a matplotlib Axis.

	Fill and label first polygon of each type separately, otherwise make sequential call to fill.

	Parameters:
		ax (Axis) : matplotlib Axis to which to add polygon patches.
		fill_ec (str) :  fill polygon edge color.
		fill_fc (str) :  fill polygon face color.
		fill_hatch (str) : fill polygon hatch pattern.
		fill_label (str) : fill polygon label.
		cut_ec (str) : cut polygon edge color.
		cut_fc (str) : cut polygon face color.
		cut_hatch (str) : cut polygon hatch pattern.
		cut_label (str) :  cut polygon label.

	Returns:
		ax (Axis) : patched matplotlib Axis.

	"""
	cuts = []
	hascut = False
	fills = []
	hasfill = False
	for i, poly in enumerate(self.polygons):
		x,y = poly.exterior.xy
		if self.cutfill[i] > 0:
			if hasfill == True:
				fills.append(x)
				fills.append(y)
			else:
				ax.fill(x, y, ec=fill_ec, fc=fill_fc, hatch=fill_hatch, label=fill_label)
				hasfill=True
		elif self.cutfill[i] < 0:
			if hascut == True:
				cuts.append(x)
				cuts.append(y)
			else:
				ax.fill(x, y, ec=cut_ec, fc=cut_fc, hatch=cut_hatch, label=cut_label)
				hascut=True
	ax.fill(*cuts, ec=cut_ec, fc=cut_fc, hatch=cut_hatch)
	ax.fill(*fills, ec=fill_ec, fc=fill_fc, hatch=fill_hatch)

	return ax

def annotate_plot(self, ax=None):
	"""Add annotation to a plot to identify individual polygons.

	Parameters:
		ax (Axis) : matplotlib Axis to which to add annotation.

	Returns:
		ax (Axis) : patched matplotlib Axis.

	"""
	import matplotlib.patches as patches
	from matplotlib.path import Path

	ylim = ax.get_ylim()
	for i, intersection in enumerate(self.intersections):
		verts = [(intersection.x, ylim[0]), (intersection.x, ylim[0]+0.05*(ylim[1]-ylim[0]))]
		codes = [ Path.MOVETO, Path.LINETO ]
		path = Path(verts, codes)
		patch = patches.PathPatch(path, color='red', alpha=0.7)
		ax.add_patch(patch)
		if i < len(self.intersections)-1:
			ax.text((intersection.x + self.intersections[i+1].x)/2, ylim[0]+0.02*(ylim[1]-ylim[0]), i, color='red', fontsize=8, ha='center')

	return ax

def get_scale_factor(fig, ax, scale, axis='x'):
	"""Get the scale factor needed to obtain a desired scale in x-axis units per inch.

	Parameters:
		fig (Figure) : the figure to scale.
		ax (Axis) : the axis to scale.
		scale (int or float) : the desired output scale.

	Returns:
		scale_factor (float) : the scale factor to apply to the figure size.

	"""	
	bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
	if axis == 'x':
		xlim = ax.get_xlim()
		initial_scale = abs(xlim[1] - xlim[0]) / bbox.width
	elif axis == 'y':
		ylim = ax.get_ylim()
		initial_scale = abs(ylim[1] - ylim[0]) / bbox.height		
	scale_factor = initial_scale/scale

	return scale_factor
