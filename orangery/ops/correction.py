import logging

def get_offsets(df, coords):
	"""
	Calulate the x,y,z offsets between a record in a dataframe and an array of x,y,z coordinates.
	"""
	if len(df) == 1:
		offsets = [coords[0] - df.iloc[0]['x'], coords[1] - df.iloc[0]['y'], coords[2] - df.iloc[0]['z']]
		return offsets
	else:
		logging.error('df can have only one record. df has {0} records.'.format(len(df)))

def translate(df, offsets):
	"""
	Translate the x,y,z coordinates for records in a dataframe by an array of offsets.
	"""
	df['x'] = df['x'] + offsets[0]
	df['y'] = df['y'] + offsets[1]
	df['z'] = df['z'] + offsets[2]
	return df