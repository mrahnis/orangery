from shapely.geometry import Point

def pointname(df, name):
	"""
	Given a DataFrame return the named point or survey record.

	Parameters
	----------
	df (DataFrame) : survey data records.
	name (str) : name of the point to select.

	Returns
	-------
	result (DataFrame) : records where point field (equivalent to the 'Point name' on Trimble data collectors) is equivalent to the name argument.
	"""
	recs = df[df['p'] == name]
	result = df.take(recs.index)
	return result

def group(df, code_table, group):
	"""
	Given a DataFrame return a copy of the survey records belonging to a given group

	Parameters
	----------
	df (DataFrame) : survey data records.
	code_table (DataFrame) : survey data record properties extracted by parse function.
	group (str) : name of the group to select.

	Returns
	-------
	result (DataFrame) : records matching the given group name.
	"""
	recs = df.loc[code_table['group'] == group]
	result = df.take(recs.index).copy()
	return result

def endpoints(df, reverse=False):
	"""
	Given a DataFrame return the first and last survey records.

	Parameters
	----------
	df (pandas.DataFrame) : survey data records.
	reverse (bool) : False returns first then last point, True returns last then first.

	Returns
	-------
	p1, p2 (Point) : first and last records in a DataFrame as Points.
	"""

	p1 = Point(df[:1]['x'], df[:1]['y'], df[:1]['z'])
	p2 = Point(df[-1:]['x'], df[-1:]['y'], df[-1:]['z'])
	if reverse == True:
		return p2, p1
	else:
		return p1, p2

def controls(df, code_table, codebook):
	"""
	Given a DataFrame return survey records that have control codes.

	Parameters
	----------
	df (pandas.DataFrame) : survey data records.
	code_table (pandas.DataFrame) : survey data record properties extracted by parse function.
	codebook (dict) : a dict that describes the codes used in the survey.

	Returns
	-------
	result (DataFrame) : records having control codes.
	"""

	recs = df[code_table['control'].isin(codebook['codes']['control'])]
	result = df.take(recs.index)
	return result

def benchmarks(df, code_table, codebook):
	"""
	Given a DataFrame return survey records with benchmark codes.

	Parameters
	----------
	df (pandas.DataFrame) : survey data records.
	code_table (pandas.DataFrame) : survey data record properties extracted by parse function.
	codebook (dict) : a dict that describes the codes used in the survey.

	Returns
	-------
	result (DataFrame) : records having benchmark codes.
	"""

	recs = df[code_table['marker'].isin(codebook['codes']['marker'])]
	result = df.take(recs.index)
	return result
