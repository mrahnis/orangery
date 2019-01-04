#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import time
from collections import Counter

import json
import pprint
import click

import orangery as o
from orangery.cli import defaults, util


@click.command(options_metavar='<options>')
@click.argument('file', nargs=1, type=click.Path(exists=True), metavar='<file>') # help="survey representing the initial condition"
@click.argument('fields', nargs=1, metavar='<fields>') # help="character string identifying the columns"
@click.option('--names', 'names', nargs=2, type=click.Tuple([str, str]), metavar='<name col>', help="Name of the cross-section; default will return all names beginning with 'XS'")
@click.option('--codes', 'codes_f', nargs=1, type=click.Path(exists=True), metavar='<codes_file>', help="JSON file representing the usage intent of a set of survey codes")
@click.option('-v', '--verbose', is_flag=True, help="Enables verbose mode")
def info(file, fields, names, codes_f, verbose):
    """Displays information about a survey file or section within a survey file.

    \b
    The cutfill subcommand takes four arguments:
    <file> : survey data representing the initial condition in csv format
    <fields> : series of characters describing the data columns
    <name> : name of cross-section to plot

    \b
    Example:
    orangery info file_2004.csv pxyzctr --name XS-7

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
    s = o.Survey(file, fields, codes, 0)

    xs_pts = o.group(s.data, s.code_table, group=names[0])

    print("Base coordinate")
    print("---------------")
    print(s.data.iloc[0])

    code_list = []
    code_col = s.data['c']
    for codes in code_col:
        code_list += codes.split(' ')

    pp = pprint.PrettyPrinter()
    print()
    print("Codes used")
    print("----------")
    #pp.pprint(sorted(set(code_list)))
    pp.pprint(dict(Counter(code_list)))

    if names:
        name_list = []
        name_col = s.data[names[1]]
        for name in name_col:
            if names[0] in str(name):
                name_list.append(name)
        print()
        print("Named lines")
        print("-----------")
        pp.pprint(sorted(set(name_list)))


