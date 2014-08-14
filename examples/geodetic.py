# consider doing all this with
# http://geographiclib.sourceforge.net/

from __future__ import print_function
from math import pow, sqrt, cos, sin, atan, radians, degrees

# from decimal import *
# getcontext().prec = 28

# WGS84 parameters
a = 6378137.000

f = 1/298.257223563
#f = 0.0033528106647474805

b = a*(1-f)
#b = 6356752.31424518 

e1 = sqrt((a**2 - b**2)/a**2)
e2 = sqrt((a**2 - b**2)/b**2)

def dms2dd(d,m,s):
	dd = d + m*60 + s*3600
	return dd

def radius_of_curvature(φ):
	N = a / sqrt(1 - e1**2 * sin(φ)**2)
	return N

def height_above_ellipsoid(p, N, φ):
	h = p/cos(φ) - N
	return h

def lla2ecef(ƛ,φ,h):
	# LLA to ECEF
	# φ : geodetic latitude, phi, in radians
	# ƛ : geodetic longitude, lambda, in radians
	# h : height above the ellipsoid in meters
	# N : radius of curvature of the ellipsoid in meters

	N = radius_of_curvature(φ)

	X = (N + h)*cos(φ)*cos(ƛ)
	Y = (N + h)*cos(φ)*sin(ƛ)
	Z = ((b**2/a**2)*N + h)*sin(φ)

	return X,Y,Z

def ecef2lla_direct(X,Y,Z):
	# ECEF to LLA by direct solution

	# auxilliary values
	p = sqrt(X**2 + Y**2)
	θ = atan((Z*a)/(p*b))

	# calculation
	ƛ = atan(Y/X)
	φ = atan((Z + e2**2 * b * sin(θ)**3) / (p - e1**2 * a * cos(θ)**3))

	N = radius_of_curvature(φ)
	h = p/cos(φ) - N

	return degrees(ƛ),degrees(φ),h

def ecef2lla_bowring(X,Y,Z):
	# ECEF to LLA iterating using method of Bowring

	ƛ = atan(Y/X)

	p = sqrt(X**2 + Y**2)

	# initial estimated values
	φ = atan(Z/(p*(1-e1**2)))
	N = radius_of_curvature(φ)
	h = 0

	while abs(h - height_above_ellipsoid(p, N, φ)) > 0.00001:
		N = radius_of_curvature(φ)
		h = p/cos(φ) - N
		φ_current = φ 
		φ = atan(Z/(p*(1-e1**2*N/(N+h))))
		#print("N {0} h {1} φ {2}".format(N, h, φ_current))

	return degrees(ƛ),degrees(φ_current),h


# test it out
lat = 39.99277705
lon = -76.26108657
h = 230.920

print("INPUT VALUES")
print("lon {0} lat {1} h {2}".format(lon,lat,h))
print()

ƛ = radians(lon)
φ = radians(lat)

X,Y,Z = lla2ecef(ƛ,φ,h)
print("ECEF COORDINATES")
print("X {0} Y {1} Z {2}".format(X,Y,Z))
print()

lon,lat,h = ecef2lla_bowring(X, Y, Z)
print("WGS84 COORDINATES (BOWRING)")
print("lon {0} lat {1} h {2}".format(lon,lat,h))
print()

lon,lat,h = ecef2lla_direct(X, Y, Z)
print("WGS84 COORDINATES (DIRECT)")
print("lon {0} lat {1} h {2}".format(lon,lat,h))
