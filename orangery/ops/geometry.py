import pandas as pnd

from numpy import array
from numpy import asarray
from numpy import float

from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import MultiLineString
from shapely.ops import polygonize
from shapely.ops import linemerge

def project2(p1, p2, p3):
	"""
	Projects a Point, p3 onto a line intersecting Points p1 and p2
	Adapted from tutorial by Paul Bourke: http://paulbourke.net/geometry/pointline/
	This projection allows for points at negative distances.

	Parameters
	----------
	p1 : Point, point at zero distance on line between p1 and p2
	p2 : Point, endpoint on line
	p3 : Point, the point to project

	Returns
	-------
	dict : a dict including the projected point, distance along line, offset from line, and fractional distance along line

	"""
	x_delta = p2.x - p1.x
	y_delta = p2.y - p1.y
	
	if x_delta == 0 and y_delta == 0:
		print "p1 and p2 cannot be the same point"
		return
	
	u = ((p3.x - p1.x) * x_delta + (p3.y - p1.y) * y_delta) / (x_delta * x_delta + y_delta * y_delta)
	pp = Point(p1.x + u * x_delta, p1.y + u * y_delta, p3.z)

	# calculate distance along the line from p1
	if u < 0:
		d = -pp.distance(p1)
	else:
		d = pp.distance(p1)
		
	# calculate the offset distance of p3 from the line
	if (p1.y - p2.y) * (p3.x -  p2.x) - (p1.x - p2.x) * (p3.y - p2.y) < 0:
		offset = -pp.distance(p3) # the point is left of the line
	else:
		offset = pp.distance(p3) # the point is right of the line
	
	return {'point':pp, 'd':d, 'offset':offset, 'u':u}

def project(p1, p2, p3):
	"""
	Projects a Point, p3 onto a line between Points p1 and p2
	Relies on shapely methods.
	This projection sets distance to zero for all negative distances.

	Parameters
	----------
	p1 : Point, point at zero distance on line between p1 and p2
	p2 : Point, endpoint of line
	p3 : Point, the point to project

	Returns
	-------
	dict : a including the projected point, disctance along line, offset from line, and fractional distance along line

	"""
	line = LineString([(p1.x, p1.y),(p2.x, p2.y)])
	u = line.project(p3, normalized=True)
	d = line.project(p3, normalized=False)
	pp2D = line.interpolate(d)
	pp = Point([pp2D.x, pp2D.y, p3.z])

	# calculate the offset distance of p3 from the line
	if (p1.y - p2.y) * (p3.x - p2.x) - (p1.x - p2.x) * (p3.y - p2.y) < 0:
		offset = -pp.distance(p3) # the point is left of the line
	else:
		offset = pp.distance(p3) # the point is right of the line

	return {'point':pp, 'd':d, 'offset':offset, 'u':u}	

def project_points(points, p1, p2):
	"""
	Projects multiple points onto a line through Points p1, p2.

	Parameters
	----------
	points : array of Points
	p1 : Point, point at zero distance on line between p1 and p2
	p2 : Point, endpoint of line

	Returns
	-------
	array : an array representing the projected points, including the original index, x, y, z, distance along line, offset from line, and fractional distance along line

	"""
	ppoints = []
	for i in points.index:
		p3 = Point(points.loc[i, 'x'], points.loc[i, 'y'], points.loc[i, 'z'])
		pp = project2(p1, p2, p3)
		ppoints.append((pp['point'].x, pp['point'].y, pp['point'].z, pp['d'], pp['offset'], pp['u']))	

	return pnd.DataFrame(ppoints, columns=['x','y','z','d','offset','u'])

def cut_by_distance(line, distance):
	"""
	cut function is from shapely recipes http://sgillies.net/blog/1040/shapely-recipes/

	Parameters
	----------
	line : LineString, line to cut
	distance : float, distance from beginning of line to cutting point

	Returns
	-------
	array of LineString

	"""
	if distance <= 0.0 or distance >= line.length:
		return [LineString(line)]
	coords = list(line.coords)
	for i, p in enumerate(coords):
		pd = line.project(Point(p))
		if pd == distance:
			return [
				LineString(coords[:i+1]),
				LineString(coords[i:])]
		if pd > distance:
			cp = line.interpolate(distance)

			return [
				LineString(coords[:i] + [(cp.x, cp.y)]),
				LineString([(cp.x, cp.y)] + coords[i:])]

