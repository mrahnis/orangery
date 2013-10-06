import pandas as pnd

def parse(points, format):

	"""
	Parses the codes in a DataFrame to extract information about points and chains of points.
	Returns a DataFrame with the index of the start and end of each chain, as well as descriptive information about the chain of points.

	Parameters
	----------
	points : DataFrame, contains the survey data
	format : dict, contains format configuration information that describes the codes used, including control codes

	Returns
	-------
	DataFrame : describes the points and chains of points; column names match keys in the codes sub-dict,
		the added group column currently comes from the 'comment' field at each start command 
	"""

	# parse the codes into columns for marker, control, view and breakline
	results = []
	build = False
	group = None
	for pt in points.index:
		codes = str(points.loc[pt, 'code']).split(' ')

		# validate start and end order for chains
		if format['control'][0] in codes:
			if build == False:
				build = True
				group = str(points.loc[pt, 'comment'])
			else:
				print 'Error: Out of order line start command.'
				break

		# assign codes to the correct column
		record = []
		for k, v in format.items():
			c = None
			for code in codes:
				if code in v:
					if c != None:
						print 'Warning: More than one %s code in point %s.' % (k, str(points.loc[pt, 'point']))
					c = code
			kv = (k, c)
			record.append(kv)
		record.append(('group', group))
		results.append(dict(record))

		# validate start and end order for chains, clean up after line end command
		if format['control'][1] in codes:
			if build == True:
				build = False
				group = None
			else:
				print 'Error: Out of order line end command.'
				break

	df = pnd.DataFrame(results)
	return df