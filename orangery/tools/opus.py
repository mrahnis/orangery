import xml.etree.ElementTree as xml
from orangery.tools.units import US_FOOT_IN_METERS

def _convert(root, val_path, unit_path, out_unit):
	"""
	Convert a value value from the OPUS file to a new unit

	Parameters
	----------
	root (XML root) : root element.
	val_path (str) : path to the value to be converted.
	unit_path  (str) : path to the unit designation.
	out_unit (str) : desired output unit.

	Returns
	-------
	result (float) : converted value.
	"""
	val = float(root.find(val_path).text)
	opus_unit = root.find(unit_path).get('UNIT')

	if opus_unit == 'm' and out_unit =='US_ft':
		result = val/US_FOOT_IN_METERS
	elif opus_unit == 'US_ft' and out_unit == 'm':
		result = val*US_FOOT_IN_METERS
	else:
		result = val
	return result

def get_plane_coords(filename, unit='m', spec_type='UTM'):	
	"""
	Extract the coordinate from an OPUS XML file PLANE_COORD_SPEC elements, and return it in the desired units and coordinate spec type.

	Parameters
	----------
	filename (str) : the path to the OPUS XML file.
	unit (str) : distance units of the returned coordinate, valid values are 'm' or 'US_ft'.
	spec_type (str) : coordinate projection of the returned coordinate, valid values are 'UTM' or 'SPC'.

	Returns
	-------
	coords (float array) : array of x,y,z coordinates.
	"""
	tree = xml.parse(filename)
	rootElement = tree.getroot()

	for pcs in rootElement.findall('PLANE_COORD_INFO/PLANE_COORD_SPEC'):
		#print pcs.tag, pcs.attrib
		if pcs.get('TYPE') == spec_type:
			e = _convert(pcs, 'EASTING', 'EASTING', unit)
			n = _convert(pcs, 'NORTHING', 'NORTHING', unit)
		else:
			continue
	h = _convert(rootElement, 'ORTHO_HGT', 'ORTHO_HGT', unit)

	coords = [e, n, h]
	return coords

def get_data_quality(filename, unit='m'):
	"""
	Extract the information from an OPUS XML file DATA_QUALITY element, and return it in the desired units.

	Parameters
	----------
	filename (str) : the path to the OPUS XML file.
	unit (str) : distance units of the returned coordinate, valid values are 'm' or 'US_ft'.

	Returns
	-------
	accuracy (float array) : array of x,y,z coordinate accuracies.
	rms (float) : the RMS value
	used (int array) : array of observations [total, used]
	fixed (int array) : array of observation ambiguities [total, fixed]
	"""
	tree = xml.parse(filename)
	rootElement = tree.getroot()
	dq = rootElement.find('DATA_QUALITY')

	accuracy = [_convert(dq, 'ACCURACY/LAT', 'ACCURACY', unit), _convert(dq, 'ACCURACY/LONG', 'ACCURACY', unit), _convert(dq, 'ACCURACY/EL_HEIGHT', 'ACCURACY', unit)]
	rms = _convert(dq, 'RMS', 'RMS', unit)

	used = [int(dq.find('PERCENT_OBS_USED').get('TOTAL')), int(dq.find('PERCENT_OBS_USED').get('USED'))]
	fixed = [int(dq.find('PERCENT_AMB_FIXED').get('TOTAL')), int(dq.find('PERCENT_AMB_FIXED').get('FIXED'))]

	return accuracy, rms, used, fixed

def get_solution_info(filename):
	"""
	Print information about the solution.
	"""

	tree = xml.parse(filename)
	rootElement = tree.getroot()


	print '-----------------'
	print 'SOLUTION_INFO'
	print '-----------------'
	print rootElement.get('SID')
	print rootElement.find('SOLUTION_TIME').text
	print rootElement.find('OBSERVATION_TIME').get('START')
	print rootElement.find('OBSERVATION_TIME').get('END')
	print rootElement.find('CONTRIBUTOR/EMAIL').text
	#print rootElement.find('CONTRIBUTOR/AGENCY').text
	print rootElement.find('DATA_SOURCES/RINEX_FILE').text
	print rootElement.find('DATA_SOURCES/EPHEMERIS_FILE').get('TYPE')
	print rootElement.find('DATA_SOURCES/ANTENNA/NAME').text
	print rootElement.find('DATA_SOURCES/ANTENNA/ARP_HEIGHT').text
	print rootElement.find('DATA_SOURCES/ANTENNA/ARP_HEIGHT').get('UNIT')

def get_mark_info(filename):
	"""
	Print information about the mark.
	"""
	
	tree = xml.parse(filename)
	rootElement = tree.getroot()

	print '-----------------'
	print 'MARK_INFO'
	print '-----------------'
	print rootElement.find('MARK_METADATA/PID').text
	print rootElement.find('MARK_METADATA/DESIGNATION').text
	print rootElement.find('MARK_METADATA/STAMPING').text
	print rootElement.find('MARK_METADATA/MONUMENT_TYPE').text
	print rootElement.find('MARK_METADATA/MONUMENT_DESC').text
	print rootElement.find('MARK_METADATA/STABILITY').text
	print rootElement.find('MARK_METADATA/DESCRIPTION').text