def cut_by_point(line, pt):
	"""
	cut function that cuts a line and inserts a point at the cut location.

	Parameters
	----------
	line : LineString, line to cut
	pt : Point, a point on the line where the cut is to be made

	Returns
	-------
	array of LineString

	"""
	d = line.project(Point(pt))
	if d <= 0.0 or d >= line.length:
		return [LineString(line)]
	coords = list(line.coords)
	for i, c in enumerate(coords):
		cd = line.project(Point(c))
		if cd == d:
			cutline = [LineString(coords[:i]), LineString(coords[i:])]
			break
		elif cd > d:
			cutline = [LineString(coords[:i] + [(pt.x, pt.y)]), LineString([(pt.x, pt.y)] + coords[i:])]
			break
	else:
		print 'loop fell through without finding the point'

	return cutline

def cut_by_distances(line, intersections):
	"""
	Doesn't really do what the method name implies, isn't used, should change or remove.
	Cut a line at multiple points by calculating the distance of each point along the line. Uses the cut_by_distance function.

	Parameters
	----------
	line : LineString, line to cut
	intersections : MultiPoint, object containing cut points

	Returns
	-------
	MultiLineString

	"""
	for i in intersections:
		d = line[-1].project(Point(i))
		if len(list(line)) == 1:
			line = cut_by_distance(line[-1], d)
		elif len(list(line)) > 1:
			cutline = cut_by_distance(line[-1], d)
			line = line[:-1] + cutline
	return MultiLineString(line)

def cut_by_points(line, intersections):
	"""
	Use the cut_by_point function

	Parameters
	----------
	line : LineString, line to cut
	intersections : MultiPoint, object containing cut points

	Returns
	-------
	MultiLineString

	"""
	for i in intersections:
		if len(list(line)) == 1:
			line = cut_by_point(line[-1], i)
		elif len(list(line)) > 1:
			cutline = cut_by_point(line[-1], i)
			line = line[:-1] + cutline
	return MultiLineString(line)

def sign(line1, line2):
	"""
	Iterates over points in two lines to identify line intersections at identical coordinates.
	At each intersection looks ahead and projects the next coordinate from line2 onto line1, and determines whether line2 is left or right of line1.
	Left offsets give a negative sign representing cut; right offsets give positive sign representing fill.

	Parameters
	----------
	line1 : LineString
	line2 : LineString

	Returns
	-------
	signs : array, members are positive or negative integer one

	"""
	signs = []
	for i in range(len(line1.coords)-1):
		for j in range(len(line2.coords)-1):
			if Point(line1.coords[i]).equals(Point(line2.coords[j])):
				pp = project(
					Point(line1.coords[i][0], line1.coords[i][1], 0),
					Point(line1.coords[i+1][0], line1.coords[i+1][1], 0),
					Point(line2.coords[j+1][0], line2.coords[j+1][1], 0))
				if pp['offset'] < 0:
					signs.append(-1)
				elif pp['offset'] > 0:
					signs.append(1)
	return signs

def extend(line, pt, prepend):
	"""
	Extends a LineString by one Point, which may be prepended at the start of the LineString, or appended at the end.

	Parameters
	----------
	line : LineString, the line to extend
	pt : Point, the coordinate to extend to
	prepend : boolean, if True then prepend, else append

	Returns
	-------
	LineString

	"""
	xs, ys = zip(*list(line.coords))
	if prepend==True:
		xs = [pt.x] + list(xs)
		ys = [pt.y] + list(ys)
	else:
		xs = list(xs) + [pt.x]
		ys = list(ys) + [pt.y]
	return LineString(zip(xs, ys))

