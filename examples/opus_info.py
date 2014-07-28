#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script prints information from an OPUS XML file.

Examples:
python opus_info.py opus/2010096o.10o.xml -u US_ft -s SPC

"""

from __future__ import print_function

import os
import sys
import logging
import argparse

import xml.etree.ElementTree as xml
import json
import matplotlib.pyplot as plt

from orangery.tools.opus import get_plane_coords, get_data_quality, get_solution_info, get_mark_info

def main(args):

	logging.basicConfig(stream=sys.stderr, level=args.loglevel or logging.INFO)

	print(get_plane_coords(args.opusxml, unit=args.unit, spec_type=args.spec))
	print(get_data_quality(args.opusxml, unit=args.unit))
	print()
	print(get_solution_info(args.opusxml))
	print()
	try:
		print(get_mark_info(args.opusxml))
	except:
		print('no info for this mark')

if __name__ == '__main__':

	argparser = argparse.ArgumentParser(description=__doc__)
	argparser.add_argument('opusxml', metavar='OPUS XML FILE', help="OPUS XML file containing the corrected coordinates")
	argparser.add_argument('-u', '--unit', metavar='DISTANCE UNIT', dest='unit', choices={'m','US_ft'}, default='m', help="the units to use")
	argparser.add_argument('-s', '--spec', metavar='PLANE COORDINATE SPEC', dest='spec', choices={'UTM','SPC'}, default='UTM', help="the plane coordinate spec type")

	group = argparser.add_mutually_exclusive_group()
	group.add_argument('-v', '--verbose', dest='loglevel', action='store_const', const=logging.DEBUG, help="Verbose (debug) logging")
	group.add_argument('-q', '--quiet', dest='loglevel', action='store_const', const=logging.WARN, help="Silent mode, only log warnings")

	args = argparser.parse_args()
	main(args)