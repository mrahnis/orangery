from __future__ import print_function

import logging
import pandas as pnd

def parse(points, codebook):

	"""
	Parses the codes in a DataFrame to extract information about points and chains of points.

	Parameters
	----------
	points (DataFrame) : contains the survey data.
	codebook (dict) : a dict that describes the codes used in the survey.

	Returns
	-------
	df (DataFrame) : Describes the points and chains of points. Column names match keys in the codes sub-dict,
		the added group column currently comes from the 'comment' field at each start command.
	"""

	# parse the codes into columns for marker, control, view and breakline
	results = []
	build = False
	group = None
	for pt in points.index:
		codes = str(points.loc[pt, 'c']).split(' ')

		# validate start and end order for chains
		if codebook['codes']['control'][0] in codes:
			if build == False:
				build = True
				group = str(points.loc[pt, codebook['group']['column']])
			else:
				logging.error('Out of order line start command')
				break

		# assign codes to the correct column
		record = []
		for k, v in codebook['codes'].items():
			c = None
			for code in codes:
				if code in v:
					if c != None:
						logging.warning('More than one {0} code in point {1}'.format(k, str(points.loc[pt, 'p'])))
					c = code
			kv = (k, c)
			record.append(kv)
		record.append(('group', group))
		results.append(dict(record))

		# validate start and end order for chains, clean up after line end command
		if codebook['codes']['control'][1] in codes:
			if build == True:
				build = False
				group = None
			else:
				logging.error('Out of order line end command')
				break

	df = pnd.DataFrame(results)
	return df