"""
Plots a map of a survey and a single cross-section from that survey.
"""

import json
import matplotlib.pyplot as plt
import orangery as o

filename = 'data/file_2004.csv'
format_json = 'format.json'

# load the configuration
format = json.load(open(format_json, 'r'))

xs_name = 'XS-7'

# load the survey data
s = o.Survey(filename, format)

# make a map of both surveys
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
s.plot(ax=ax1, marker='o', markersize=4, linestyle='none', label='2004')
ax1.set_aspect(1)
ax1.set_xlabel('Easting (ft)')
ax1.set_ylabel('Northing (ft)')
ax1.grid(True)
ax1.legend(loc='best')
plt.show(block=False)

# select a group of points, in this case a cross section
xs_pts = o.group(s.data, s.code_table, group=xs_name)

# get the endpoints of the group
p1, p2 = o.endpoints(xs_pts, reverse=True)

# make the sections
xs = o.Section(xs_pts, p1, p2, reverse=True)

# plot a single cross-section
exag = 2

title = 'Cross-section {0}'.format(xs_name)
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
xs.plot(ax=ax2, linestyle='-', label='2004')
ax2.set_aspect(exag)
ax2.set_xlabel('Distance (ft)')
ax2.set_ylabel('Elevation (ft), {0}x exageration'.format(exag))
plt.title(title)
plt.legend(loc='best')
plt.show(block=True)