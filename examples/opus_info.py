#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script prints information from an OPUS XML file.

Examples:
python opus_info.py opus/2010096o.10o.xml -u US_ft -s SPC

"""

from __future__ import print_function

import os
import argparse

import xml.etree.ElementTree as xml
import json
import matplotlib.pyplot as plt

from orangery.tools.opus import get_plane_coords, get_data_quality, get_solution_info, get_mark_info

def printout(args):
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
	argparser.add_argument('opusxml', help="OPUS XML file containing the corrected coordinates")
	argparser.add_argument('-u', '--unit', dest='unit', choices={'m','US_ft'}, default='m', help="the units to use")
	argparser.add_argument('-s', '--spec', dest='spec', choices={'UTM','SPC'}, default='UTM', help="the plane coordinate spec type")

	args = argparser.parse_args()
	printout(args)