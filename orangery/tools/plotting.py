def polygon_plot(self, ax=None, fill_ec='black', fill_fc='none', fill_hatch='...', fill_label=None, cut_ec='black', cut_fc='none', cut_hatch='x', cut_label=None):
	"""
	Fill and label first polygon of each type separately, otherwise sequential call to fill with label property
	produces a legend label for each individual polygon.
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