# consider doing all this with
# http://geographiclib.sourceforge.net/

from __future__ import print_function
from math import pow, sqrt, cos, sin, atan, radians, degrees, modf
from orangery.ops.geodetic import *

# test it out using the default WGS84 ellipsoid
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