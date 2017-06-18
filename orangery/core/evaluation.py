from __future__ import print_function

import sys
import logging
import numpy as np
import pandas as pnd

import orangery.ops.geometry as og

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class Change:
    """ An analysis of the change between two Section objects.

    Parameters
        section1 (Section) : the initial condition.
        section2 (Section) : the final condition.
        close_ends (bool) : True indicates dangles should be closed with a vertical line.

    """
    def __init__(self, section1, section2, close_ends=False):
        self.section1 = section1
        self.section2 = section2

        try:
            self.intersections, self.polygons, self.cutfill = og.difference(self.section1.line, self.section2.line, close_ends=close_ends)
        except:
            logger.error('Error calculating cut and fill')
            raise

    def summarize(self):
        """Prints summary information

        """
        print('\n')
        print("Length: ", self.length())
        print("Fill: ", self.cutfill[self.cutfill > 0].sum())
        print("Cut:  ", self.cutfill[self.cutfill < 0].sum())
        print("Net:  ", self.cutfill.sum())

    def length(self):
        """Return the length of overlap in two sections on which cut and fill was calculated

        Result (float) : legnth of the cross-sectional cut and fill area 

        """
        p1 = self.intersections[0]
        p2 = self.intersections[-1]
        result = p1.distance(p2)

        return result

    def segment(self, materials):
        """Prompt the user to assign material from the materials dict to each polygon in the Change objects

        Parameters
            materials (dict) : a dict containing possible materials

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

        # materials list and array to track assignment of material to polygon
        materials = materials['materials']
        assignments = []

        print('\n')
        print('Areas')
        print('--------------------')
        print(self.cutfill)
        print('-------------------')

        print('\n')
        print("No.   Material")
        print('-------------------')
        for i, material in enumerate(materials):
            print(i, "   ", material['name'])

        print('\n')
        print("Assign a material, by number, to each area")
        print('-------------------')

        for i, poly in enumerate(self.cutfill):
            m = __assign_material(i, 0, len(materials)-1)
            assignments.append([i, m, materials[m]['name'], materials[m]['density'], materials[m]['fines']])
        assignments_df = pnd.DataFrame(assignments, columns=['polygon', 'material', 'name', 'density', 'fines'])

        self.results = assignments_df.join(self.cutfill)
        self.results['mass_fines'] = self.results['density']*self.results['fines']/100*self.results['area']
        print('\n')
        print('Results ')
        print('-------------------')
        print(self.results)
        print('-------------------')
        print('Net change in mass of fines: ', self.results['mass_fines'].sum())
        
        print('\n')

        if sys.hexversion >= 0x03000000:
            input("Press Enter to exit")
        else:
            raw_input("Press Enter to exit")

    def save(self, filename=None):
        # save polygon cut-fill areas to csv
        self.results.to_csv(filename)

# add plot method
import orangery.tools.plotting as _gfx

#Change.plot = _gfx.change_plot
Change.polygon_plot = _gfx.polygon_plot
Change.annotate_plot = _gfx.annotate_plot

