#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import time

import json
import click
import matplotlib.pyplot as plt

import orangery as o
from orangery.cli import defaults, util
from orangery.tools.plotting import get_scale_factor

@click.command(options_metavar='<options>')
@click.argument('file1', nargs=1, type=click.Path(exists=True), metavar='<file_t0>') # help="survey representing the initial condition"
@click.argument('file2', nargs=1, type=click.Path(exists=True), metavar='<file_t1>') # help="survey representing the final condition"
@click.argument('fields', nargs=1, metavar='<fields>') # help="character string identifying the columns"
@click.argument('xs_name', nargs=1, metavar='<name>') # help="name of the cross-section to plot"
@click.option('--codes', 'codes_f', nargs=1, type=click.Path(exists=True), metavar='<codes_file>', help="JSON file representing the usage intent of a set of survey codes")
@click.option('--show/--save', is_flag=True, default=True, help="Show the plot or save to files; --show is the default")
@click.option('--summary/--no-summary', default=True, help="Print summary information; --summary is the default")
@click.option('--units', type=click.Choice(['m','sft','ft']), default='m', help="Unit to show in axis labels")
@click.option('--labels', nargs=2, metavar='<text text>', help="Labels to display in the legend")
@click.option('--exaggeration', metavar='<int>', default=3, help="Vertical exaggeration of plot")
@click.option('--scale', nargs=2, metavar='<float int>', type=click.Tuple([float, int]), default=(10, 300), help="Scale where first argument is units per-inch on the horizontal axis and second argument is output DPI")
@click.option('--close/--no-close', default=True, help="Close the line ends; --close is the default")
@click.option('--reverse', type=click.Choice(['t0','t1','tx']), help="Reverse a line or lines of section (t0=initial, t1=final, tx=both)")
@click.option('--exclude', nargs=2, type=click.Tuple([str, click.Choice(['t0','t1','tx'])]), multiple=True, metavar='<str choice>', help="Exclude a survey code from a line or lines of section (t0=initial, t1=final, tx=both)")
@click.option('--overlay', nargs=1, type=click.Path(exists=True))
@click.option('-v', '--verbose', is_flag=True, help="Enables verbose mode")
def cutfill(file1, file2, fields, xs_name, codes_f, show, summary, units, labels, exaggeration, scale, close, reverse, exclude, overlay, verbose):
	"""Displays a plot of a repeat survey with cut and fill.

	\b
	The cutfill subcommand takes four arguments:
	<file_t0> : survey data representing the initial condition in csv format
	<file_t1> : survey data representing the final condition in csv format
	<fields> : series of characters describing the data columns
	<name> : name of cross-section to plot

	Options allow to set various properties of the plot. The default is to --show the plot.
	With the --save option the plot will be saved as an image along with a csv file containing
	data about cross-sectional cut-and-fill areas along the line of secion.

	\b
	Example:
	orangery cutfill file_2004.csv file_2010.csv pxyzctr XS-7 --reverse t0

	"""
	if verbose is True:
		loglevel = 2
	else:
		loglevel = 0

	logging.basicConfig(stream=sys.stderr, level=loglevel or logging.INFO)

	# load the configuration
	codes = defaults.codes.copy()
	if codes_f:
		user_codes = util.load_config(codes_f)
		codes.update(user_codes)

	# load the survey data
	s1 = o.Survey(file1, fields, codes, 0)
	s2 = o.Survey(file2, fields, codes, 0)

	if overlay:
		s3 = o.Survey(overlay, fields, codes, 0)

	exclude_t0 = []
	exclude_t1 = []
	for code in exclude:
		if code[1] in ('t0', 'tx'):
			exclude_t0.append(code[0])
		if code[1] in ('t1', 'tx'):
			exclude_t1.append(code[0])

	# select a group of points, in this case a cross section
	xs_pts1 = o.group(s1.data, s1.code_table, group=xs_name, exclude=exclude_t0)
	xs_pts2 = o.group(s2.data, s2.code_table, group=xs_name, exclude=exclude_t1)

	xs_pts_overlay = o.group(s3.data, s3.code_table, group=xs_name)

	# get the endpoints of the group
	p1, p2 = o.endpoints(xs_pts1, reverse=reverse in ('t0','tx'))

	# make the sections
	xs1 = o.Section(xs_pts1, p1, p2, reverse=reverse in ('t0','tx'))
	xs2 = o.Section(xs_pts2, p1, p2, reverse=reverse in ('t1','tx'))

	xs_overlay = o.Section(xs_pts_overlay, p1, p2)

	if labels:
		label_t0 = labels[0]
		label_t1 = labels[1]
		label_overlay = labels[3]
	elif 't' in fields:
		label_t0 = (xs1.data.iloc[0]['t']).split('T')[0]
		label_t1 = (xs2.data.iloc[0]['t']).split('T')[0]
		label_overlay = (xs_overlay.data.iloc[0]['t']).split('T')[0]
	else:
		label_t0 = 't0'
		label_t1 = 't1'
		label_overlay = 'pre-restoration'

	# calculate the change
	chg = o.Change(xs1, xs2, close_ends=close)
	if summary:
		chg.summarize()

	import matplotlib
	font = {'family':'normal','weight':'normal','size':16}
	matplotlib.rc('font', **font)
	# plot the change between two cross-sections
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_aspect(exaggeration)

	xs_overlay.plot(ax=ax, marker='None', linestyle='-', linewidth=3, color='tab:red', label=label_overlay)
	xs1.plot(ax=ax, marker='o', markersize=4, markerfacecolor='white', markeredgecolor='black', linestyle='-', color='gray', label=label_t0)
	xs2.plot(ax=ax, marker='o', markersize=4, markerfacecolor='black', markeredgecolor='black', linestyle='-', color='black', label=label_t1)
	chg.polygon_plot(ax=ax, fill_label='Fill', cut_label='Cut')
	chg.annotate_plot(ax=ax)
	ax.set_xlabel('Distance ({0})'.format(units))
	ax.set_ylabel('Elevation ({0}), {1}x exaggeration'.format(units, exaggeration))
	plt.legend(loc='best')
	plt.title('Cross-section {0}'.format(xs_name))

	if show:
		plt.show()
	else:
		fname = xs_name + '-' + label_t0.replace('-', '') + '-' + label_t1.replace('-', '')
	
		scale_factor = get_scale_factor(fig, ax, scale[0])
		dims = fig.get_size_inches()
		fig.set_size_inches(dims[0]*scale_factor, dims[1]*scale_factor)
		fig.savefig(fname+'.png', dpi=scale[1])
		click.echo('Figure saved to: {}'.format(fname+'.png'))

		chg.save(fname+'.csv')
		click.echo('Data saved to: {}'.format(fname+'.csv'))