def update(line, pt, idx):
	"""
	Parameters
	----------
	line : LineString, the line to update
	pt : Point, the new coordinate
	idx : idx, the index of the vertex to update

	Returns
	-------
	LineString

	"""	
	xs, ys = zip(*list(line.coords))
	xs = list(xs)
	ys = list(ys)
	xs[idx] = pt.x
	ys[idx] = pt.y
	print zip(xs,ys)
	return LineString(zip(xs, ys))

def difference(line1, line2, close):
	"""
	Creates polygons from two LineString objects.

	Parameters
	----------
	line1 : LineString
	line2 : LineString
	close : boolean, option to close open line ends with vertical line segments

	Returns
	-------
	intersections : array of Points, the intersections between the LineString objects
	polygons : array of Polygons, the polygons between the lines
	signs : array of integers, contains values of +1 or -1 to identify polygons as cut or fill
	
	"""
	if close==True:
		try:
			# prepend
			if line1.coords[0][0] > line2.coords[0][0]:
				# prepend to line1
				bi = line2.intersection(
					LineString([(line1.coords[0][0], line2.bounds[1]-1), (line1.coords[0][0], line2.bounds[3]+1)]))
				if bi.y < line1.coords[0][1]:
					prepend = Point([bi.x, bi.y-1])
				else:
					prepend = Point([bi.x, bi.y+1])
				line1 = extend(line1, prepend, True)
			else:
				# prepend to line2
				bi = line1.intersection(
					LineString([(line2.coords[0][0], line1.bounds[1]-1), (line2.coords[0][0], line1.bounds[3]+1)]))
				if bi.y < line2.coords[0][1]:
					prepend = Point([bi.x, bi.y-1])
				else:
					prepend = Point([bi.x, bi.y+1])
				line2 = extend(line2, prepend, True)
			# append
			if line1.coords[-1][0] < line2.coords[-1][0]:
				# append to line1
				ei = line2.intersection(LineString([(line1.coords[-1][0], line2.bounds[1]-1), (line1.coords[-1][0], line2.bounds[3]+1)]))
				if ei.y < line1.coords[-1][1]:
					append = Point([ei.x, ei.y-1])
				else:
					append = Point([ei.x, ei.y+1])
				line1 = extend(line1, append, False)
			else:
				# append to line2
				ei = line1.intersection(LineString([(line2.coords[-1][0], line1.bounds[1]-1), (line2.coords[-1][0], line1.bounds[3]+1)]))
				if ei.y < line2.coords[-1][1]:
					append = Point([ei.x, ei.y-1])
				else:
					append = Point([ei.x, ei.y+1])
				line2 = extend(line2, append, False)
		except:
			print 'Error: Unable to close line ends. You may need to flip one of your sections.'
			raise
			
	intersections = line1.intersection(line2)

	segs1 = cut_by_points([line1], intersections)
	segs2 = cut_by_points([line2], intersections)

	polygons = polygonize([segs1, segs2])

	signs = sign(linemerge(segs1), linemerge(segs2))

	# can't pass the polygonize generator to my class so convert the polygons into an array
	polygontxt = []
	areas = []
	for i, poly in enumerate(polygons):
		polygontxt.append(poly)
		areas.append(poly.area*signs[i])
	cutfill = pnd.Series(asarray(areas), name='area')

	return intersections, polygontxt, cutfill

def snap_to_points(segments, intersections):
	"""
	Compare segment endpoints in a MultiLineString against points in a Point array to within a given precision;
	if the points match then update the segment endpoint with the coordinate given in the Point array.

	Parameters
	----------
	segments : MultiLineString
	intersections : an array of Points

	Returns
	-------
	MultiLineString : an updated MultiLineString

	"""
	snapped = []
	for s, segment in enumerate(segments):
		coords = list(segment.coords)
		for i, intersection in enumerate(intersections):
			if Point(coords[0]).almost_equals(intersection, decimal=8):
				segment = update(segment, intersection, 0)
			if Point(coords[-1]).almost_equals(intersection, decimal=8):
				segment = update(segment, intersection, len(coords)-1)
		snapped.append(segment)
		
	return MultiLineString(snapped)