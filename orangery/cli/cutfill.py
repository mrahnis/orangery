#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import time
import click

import json
import matplotlib.pyplot as plt
import orangery as o

@click.command(options_metavar='<options>')
@click.argument('file1', nargs=1, type=click.Path(exists=True), metavar='<file_t0>') # help="survey representing the initial condition"
@click.argument('file2', nargs=1, type=click.Path(exists=True), metavar='<file_t1>') # help="survey representing the final condition"
@click.argument('codes_json', nargs=1, type=click.Path(exists=True), metavar='<codes_file>') # help="json file representing the usage intent of a set of survey codes"
@click.argument('fields', nargs=1, metavar='<fields>') # help="character string identifying the columns"
@click.argument('xs_name', nargs=1, metavar='<name>') # help="name of the cross-section to plot"
@click.option('-o', '--output', metavar='<file>', type=click.File('wb', 0), help="Output file path")
@click.option('--units', type=click.Choice(['m','sft','ft']), default='m', help="Unit to show in axis labels")
@click.option('--labels', nargs=2, help="Labels to display in the legend")
@click.option('--exaggeration', metavar='<int>', default=3, help="Vertical exaggeration of plot")
@click.option('--scale', metavar='<int>', default=10, help="Scale in units per-inch on the horizontal axis")
@click.option('--close/--no-close', default=True, help="Close the line ends; --close is the default")
@click.option('--reverse', type=click.Choice(['t0','t1','tx']), help="Reverse a line or lines of section (t0=initial, t1=final, tx=both)")
@click.option('--withhold', nargs=2, type=click.Tuple([str, click.Choice(['t0','t1','tx'])]), multiple=True, help="Withhold a survey code from a line or lines of section (t0=initial, t1=final, tx=both)")
@click.option('--segment', 'materials_json', nargs=1, type=click.Path(exists=True), metavar='<materials_file>', help="Prompts user to do interactive segmentation in the console using a list of materials.")
@click.option('--summary/--no-summary', default=True, help="Print summary information; --summary is the default")
@click.option('-v', '--verbose', is_flag=True, help="Enables verbose mode")
def cli(file1, file2, codes_json, fields, xs_name, output, units, labels, exaggeration, scale, close, reverse, withhold, materials_json, summary, verbose):
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
	codes = json.load(open(codes_json, 'r'))

	# load the survey data
	s1 = o.Survey(file1, fields, codes, 0)
	s2 = o.Survey(file2, fields, codes, 0)

	withhold_t0 = []
	withhold_t1 = []
	for code in withhold:
		if code[1] in ('t0', 'tx'):
			withhold_t0.append(code[0])
		if code[1] in ('t1', 'tx'):
			withhold_t1.append(code[0])

	# select a group of points, in this case a cross section
	xs_pts1 = o.group(s1.data, s1.code_table, group=xs_name, withhold=withhold_t0)
	xs_pts2 = o.group(s2.data, s2.code_table, group=xs_name, withhold=withhold_t1)

	# get the endpoints of the group
	p1, p2 = o.endpoints(xs_pts1, reverse=reverse in ('t0','tx'))

	# make the sections
	xs1 = o.Section(xs_pts1, p1, p2, reverse=reverse in ('t0','tx'))
	xs2 = o.Section(xs_pts2, p1, p2, reverse=reverse in ('t1','tx'))

	if labels:
		label_t0 = labels[0]
		label_t1 = labels[1]
	elif 't' in fields:
		label_t0 = (xs1.data.iloc[0]['t']).split('T')[0]
		label_t1 = (xs2.data.iloc[0]['t']).split('T')[0]
	else:
		label_t0 = 't0'
		label_t1 = 't1'

	# calculate the change
	chg = o.Change(xs1, xs2, close_ends=close)
	if summary:
		chg.summarize()

	# plot the change between two cross-sections
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_aspect(exaggeration)

	xs1.plot(ax=ax, marker='o', markersize=4, markerfacecolor='white', markeredgecolor='black', linestyle='-', color='gray', label=label_t0)
	xs2.plot(ax=ax, marker='o', markersize=4, markerfacecolor='black', markeredgecolor='black', linestyle='-', color='black', label=label_t1)
	chg.polygon_plot(ax=ax, fill_label='Fill', cut_label='Cut')
	chg.annotate_plot(ax=ax)
	ax.set_xlabel('Distance ({0})'.format(units))
	ax.set_ylabel('Elevation ({0}), {1}x exaggeration'.format(units, exaggeration))
	plt.legend(loc='best')
	plt.title('Cross-section {0}'.format(xs_name))
	plt.show(block = not materials_json)

	from orangery.tools.plotting import get_scale_factor
	scale_factor = get_scale_factor(fig, ax, scale)

	dims = fig.get_size_inches()
	fig.set_size_inches(dims[0]*scale_factor, dims[1]*scale_factor)

	fname = xs_name + '-' + label_t0.replace('-', '') + '-' + label_t1.replace('-', '')
	fig.savefig(fname+'.png', dpi=300)

	if materials_json:
		materials = json.load(open(materials_json, 'r'))
		chg.segment(materials)
		chg.save(fname+'.csv')
