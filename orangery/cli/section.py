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
@click.argument('fields', nargs=1, metavar='<fields>') # help="character string identifying the columns"
@click.argument('xs_name', nargs=1, metavar='<name>') # help="name of the cross-section to plot"
@click.option('--codes', 'codes_f', nargs=1, type=click.Path(exists=True), metavar='<codes_file>', help="JSON file representing the usage intent of a set of survey codes")
@click.option('--show/--save', is_flag=True, default=True, help="Show the plot or save to files; --show is the default")
@click.option('--units', type=click.Choice(['m','sft','ft']), default='m', help="Unit to show in axis labels")
@click.option('--label', nargs=1, metavar='<text>', help="Label to display in the legend")
@click.option('--exaggeration', metavar='<int>', default=3, help="Vertical exaggeration of plot")
@click.option('--scale', nargs=2, metavar='<float int>', type=click.Tuple([float, int]), default=(10, 300), help="Scale where first argument is units per-inch on the horizontal axis and second argument is output DPI")
@click.option('--reverse/--no-reverse', is_flag=True, default=False, help="Reverse the line of section")
@click.option('--exclude', nargs=1, multiple=True, metavar='<str>', help="Exclude a survey code from the section plot")
@click.option('-v', '--verbose', is_flag=True, help="Enables verbose mode")
def section(file1, fields, xs_name, codes_f, show, units, label, exaggeration, scale, reverse, exclude, verbose):
    """Displays a cross-section plot.

    \b
    The section subcommand takes three arguments:
    <file_t0> : survey data representing the initial condition in csv format
    <fields> : series of characters describing the data columns
    <name> : name of cross-section to plot

    Options allow to set various properties of the plot. The default is to --show the plot.
    With the --save option the plot will be saved as an image.

    \b
    Example:
    orangery section file_2004.csv pxyzctr XS-7 --reverse t0

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

    # select a group of points, in this case a cross section
    xs_pts1 = o.group(s1.data, s1.code_table, group=xs_name, exclude=exclude)

    # get the endpoints of the group
    p1, p2 = o.endpoints(xs_pts1, reverse=reverse)

    # make the sections
    xs1 = o.Section(xs_pts1, p1, p2, reverse=reverse)

    if label:
        label = label
    elif 't' in fields:
        label = (xs1.data.iloc[0]['t']).split('T')[0]
    else:
        label = 't0'

    # plot the change between two cross-sections
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect(exaggeration)

    xs1.plot(ax=ax, marker='o', markersize=4, markerfacecolor='white', markeredgecolor='black', linestyle='-', color='gray', label=label)
    ax.set_xlabel('Distance ({0})'.format(units))
    ax.set_ylabel('Elevation ({0}), {1}x exaggeration'.format(units, exaggeration))
    plt.legend(loc='best')
    plt.title('Cross-section {0}'.format(xs_name))

    if show:
        plt.show()
    else:
        fname = xs_name + '-' + label.replace('-', '')
    
        scale_factor = get_scale_factor(fig, ax, scale[0])
        dims = fig.get_size_inches()
        fig.set_size_inches(dims[0]*scale_factor, dims[1]*scale_factor)
        fig.savefig(fname+'.png', dpi=scale[1])
        click.echo('Figure saved to: {}'.format(fname+'.png'))
