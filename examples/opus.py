from __future__ import print_function

import os
import xml.etree.ElementTree as xml
import json
import matplotlib.pyplot as plt
import orangery as o
from orangery.tools.opus import get_plane_coords, get_data_quality, get_solution_info, get_mark_info
from orangery.ops.correction import get_offsets

opusxml = 'opus/2010096o.10o.xml'

filename = 'data/Topo-20100331.csv'
codebook_json = 'json/codebook.json'

bmname = 'BASE2'

# load the configuration
codebook = json.load(open(codebook_json, 'r'))

# load the survey data
s = o.Survey(filename, 'pyxzctr', codebook, 0)

bmrecord = o.pointname(s.data, bmname)

# get the OPUS coordinates in the desired units and projection
coords = get_plane_coords(opusxml, unit='US_ft', spec_type='SPC')

# get the deltas
offsets = get_offsets(bmrecord, coords)

s.history.append('Offset correction between: {0} and {1}\n'.format(bmname, os.path.basename(opusxml)))
s.translate(offsets)

dirpath = os.path.dirname(filename)
fnsplit = os.path.splitext(os.path.basename(filename))
outname = '{0[0]}-corr{0[1]}'.format(fnsplit)

s.save(outname, original_header=True)

#print(get_data_quality(opusxml, unit='US_ft'))

#get_solution_info(opusxml)

#get_mark_info(opusxml)