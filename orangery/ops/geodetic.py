# consider doing all this with
# http://geographiclib.sourceforge.net/

from __future__ import print_function
from math import pow, sqrt, cos, sin, atan, radians, degrees, modf
# from numba import vectorize, float64, jit

def wgs84():
	# calculates the WGS84 ellipsoidal parameters
	a = 6378137.000
	f = 1/298.257223563
	#f = 0.0033528106647474805
	return ellipsoid(a,f)

# dict returned to represent ellipsoid will not work with numba (unless in object mode, not desirable)
# stackoverflow response to similar: http://stackoverflow.com/questions/27889463/optimizing-dict-of-set-of-tuple-of-ints-with-numba
def ellipsoid(a, f):
	b = a*(1-f)
	#b = 6356752.31424518 
	e1 = sqrt((a**2 - b**2)/a**2)
	e2 = sqrt((a**2 - b**2)/b**2)
	return {'a':a, 'f':f, 'b':b, 'e1':e1, 'e2':e2}
	# return [a, f, b, e1, e2]

def radius_of_curvature(φ, ellipsoid):
	N = ellipsoid['a'] / sqrt(1 - ellipsoid['e1']**2 * sin(φ)**2)
	# N = ellipsoid[0] / sqrt(1 - ellipsoid[3]**2 * sin(φ)**2)
	return N

def height_above_ellipsoid(p, N, φ):
	h = p/cos(φ) - N
	return h

def lla2ecef(ƛ,φ,h, ellipsoid=wgs84()):
	# LLA to ECEF
	# φ : geodetic latitude, phi, in radians
	# ƛ : geodetic longitude, lambda, in radians
	# h : height above the ellipsoid in meters
	# N : radius of curvature of the ellipsoid in meters
	N = radius_of_curvature(φ, ellipsoid)

	X = (N + h)*cos(φ)*cos(ƛ)
	Y = (N + h)*cos(φ)*sin(ƛ)
	Z = ((ellipsoid['b']**2/ellipsoid['a']**2)*N + h)*sin(φ)
	# Z = ((ellipsoid[2]**2/ellipsoid[0]**2)*N + h)*sin(φ)

	return X,Y,Z

def ecef2lla_direct(X,Y,Z, ellipsoid=wgs84()):
	# ECEF to LLA by direct solution

	# auxilliary values
	p = sqrt(X**2 + Y**2)
	θ = atan((Z*ellipsoid['a'])/(p*ellipsoid['b']))
	# θ = atan((Z*ellipsoid[0])/(p*ellipsoid[2]))

	# calculation
	ƛ = atan(Y/X)
	φ = atan((Z + ellipsoid['e2']**2 * ellipsoid['b'] * sin(θ)**3) / (p - ellipsoid['e1']**2 * ellipsoid['a'] * cos(θ)**3))
	# φ = atan((Z + ellipsoid[4]**2 * ellipsoid[2] * sin(θ)**3) / (p - ellipsoid[3]**2 * ellipsoid[0] * cos(θ)**3))

	N = radius_of_curvature(φ, ellipsoid)
	h = height_above_ellipsoid(p, N, φ)

	return degrees(ƛ),degrees(φ),h

def ecef2lla_bowring(X,Y,Z, ellipsoid=wgs84()):
	# ECEF to LLA iterating using method of Bowring

	ƛ = atan(Y/X)

	p = sqrt(X**2 + Y**2)

	# initial estimated values
	φ = atan(Z/(p*(1-ellipsoid['e1']**2)))
	# φ = atan(Z/(p*(1-ellipsoid[3]**2)))
	N = radius_of_curvature(φ, ellipsoid)
	h = 0

	while abs(h - height_above_ellipsoid(p, N, φ)) > 0.00001:
		N = radius_of_curvature(φ, ellipsoid)
		h = height_above_ellipsoid(p, N, φ)
		φ_current = φ 
		φ = atan(Z/(p*(1-ellipsoid['e1']**2*N/(N+h))))
		# φ = atan(Z/(p*(1-ellipsoid[3]**2*N/(N+h))))
		#print("N {0} h {1} φ {2}".format(N, h, φ_current))

	return degrees(ƛ),degrees(φ_current),h