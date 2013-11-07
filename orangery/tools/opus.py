import xml.etree.ElementTree as xml
from orangery.tools.units import US_FOOT_IN_METERS

def get_plane_coords(filename, unit='m', spec_type='UTM'):	
	"""
	Extract the coordinate from an OPUS XML file PLANE_COORD_SPEC elements, and return it in the desired units and coordinate spec type.

	Parameters
	----------
	filename (str) : the path to the OPUS XML file.
	unit (str) : distance units of the returned coordinate, valid values are 'm' or 'US_ft'.
	spec_type (str) : coordinate projection of the returned coordinate, valid values are 'UTM' or 'SPC'

	Returns
	-------
	coords (float array) : array of x,y,z coordinates.
	"""
	tree = xml.parse(filename)
	rootElement = tree.getroot()

	h = rootElement.find('ORTHO_HGT')
	ortho_hgt = float(h.text)
	h_unit = h.get('UNIT')

	for pcs in rootElement.findall('PLANE_COORD_INFO/PLANE_COORD_SPEC'):
		#print pcs.tag, pcs.attrib

		if pcs.get('TYPE') == spec_type:
			e = pcs.find('EASTING')
			n = pcs.find('NORTHING')

			easting = float(e.text)
			northing = float(n.text)

			e_unit = e.get('UNIT')
			n_unit = n.get('UNIT')

			opus_coords = [easting, northing, ortho_hgt]
			units = [e_unit, n_unit, h_unit]
		else:
			continue

	coords = []
	for i, coord in enumerate(opus_coords):
		if units[i] == 'm' and unit == 'US_ft':
			coords.append(coord/US_FOOT_IN_METERS)
		elif units[i] == 'US_ft' and unit == 'm':
			coords.append(coord*US_FOOT_IN_METERS)
		else:
			coords.append(coord)

	return coords
