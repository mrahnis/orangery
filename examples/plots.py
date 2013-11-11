"""
Plots a map of a survey and a single cross-section from that survey.
"""
import json
import matplotlib.pyplot as plt
import orangery as o
from orangery.tools.plotting import get_scale_factor

filename = 'data/file_2004.csv'
format_json = 'json/format.json'

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
ve = 2

title = 'Cross-section {0}'.format(xs_name)
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
xs.plot(ax=ax2, linestyle='-', label='2004')
ax2.set_aspect(ve)
ax2.set_xlabel('Distance (ft)')
ax2.set_ylabel('Elevation (ft), {0}x exaggeration'.format(ve))

# set the desired scale
scale = 5
scale_factor = get_scale_factor(fig2, ax2, scale)
fig2.set_size_inches(fig2.get_size_inches()*scale_factor)

plt.title(title)
plt.legend(loc='best')
fig2.savefig('test.png', dpi=300)
plt.show(block=True)