#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import click

import xml.etree.ElementTree as xml
import json
import matplotlib.pyplot as plt

import opusxml
import orangery as o
from orangery.ops.correction import get_offsets


def _default_outname(filename):
    dirpath = os.path.dirname(filename)
    fnsplit = os.path.splitext(os.path.basename(filename))
    outname = '{0[0]}-corr{0[1]}'.format(fnsplit)
    return outname


@click.command(options_metavar='<options>')
@click.argument('opusfile', nargs=1, type=click.Path(exists=True), metavar='<opusxml_file>') # help="OPUS XML file containing the corrected coordinates"
@click.argument('filename', nargs=1, type=click.Path(exists=True), metavar='<file>') # help="survey file to adjust"
@click.argument('codes', nargs=1, metavar='<codes_file>') # help="JSON file containing a list of survey codes"
@click.argument('fields', nargs=1, metavar='<fields>') # help="Character string identifying the columns"
@click.argument('point', nargs=1, metavar='<name>', required=True) # help="name of the base or reference point"
@click.option('-o', '--output', type=click.File('wb', 0), metavar='<outfile>', help="Output file path") # default = '{0[0]}-corr{0[1]}'.format(fnsplit)
@click.option('-u', '--unit', metavar='<unit>', type=click.Choice(['m','sft']), default='m', help="Distance units")
@click.option('-s', '--system', metavar='<plane_system>', type=click.Choice(['UTM','SPC']), default='UTM', help="Plane coordinate spec type")
@click.option('--keep-header', 'header', is_flag=True, default=True, help="Keeps the original header")
@click.option('--drop-header', 'header', is_flag=True, help="Drops the original header")
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
def adjust(opusfile, filename, codes, fields, output, point, unit, system, header, verbose):
    """A command-line utility to adjust a survey dataset.

    It translates coordinates by the offset between one coordinate in the dataset and coordinates in an OPUS XML file.

    \b
    Examples:
    adjust opus/2010096o.10o.xml data/Topo-20100331.csv json/codebook.json pyxzctr BASE2 -u sft -s SPC --keep-header

    """
    if verbose is True:
        loglevel = 2
    else:
        loglevel = 0

    logging.basicConfig(stream=sys.stderr, level=loglevel or logging.INFO)
    logger = logging.getLogger('translate')

    codes = json.load(open(codes, 'r'))
    s = o.Survey(filename, fields, codes, 0)

    record = o.pointname(s.data, point)

    solution = opusxml.Solution(opusfile)
    coords = solution.plane_coords(system='SPC', unit=unit)
    offsets = get_offsets(record, coords)

    logger.info('Translating data by offsets between {0} and {1}\n'.format(point, os.path.basename(opusfile)))

    s.translate(offsets)
    s.save(_default_outname(filename), original_header=header)