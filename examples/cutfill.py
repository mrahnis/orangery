"""
Displays a plot of a repeat survey with cut and fill.
The console prompts the user to assign a material to each polygon along the line of section.
Then saves a CSV file containing the net gain or loss of fine sediment.
"""
# use a different backend such as TkAgg or WebAgg
#import matplotlib
#matplotlib.use('TkAgg')

# use mpld3
#%matplotlib inline
#from mpld3 import enable_notebook
#enable_notebook()

import json
import matplotlib.pyplot as plt
import orangery as o

file1 = 'data/file_2004.csv'
file2 = 'data/file_2010.csv'
materials_json = 'json/materials.json'
codebook_json = 'json/codebook.json'

# load the configuration
codebook = json.load(open(codebook_json, 'r'))
materials = json.load(open(materials_json, 'r'))

# the cross section to plot
xs_name = 'XS-7'

# load the survey data
s1 = o.Survey(file1, 'pyxzctr', codebook, 0)
s2 = o.Survey(file2, 'pyxzctr', codebook, 0)

# select a group of points, in this case a cross section
xs_pts1 = o.group(s1.data, s1.code_table, group=xs_name)
xs_pts2 = o.group(s2.data, s2.code_table, group=xs_name)

# get the endpoints of the group
p1, p2 = o.endpoints(xs_pts1, reverse=True)

# make the sections
xs1 = o.Section(xs_pts1, p1, p2, reverse=True)
xs2 = o.Section(xs_pts2, p1, p2, reverse=False)

# calculate the change
chg = o.Change(xs1, xs2, close=True)

ve = 3 # vertical exaggeration

# plot the change between two cross-sections

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect(ve)
ax.set_xlabel('Distance (ft)')
ax.set_ylabel('Elevation (ft), {0}x exaggeration'.format(ve))
xs1.plot(ax=ax, marker='o', markersize=4, markerfacecolor='gray', linestyle='none', label='2004')
xs2.plot(ax=ax, marker='o', markersize=4, markerfacecolor='black', linestyle='none', label='2010')
chg.polygon_plot(ax=ax, fill_label='Fill', cut_label='Cut')
chg.annotate_plot(ax=ax)

plt.legend(loc='best')
plt.title('Cross-section {0}'.format(xs_name))
plt.show(block=False)

# if QT binding in matplotlibrc is PySide uncomment the following:
#from matplotlib.pyplot import pause
#pause(0.1)

# or install PyQt4 from http://www.riverbankcomputing.com/software/pyqt/download
# then edit ~/Anaconda/Lib/site-packages/matplotlib/mpl-data/matplotlibrc
# changing from
# backend.qt4 : PySide        # PyQt4 | PySide
# to
# backend.qt4 : PyQt4        # PyQt4 | PySide

chg.segment(materials)
chg.save(xs_name)
