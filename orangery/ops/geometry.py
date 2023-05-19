from __future__ import annotations

import logging
from typing import Union

import numpy as np
import pandas as pnd
from numpy import asarray
from shapely import box, union, union_all, intersection, intersection_all, get_parts, get_coordinates
from shapely.validation import make_valid
from shapely.geometry import Point, LineString, MultiLineString, MultiPoint, Polygon
from shapely.ops import polygonize, polygonize_full, linemerge, split, snap

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def project2(p1: Point, p2: Point, p3: Point) -> Union[None, dict]:
    """Project a Point, p3 onto a line intersecting Points p1 and p2.

    Adapted from tutorial by Paul Bourke: http://paulbourke.net/geometry/pointline/
    This projection function allows for points at negative distances.

    Parameters:
        p1 (Point) : point at zero distance on line between p1 and p2.
        p2 (Point) : endpoint on line.
        p3 (Point) : the point to project.

    Returns:
        result (dict) : the projected Point, distance along line, offset from line, and fractional distance along line.

    """
    x_delta = p2.x - p1.x
    y_delta = p2.y - p1.y

    if x_delta == 0 and y_delta == 0:
        logger.warning("p1 and p2 cannot be the same point")
        return None

    u = ((p3.x - p1.x) * x_delta + (p3.y - p1.y) * y_delta) / (x_delta * x_delta + y_delta * y_delta)
    pt = Point(p1.x + u * x_delta, p1.y + u * y_delta, p3.z)

    # calculate distance along the line from p1
    if u < 0:
        d = -pt.distance(p1)
    else:
        d = pt.distance(p1)

    # calculate the offset distance of p3 from the line
    if (p1.y - p2.y) * (p3.x -  p2.x) - (p1.x - p2.x) * (p3.y - p2.y) < 0:
        offset = -pt.distance(p3) # the point is offset left of the line
    else:
        offset = pt.distance(p3) # the point is offset right of the line

    result = {'pt':pt, 'd':d, 'o':offset, 'u':u}
    return result


def project(p1: Point, p2: Point, p3: Point) -> dict:
    """Project a Point, p3 onto a line between Points p1 and p2.

    Uses Shapely and GEOS functions, which set distance to zero for all negative distances.

    Parameters:
        p1 (Point) : point at zero distance on line between p1 and p2.
        p2 (Point) : endpoint of line.
        p3 (Point) : the point to project.

    Returns:
        result (dict) : the projected Point, disctance along line, offset from line, and fractional distance along line.

    """
    line = LineString([(p1.x, p1.y),(p2.x, p2.y)])
    u = line.project(p3, normalized=True)
    d = line.project(p3, normalized=False)
    pt_xy = line.interpolate(d)
    pt = Point([pt_xy.x, pt_xy.y, p3.z])

    # calculate the offset distance of p3 from the line
    if (p1.y - p2.y) * (p3.x - p2.x) - (p1.x - p2.x) * (p3.y - p2.y) < 0:
        offset = -pt.distance(p3) # the point is offset left of the line
    else:
        offset = pt.distance(p3) # the point is offset right of the line

    result = {'pt':pt, 'd':d, 'o':offset, 'u':u}
    return result


def project_points(points: pnd.DataFrame, p1: Point, p2: Point) -> pnd.DataFrame:
    """Project multiple points onto a line through Points p1, p2.

    Parameters:
        points (pandas.DataFrame) : survey data to project.
        p1 (Point) : point at zero distance on line between p1 and p2.
        p2 (Point) : endpoint of line.

    Returns:
        result (DataFrame) : DataFrame of projected points, including x, y, z, distance along line, offset from line, and fractional distance along line.

    """
    ppoints = []
    for i in points.index:
        p3 = Point(points.loc[i, 'x'], points.loc[i, 'y'], points.loc[i, 'z'])
        pt = project2(p1, p2, p3)
        if pt is not None:
            ppoints.append((pt['pt'].x, pt['pt'].y, pt['pt'].z, pt['d'], pt['o'], pt['u'])) 

    result = pnd.DataFrame(ppoints, columns=['x','y','z','d','o','u'])
    return result


