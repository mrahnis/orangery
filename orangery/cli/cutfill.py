#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import click

import json
import matplotlib.pyplot as plt
import orangery as o

@click.command(options_metavar='<options>')
@click.argument("file1", nargs=1, type=click.Path(exists=True), metavar='<file_t0>') # help="survey representing the initial condition"
@click.argument("file2", nargs=1, type=click.Path(exists=True), metavar='<file_t1>') # help="survey representing the final condition"
@click.argument("fields", nargs=1, metavar='<fields>') # help="character string identifying the columns"
@click.argument("xs_name", nargs=1, metavar='<name>') # help="name of the cross-section to plot"
@click.option("-o", "--output", metavar='<file>', type=click.File('wb', 0), help="Output file path") 
@click.option("-e", "--exaggeration", metavar='<int>', default=3, help="Vertical exaggeration of plot")
@click.option("--close/--no-close", default=True, help="Close the line ends")
@click.option('-r0', '--reverse-t0', is_flag=True, help="Reverse initial line of section (time t0) shot right-to-left")
@click.option('-r1', '--reverse-t1', is_flag=True, help="Reverse final line of section (time t1) shot right-to-left")
@click.option('-s', '--segment', is_flag=True, help="Prompts user to do interactive segmentation in the console")
@click.option('-v', '--verbose', is_flag=True, help="Enables verbose mode")
def cli(file1, file2, fields, xs_name, output, exaggeration, close, reverse_t0, reverse_t1, segment, verbose):
	"""
	Displays a plot of a repeat survey with cut and fill.
	The console prompts the user to assign a material to each polygon along the line of section.
	Then saves a CSV file containing the net gain or loss of fine sediment.

	\b
	Example:
	cutfill ./examples/data/file_2004.csv ./examples/data/file_2010.csv pxyzctr XS-7 --reverse-t0

	"""

	if verbose is True:
		loglevel = 2
	else:
		loglevel = 0

	logging.basicConfig(stream=sys.stderr, level=loglevel or logging.INFO)

	# load the configuration
	materials_json = 'examples/json/materials.json'
	codebook_json = 'examples/json/codebook.json'

	codebook = json.load(open(codebook_json, 'r'))
	materials = json.load(open(materials_json, 'r'))

	# load the survey data
	s1 = o.Survey(file1, fields, codebook, 0)
	s2 = o.Survey(file2, fields, codebook, 0)

	# select a group of points, in this case a cross section
	xs_pts1 = o.group(s1.data, s1.code_table, group=xs_name)
	xs_pts2 = o.group(s2.data, s2.code_table, group=xs_name)

	# get the endpoints of the group
	p1, p2 = o.endpoints(xs_pts1, reverse=reverse_t0)

	# make the sections
	xs1 = o.Section(xs_pts1, p1, p2, reverse=reverse_t0)
	xs2 = o.Section(xs_pts2, p1, p2, reverse=reverse_t1)

	# calculate the change
	chg = o.Change(xs1, xs2, close_ends=close)

	# plot the change between two cross-sections
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_aspect(exaggeration)

	xs1.plot(ax=ax, marker='o', markersize=4, markerfacecolor='gray', linestyle='none', label='2004')
	xs2.plot(ax=ax, marker='o', markersize=4, markerfacecolor='black', linestyle='none', label='2010')
	chg.polygon_plot(ax=ax, fill_label='Fill', cut_label='Cut')
	chg.annotate_plot(ax=ax)
	ax.set_xlabel('Distance (ft)')
	ax.set_ylabel('Elevation (ft), {0}x exaggeration'.format(exaggeration))
	plt.legend(loc='best')
	plt.title('Cross-section {0}'.format(xs_name))
	plt.show(block = not segment)

	if segment:
		chg.segment(materials)
		chg.save(xs_name)
