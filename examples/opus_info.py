#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script prints information from an OPUS XML file.

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

def printout(args):

	print(get_data_quality(args.opusxml, unit=args.unit))
	print()
	print(get_solution_info(args.opusxml))
	print()
	print(get_mark_info(args.opusxml))


if __name__ == '__main__':

	argparser = argparse.ArgumentParser(description=__doc__)
	argparser.add_argument('opusxml', help="OPUS XML file containing the corrected coordinates")
	argparser.add_argument('-u', '--unit', dest='unit', choices={'m','US_ft'}, default='m', help="the units to use")
	argparser.add_argument('-s', '--spec', dest='spec', choices={'UTM','SPC'}, default='UTM', help="the plane coordinate spec type")

	args = argparser.parse_args()
	printout(args)