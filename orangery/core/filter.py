from shapely.geometry import Point

def pointname(df, name):
	"""
	Given a DataFrame return the named point or survey record

	Parameters
	----------
	df : DataFrame of survey data records
	name : string, name of the point to select
	"""
	print 'not implemented'

def group(df, code_table, group):
	"""
	Given a DataFrame return the survey records belonging to a given group

	Parameters
	----------
	df : DataFrame of survey data records
	code_table : DataFrame of survey date record properties
	group : string, name of the group to select

	Returns
	-------
	DataFrame
	"""
	recs = df[code_table['group'] == group]
	result = df.take(recs.index)
	return result

def endpoints(df, reverse=False):
	"""
	Given a DataFrame return the first and last survey records

	Parameters
	----------
	df : DataFrame of survey records
	reverse : boolean, False returns first then last point, True returns last then first

	Returns
	-------
	p1, p2 : shapely Points
	"""

	p1 = Point(df[:1]['x'], df[:1]['y'], df[:1]['z'])
	p2 = Point(df[-1:]['x'], df[-1:]['y'], df[-1:]['z'])
	if reverse == True:
		return p2, p1
	else:
		return p1, p2

def controls(df, code_table, format):
	"""
	Given a DataFrame return survey records with control codes

	Parameters
	----------
	df : a DataFrame of survey data records
	code_table : a DataFrame of survey date record properties
	format : a dict that describes the survey format

	Returns
	-------
	DataFrame
	"""

	recs = df[code_table['control'].isin(format['codes']['control'])]
	result = df.take(recs.index)
	return result

def benchmarks(df, code_table, format):
	"""
	Given a DataFrame return survey records with benchmark codes

	Parameters
	----------
	df : a DataFrame of survey data records
	code_table : a DataFrame of survey date record properties
	format : a dict that describes the survey format

	Returns
	-------
	DataFrame
	"""

	recs = df[code_table['marker'].isin(format['codes']['marker'])]
	result = df.take(recs.index)
	return result