def cut_by_distance(line: LineString, distance: float) -> list[LineString]:
    """This line cutting function is from shapely recipes http://sgillies.net/blog/1040/shapely-recipes/

    Parameters:
        line (LineString) : the line to cut.
        distance (float) : distance from beginning of line to cutting point.

    Returns:
        segments (LineString array) : array of cut line segments.

    """
    if distance > 0.0 or distance < line.length:
        coords = list(line.coords)
        for i, c in enumerate(coords):
            cd = line.project(Point(c))
            if cd == distance:
                segments = [
                    LineString(coords[:i+1]),
                    LineString(coords[i:])]
            if cd > distance:
                cp = line.interpolate(distance)
                segments = [
                    LineString(coords[:i] + [(cp.x, cp.y)]),
                    LineString([(cp.x, cp.y)] + coords[i:])]
    else:
        segments = [LineString(line)]

    return segments


def cut_by_point(line: LineString, pt: Point) -> list[LineString]:
    """A cut function that divides a line and inserts points at the cut location.

    Parameters:
        line (LineString) : the line to cut.
        pt (Point) : a point on the line where the cut is to be made.

    Returns:
        segments (LineString array) : array of cut line segments.

    """
    distance = line.project(Point(pt))
    offset = line.distance(Point(pt))
    if distance > 0.0 and distance < line.length and offset < 1e-8:
        coords = list(line.coords)
        for i, c in enumerate(coords):
            cd = line.project(Point(c))
            if cd == distance:
                segments = [LineString(coords[:i]), LineString(coords[i:])]
                break
            elif cd > distance:
                segments = [LineString(coords[:i] + [(pt.x, pt.y)]), LineString([(pt.x, pt.y)] + coords[i:])]
                break
    else:
        segments = [LineString(line)]

    return segments


def cut_by_distances(line: LineString, intersections: list[Point]) -> MultiLineString:
    """ Cut a line at multiple points by calculating the distance of each point along the line. Uses the cut_by_distance function.

    Parameters:
        line (LineString) : the line to cut.
        intersections (MultiPoint) : a MultiPoint object containing cut points

    Returns:
        segments (MultiLineString) : contains the line segments.

    """
    for i in intersections:
        cutline = cut_by_distance(line[-1], i)
        line = line[:-1] + cutline
    segments = MultiLineString(line)
    return segments


def cut_by_points(line: LineString, intersections: list[Point]) -> MultiLineString:
    """Cut a line at multiple points by breaking the line and inserting each point. Uses the cut_by_point function.

    Parameters:
        line (LineString) : the line to cut.
        intersections (MultiPoint) : a MultiPoint object containing the cut points.

    Returns:
        segments (MultiLineString) : contains the line segments.

    """
    for i in list(intersections.geoms):
        cutline = cut_by_point(line[-1], i)
        line = line[:-1] + cutline
    segments = MultiLineString(line)
    return segments


def extend(line: LineString, pt: Point, prepend: bool) -> LineString:
    """Extends a LineString by one Point, which may be prepended at the start of the LineString, or appended at the end.

    Parameters:
        line (LineString) : the line to extend.
        pt (Point) : the coordinate to extend to.
        prepend (bool) : if True then prepend, else append.

    Returns:
        newline (LineString) : the extended LineString.

    """
    xs, ys = zip(*list(line.coords))
    if prepend==True:
        xs = [pt.x] + list(xs)
        ys = [pt.y] + list(ys)
    else:
        xs = list(xs) + [pt.x]
        ys = list(ys) + [pt.y]
    newline = LineString(zip(xs, ys))
    return newline


def update(line: LineString, pt: Point, idx: int) -> LineString:
    """Update a point within a LineString

    Parameters:
        line (LineString) : the line to update.
        pt (Point) : the new coordinate.
        idx (int) : the integer index of the vertex to update.

    Returns:
        newline (LineString) : the updated LineString.

    """ 
    xs, ys = zip(*list(line.coords))
    xs = list(xs)
    ys = list(ys)
    xs[idx] = pt.x
    ys[idx] = pt.y
    newline = LineString(zip(xs, ys))
    return newline


