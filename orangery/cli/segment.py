import sys
import logging
import time

import json
import click
import pandas as pnd
import matplotlib.pyplot as plt

import orangery as o


@click.command(options_metavar='<options>')
@click.argument('areas_f', nargs=1, type=click.Path(exists=True), metavar='<areas_file>')
@click.argument('materials_f', nargs=1, type=click.Path(exists=True), metavar='<materials_file>')
def segment(areas_f, materials_f):
    """Prompt the user to assign materials to polygon areas listed in a csv file.

    The segment subcommand takes two arguments: A path to a csv file listing cut-and-fill polygon areas and a path to a JSON file listing possible materials.

    The csv file listing the cut-and-fill polygon areas is created with the --save option of the cutfill subcommand.

    \b
    Example:
    orangery segment XS-3-20130514-20170609.csv materials.json

    """
    def __assign_material(p, low, high):
        prompt = 'Enter a material no. for area {0}: '.format(p)
        err = 'Input must be an integer number between {0} and {1}.'.format(low, high)
        while True:
            try:
                if sys.hexversion >= 0x03000000:
                    m = int(input(prompt))
                else:
                    m = int(raw_input(prompt))
                if low <= m <= high:
                    return m
                else:
                    print(err)
            except ValueError:
                print(err)

    areas = pnd.read_csv(areas_f, index_col=0)
    # materials list and array to track assignment of material to polygon
    materials = json.load(open(materials_f, 'r'))
    materials = materials['materials']
    assignments = []

    print('\n')
    print('Areas')
    print('--------------------')
    print(areas)
    print('-------------------')

    print('\n')
    print("No.   Material")
    print('-------------------')
    for i, material in enumerate(materials):
        print(i, "   ", material['name'])

    print('\n')
    print("Assign a material, by number, to each area")
    print('-------------------')
    for i, area in areas.iterrows():
        m = __assign_material(i, 0, len(materials)-1)
        assignments.append([i, m, materials[m]['name'], materials[m]['density'], materials[m]['fines']])
    assignments_df = pnd.DataFrame(assignments, columns=['polygon', 'material', 'name', 'density', 'fines'])
    result = assignments_df.join(areas)
    result['mass_fines'] = result['density']*result['fines']/100*result['area']

    print('\n')
    print('Results ')
    print('-------------------')
    print(result)
    print('-------------------')
    print('Net change in mass of fines: ', result['mass_fines'].sum())
    
    print('\n')

    if sys.hexversion >= 0x03000000:
        input("Press Enter to exit")
    else:
        raw_input("Press Enter to exit")

    outfile = areas_f.split('.')[0] + '-sgmt.' + areas_f.split('.')[1]
    result.to_csv(outfile)