import sys
import logging

import numpy as np
import pandas as pnd
from shapely.geometry import LineString

import orangery.ops.geometry as og
import orangery.tools.plotting as _gfx

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
        #self.polygon_plot = None
        #self.annotate_plot = None

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

    def save(self, filename):
        """Save polygon cut-fill areas to csv file

        Parameters
            filename (str) : file to output
        """
        line = LineString(self.intersections)
        xs, _ = zip(*list(line.coords))
        intervals = zip(xs[0::1], xs[1::1])
        interval_df = pnd.DataFrame(list(intervals), columns=['x0', 'x1'])
        result = interval_df.join(self.cutfill)

        result.to_csv(filename, header=True)


Change.polygon_plot = _gfx.polygon_plot
Change.annotate_plot = _gfx.annotate_plot
