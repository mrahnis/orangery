#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A command-line utility to adjust a survey dataset. It translates coordinates by the offset between one coordinate in the dataset and coordinates in an OPUS XML file.

Examples:
python translate_to_coords.py opus/2010096o.10o.xml data/Topo-20100331.csv json/codebook.json pyxzctr -p BASE2 -u US_ft -s SPC --keep-header

"""

from __future__ import print_function

import os
import sys
import logging
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

def main(args):

	logging.basicConfig(stream=sys.stderr, level=args.loglevel or logging.INFO)

	codes = json.load(open(args.codes, 'r'))
	s = o.Survey(args.filename, args.fields, codes, 0)

	record = o.pointname(s.data, args.point)
	coords = get_plane_coords(args.opusxml, unit=args.unit, spec_type=args.spec)
	offsets = get_offsets(record, coords)

	logging.info('Translating data by offsets between {0} and {1}\n'.format(args.point, os.path.basename(args.opusxml)))
	
	s.translate(offsets)
	s.save(_default_outname(args.filename), original_header=args.header)

if __name__ == '__main__':

	argparser = argparse.ArgumentParser(description=__doc__)
	argparser.add_argument('opusxml', metavar='OPUS XML FILE', help="OPUS XML file containing the corrected coordinates")
	argparser.add_argument('filename', metavar='INPUT FILE', help="survey file to adjust")
	argparser.add_argument('codes', metavar='CODES', help="JSON file containing a list of survey codes")
	argparser.add_argument('fields', metavar='FIELDS', help="Character string identifying the columns")
	argparser.add_argument('-o', '--output', metavar='OUTPUT FILE', dest='output', type=argparse.FileType('wb', 0), help="output file path") # default = '{0[0]}-corr{0[1]}'.format(fnsplit)
	argparser.add_argument('-p', '--point', metavar='POINT NAME', dest='point', required=True, help="name of the base or reference point")
	argparser.add_argument('-u', '--unit', metavar='DISTANCE UNIT', dest='unit', choices={'m','US_ft'}, default='m', help="the units to use")
	argparser.add_argument('-s', '--spec', metavar='PLANE COORDINATE SPEC', dest='spec', choices={'UTM','SPC'}, default='UTM', help="the plane coordinate spec type")

	argparser.add_argument('--keep-header', dest='header', action='store_true', help="keep the original header")
	argparser.add_argument('--drop-header', dest='header', action='store_false', help="drop the original header")
	argparser.set_defaults(header=True)

	group = argparser.add_mutually_exclusive_group()
	group.add_argument('-v', '--verbose', dest='loglevel', action='store_const', const=logging.DEBUG, help="Verbose (debug) logging")
	group.add_argument('-q', '--quiet', dest='loglevel', action='store_const', const=logging.WARN, help="Silent mode, only log warnings")

	args = argparser.parse_args()
	main(args)