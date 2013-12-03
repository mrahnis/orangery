def get_offsets(df, coords):
	"""
	Calulate the x,y,z offsets between a record in a dataframe and an array of x,y,z coordinates.
	"""
	if len(df) == 1:
		offsets = [coords[0] - df.iloc[0]['X'], coords[1] - df.iloc[0]['Y'], coords[2] - df.iloc[0]['Z']]
		return offsets
	else:
		print 'df can have only one record. df has ', len(df), ' records.'

def translate(df, offsets):
	"""
	Translate the x,y,z coordinates for records in a dataframe by an array of offsets.
	"""
	df['X'] = df['X'] + offsets[0]
	df['Y'] = df['Y'] + offsets[1]
	df['Z'] = df['Z'] + offsets[2]
	return df