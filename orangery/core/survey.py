from __future__ import annotations

import logging
import collections
from typing import Union

import pandas as pnd
from shapely.geometry import Point, LineString
from matplotlib.lines import Line2D

import orangery.ops.text as ot
import orangery.ops.geometry as og
import orangery.ops.correction as oc

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Survey:
    """ A Survey dataset.

    Parameters:
        filename (str) : the path to the file to read.
        format (str) : a string of characters that describes the survey data. Accepts:
            p    - point
            x, e - x coord, easting
            y, n - y coord, northing
            z, h - z coord
            d, s - distance, station
            o    - offset
            t    - timestamp
            c    - code
            r    - remark
            q    - quality
            f    - foresight
            a    - attribute
            The string may contain the characters in any order, without duplicates, except for 'a' which may occur multiple times. The string must contain x/e,y/n,z/h or d/s,z/h.
            Examples: 'pyxzctnff', 'pnezfrf'
        codebook (dict) : a dict that describes the codes used in the survey.
        header (int) : the row number of the header. As in pandas it is 0 by default. If there is no header row specify 'None'.
        kwargs (dict) : keyword arguments passed to pandas.read_csv.

    """
    def __init__(
        self,
        filename: str,
        columns: str,
        codebook: dict,
        header: int = 0,
        **kwargs
    ):
        self.filename = filename
        self.codebook = codebook

        try:
            self.data = pnd.read_csv(filename, header=header, **kwargs)

            known_columns = set(('p','x','y','z','n','e','s','o','z','t','d','c','r','q','f','a'))
            columns_tmp = list(columns.lower())
            #columns = columns.lower()

            if set(columns_tmp).issubset(known_columns) == False:
                unrecognized = set(columns_tmp).difference(known_columns)
                logger.warning('Unrecognized column entry: {0}'.format(unrecognized))

            columns_tmp = [c.replace('a', 'a'+str(i)) for i, c in enumerate(columns)]

            if len(set(columns_tmp)) < len(columns_tmp):
                duplicates = [i for i, c in collections.Counter(columns).items() if c > 1]
                logger.warning('Duplicate columns: {0}'.format(duplicates))

            columns_tmp = [c.replace('n', 'y') for c in columns]
            columns_tmp = [c.replace('e', 'x') for c in columns]
            columns_tmp = [c.replace('h', 'z') for c in columns]
            columns_tmp = [c.replace('s', 'd') for c in columns]

            # get inverse map of the dataframe column names, then rename columns for internal use
            self.format = collections.OrderedDict(zip(columns_tmp, self.data.columns))
            inv_col_map = {v:k for k, v in self.format.items()}
            self.data.rename(columns=inv_col_map, inplace=True)
        except:
            logger.error('Failed to read CSV file: {0}'.format(filename))
            raise
        try:
            self.code_table = ot.parse(self.data, self.codebook)
        except:
            logger.error('Failed to parse CSV file: {0}'.format(filename))
            raise

    def translate(self, deltas: list[float]):
        """
        Translate the data by an xyz offset and add a line to history.
        """
        self.data = oc.translate(self.data, deltas)
        # add a line to history
        logger.info('Translated data by x,y,z offsets: {0[0]}, {0[1]}, {0[2]}\n'.format(deltas))

    def save(
        self,
        filename: Union[None, str] = None,
        original_header: bool = False,
        write_history: bool = False
    ):
        """
        Save the data to a file
        """
        if original_header==True:
            output = self.data.rename(columns=self.format, inplace=False)
        else:
            output = self.data

        output.to_csv(filename)
        logger.info('Saved data to: {0}'.format(filename))

    def plot(self, **kwargs) -> Line2D:
        """Plot the x, y values of the data.

        Parameters:
            kwargs (dict) : Keyword arguments to be passed to Pandas and matplotlib.

        Returns:
            ax (Axis) : a matplotlib Axis.

        """
        if {'x','y','z'}.issubset(self.data.columns):
            ax = self.data.plot('x','y', **kwargs)
        else:
            logger.warning('x,y columns not available in this data')
            ax = None
        return ax


class Section:
    """A Section view of a set of x,y,z coordinates.

    Parameters:
        data (pandas.DataFrame) : contains the data to project.
        p1 (shapely.Point) : the start of a line of section.
        p2 (shapely.Point) : the end of a line of section.
        reverse (bool) : reverse the order of points in the section.
        z_adjustment (float) : adjust the elevation of the data.

    """
    def __init__(
        self,
        data: pnd.DataFrame,
        p1: Point,
        p2: Point,
        reverse: bool = False,
        z_adjustment: Union[None, float] = None
    ):
        self.data = data
        self.p1, self.p2 = p1, p2

        self.projection = None
        self.line = None
        self.date = None

        if reverse == True:
            self.data.sort_index(ascending=False, inplace=True) # flip sections shot right to left
        if z_adjustment != None:
            self.data['z'] = self.data['z'] + z_adjustment

        self.projection = og.project_points(self.data, self.p1, self.p2)
        self.line = LineString(list(zip(self.projection['d'],self.projection['z'])))
        self.date = (self.data.iloc[0]['t']).split('T')[0]

    def plot(self, view='section', **kwargs) -> Union[None, Line2D]:
        """Plot the d, z values of the projected data.

        Parameters:
            view (str) : Valid entries are 'section' and 'map'. Default is 'section' view.
            kwargs (dict) : Keyword arguments to be passed to Pandas and matplotlib.

        Returns:
            ax (Axis) : a matplotlib Axis.

        """
        if view=='section':
            ax = self.projection.plot('d','z',**kwargs)
        elif view=='map':
            ax = self.data.plot('x','y',**kwargs)
        else:
            logger.warning('{0} is not a valid view option'.format(view))
            ax = None
        return ax


class LevelSection:
    """
    A Section view of a set of d,z coordinates. Z values may be calculated based on backsight, foresight and datum elevation.
    """
    def __init__(self, data, p1, p2, backsight=0.0, datum=0.0, reverse=False, z_adjustment=None):
        self.data = data
        self.datum = datum
        self.backsight = backsight

        self.location = None # this will assign x,y values to the data based on p1, p2 coordinates
        self.line = None

        if {'f'}.isin(self.data.columns):
            logger.info('calculate elevations')

        if reverse == True:
            self.data.sort(ascending=False, inplace=True) # flip sections shot right to left
        if z_adjustment != None:
            self.data['z'] = self.data['z'] + z_adjustment

        if p1 != None and p2 != None:
            # calculate locations, but instead of dou, calculate xyz
            # xyzdou
            self.location = og.locate_points(self.data, self.p1, self.p2)

        self.line = LineString(list(zip(self.data['d'],self.data['z'])))

    def plot(self, view='section', **kwargs):
        """Plot the d, z values of the data.

        Parameters:
            view (str) : Valid entries are 'section' and 'map'. Default is 'section' view.
            kwargs (dict) : Keyword arguments to be passed to Pandas and matplotlib.

        Returns:
            ax (Axis) : a matplotlib Axis.

        """
        if view=='section':
            ax = self.data.plot('d','z',**kwargs)
        elif view=='map':
            ax = self.location.plot('x','y',**kwargs)
        else:
            logger.warning('{0} is not a valid view option'.format(view))
            ax=None
        return ax
