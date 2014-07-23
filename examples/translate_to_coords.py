#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A command-line utility to adjust a survey dataset. It translates coordinates by the offset between one coordinate in the dataset and coordinates in an OPUS XML file.

Examples:
python opus.py opus/2010096o.10o.xml data/Topo-20100331.csv json/codebook.json pyxzctr -p BASE2 -u US_ft -s SPC --keep-header

"""

from __future__ import print_function

import os
import argparse

import xml.etree.ElementTree as xml
import json
import matplotlib.pyplot as plt

import orangery as o
from orangery.tools.opus import get_plane_coords, get_data_quality, get_solution_info, get_mark_info
from orangery.ops.correction import get_offsets

def _default_outname(filename):
	dirpath = os.path.dirname(filename)
	fnsplit = os.path.splitext(os.path.basename(filename))
	outname = '{0[0]}-corr{0[1]}'.format(fnsplit)
	return outname

def adjust(args):

	codes = json.load(open(args.codes, 'r'))
	s = o.Survey(args.filename, args.fields, codes, 0)

	record = o.pointname(s.data, args.point)
	coords = get_plane_coords(args.opusxml, unit=args.unit, spec_type=args.spec)
	offsets = get_offsets(record, coords)

	s.history.append('Offset correction between: {0} and {1}\n'.format(args.point, os.path.basename(args.opusxml)))
	s.translate(offsets)
	s.save(_default_outname(args.filename), original_header=args.header)

if __name__ == '__main__':

	argparser = argparse.ArgumentParser(description=__doc__)
	argparser.add_argument('opusxml', help="OPUS XML file containing the corrected coordinates")
	argparser.add_argument('filename', help="survey file to adjust")
	argparser.add_argument('codes', help="JSON file containing a list of survey codes")
	argparser.add_argument('fields', help="Character string identifying the columns")
	argparser.add_argument('-o', '--output', dest='output', type=argparse.FileType('wb', 0), help="output file path") # default = '{0[0]}-corr{0[1]}'.format(fnsplit)
	argparser.add_argument('-p', '--point', dest='point', required=True, help="name of the base or reference point")
	argparser.add_argument('-u', '--unit', dest='unit', choices={'m','US_ft'}, default='m', help="the units to use")
	argparser.add_argument('-s', '--spec', dest='spec', choices={'UTM','SPC'}, default='UTM', help="the plane coordinate spec type")

	argparser.add_argument('--keep-header', dest='header', action='store_true', help="keep the original header")
	argparser.add_argument('--drop-header', dest='header', action='store_false', help="drop the original header")
	argparser.set_defaults(header=True)


	args = argparser.parse_args()
	adjust(args)