import xml.etree.ElementTree as xml
import json
import matplotlib.pyplot as plt
import orangery as o
from orangery.tools.opus import get_plane_coords, get_data_quality, get_solution_info, get_mark_info
from orangery.ops.correction import get_offsets

opusxml = 'opus/2010096o.10o.xml'

filename = 'data/Topo-20100331.csv'
codebook_json = 'json/codebook.json'

# load the configuration
codebook = json.load(open(codebook_json, 'r'))

# load the survey data
s = o.Survey(filename, 'pyxzctn', codebook, 0)

print s.data.head()

base = o.pointname(s.data, 'BASE2')
print
print 'Base Record: ', base

# get the OPUS coordinates in the desired units and projection
coords = get_plane_coords(opusxml, unit='US_ft', spec_type='SPC')
print
print 'OPUS Coords: ', coords

# get the deltas
offsets = get_offsets(base, coords)
print
print 'Offsets: ', offsets

s.translate(offsets)
print
print s.data.head()

#print get_data_quality(opusxml, unit='US_ft')

#get_solution_info(opusxml)

#get_mark_info(opusxml)