def sign(polygon: Polygon, line: LineString) -> int:
    minx, _, maxx, _ = polygon.bounds
    _, miny, _, maxy = (union(box(*polygon.bounds), box(*line.bounds))).bounds

    midx = minx + (maxx - minx) / 2
    test = LineString([(midx, miny), (midx, maxy)])

    poly_zs = get_coordinates(intersection(test, polygon))[:,1]
    line_zs = get_coordinates(intersection(test, line))[:,1]

    # the comparison below fails if the test line intersects the input line more than once
    # this situation occurs when the line at t0 doubles back on itself
    if len(line_zs) == 1:
        if np.any(poly_zs > line_zs):
            sign = 1
        elif np.any(poly_zs < line_zs):
            sign = -1
        else:
            sign = 0
    else:
        logger.warning("Invalid line LineString for t0, returning zero area, check cross section at distance {}".format(midx))
        sign = 0

    return sign


def close(line1: LineString, line2: LineString) -> tuple[LineString, LineString]:
    """Create lines to close left and right cross-section ends

    Do something like this...

    """
    bbox1 = box(*line1.bounds)
    bbox2 = box(*line2.bounds)

    minx, _, maxx, _ = (intersection(bbox1, bbox2)).bounds
    _, miny, _, maxy = (union(bbox1, bbox2)).bounds

    left_closing = LineString([(minx, miny), (minx, maxy)])
    right_closing = LineString([(maxx, miny), (maxx, maxy)])

    return left_closing, right_closing


def difference(line1: LineString, line2: LineString, close_ends: bool = False) -> tuple[list[Point], list[LineString], pnd.Series]:
    """ Create polygons from two LineString objects.

    Parameters:
        line1 (LineString) : a line representing the initial condition.
        line2 (LineString) : a line representing the final condition.
        close_ends (bool) : option to close open line ends with vertical line segments.

    Returns:
        intersections (Point array) : the intersections between the LineString objects.
        polygons (Polygon array) : the polygons between the lines.
        signs (int array) : contains values of +1 or -1 to identify polygons as cut or fill.

    """
    if close_ends==True:
        # get the left and right bounding lines
        left_close, right_close = close(line1, line2)

        # get the intersections on the bounding line
        left_intersections = MultiPoint(intersection_all([[left_close, line1], [left_close, line2]], axis=1))
        right_intersections = MultiPoint(intersection_all([[right_close, line1], [right_close, line2]], axis=1))
        intersections = union_all([intersection(line1, line2), left_intersections, right_intersections])

        # build the list of segments
        left_segs = get_parts(split(left_close, left_intersections))
        right_segs = get_parts(split(right_close, right_intersections))
        segs1 = get_parts(cut_by_points([line1], intersections))
        segs2 = get_parts(cut_by_points([line2], intersections))
        segs = segs1.tolist() + segs2.tolist() + left_segs.tolist() + right_segs.tolist()
    else:
        intersections = intersection(line1, line2)
        segs1 = get_parts(split(line1, intersections))
        segs2 = get_parts(split(line2, intersections))
        segs = segs1.tolist() + segs2.tolist()

    # polygons = polygonize(segs)

    # use polygonize_full and make_valid to find the invalid geometries
    _polygons, _cuts, _dangles, _invalid = polygonize_full(segs)
    polygons = get_parts(_polygons).tolist()

    for invalid in get_parts(_invalid).tolist():
        polygons += [make_valid(Polygon(invalid.coords))]
        # the problem is in the 2022 data at 46.8 ft
        # the line of section doubles-back on itself zoom in to see
        # pre-sorting the points by distance would fix but may not always desireable?

    areas = []
    for poly in polygons:
        s = sign(poly, line1)
        areas.append(poly.area*s)

    cutfill = pnd.Series(asarray(areas), name='area')

    return intersections, polygons, cutfill


def snap_to_points(segments: MultiLineString, intersections: list[Point]) -> MultiLineString:
    """Snap line segment endpoints to given points

    Compare segment endpoints in a MultiLineString against points in a Point array to within a given precision;
    if the points match then update the segment endpoint with the coordinate given in the Point array.

    Parameters:
        segments (MultiLineString) : the line segments to snap.
        intersections (Point array) : the points to snap to.

    Returns:
        newline (MultiLineString) : an updated MultiLineString.

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
    newline = MultiLineString(snapped)
    return newline
