from __future__ import annotations

import pandas as pnd
from shapely.geometry import Point


def pointname(df: pnd.DataFrame, name: str) -> pnd.DataFrame:
    """Given a DataFrame return the named point or survey record.

    Parameters:
        df (DataFrame) : survey data records.
        name (str) : name of the point to select.

    Returns:
        result (DataFrame) : records where point field (equivalent to the 'Point name' on Trimble data collectors) is equivalent to the name argument.

    """
    recs = df[df['p'] == name]
    result = df.take(recs.index)
    return result


def group(df: pnd.DataFrame, code_table: pnd.DataFrame, group: str, exclude: list = []) -> pnd.DataFrame:
    """Given a DataFrame return a copy of the survey records belonging to a given group

    Parameters:
        df (DataFrame) : survey data records.
        code_table (DataFrame) : survey data record properties extracted by parse function.
        group (str) : name of the group to select.

    Returns:
        result (DataFrame) : records matching the given group name.

    """
    recs = df.loc[code_table['group'] == group]

    def match(codes, exclude):
        codeset = set(codes.split(' '))
        matches = codeset.intersection(exclude)
        return matches

    mask = recs['c'].apply(lambda x: bool(match(x, set(exclude))))
    masked = recs[~mask]

    result = df.take(masked.index).copy()
    return result


def endpoints(df: pnd.DataFrame, reverse: bool = False) -> tuple[Point, Point]:
    """Given a DataFrame return the first and last survey records.

    Parameters:
        df (pandas.DataFrame) : survey data records.
        reverse (bool) : False returns first then last point, True returns last then first.

    Returns:
        p1, p2 (Point) : first and last records in a DataFrame as Points.

    """
    p1 = Point(float(df[:1]['x']), float(df[:1]['y']), float(df[:1]['z']))
    p2 = Point(float(df[-1:]['x']), float(df[-1:]['y']), float(df[-1:]['z']))
    if reverse == True:
        return p2, p1
    else:
        return p1, p2


def controls(df: pnd.DataFrame, code_table: pnd.DataFrame, codebook: dict) -> pnd.DataFrame:
    """Given a DataFrame return survey records that have control codes.

    Parameters:
        df (pandas.DataFrame) : survey data records.
        code_table (pandas.DataFrame) : survey data record properties extracted by parse function.
        codebook (dict) : a dict that describes the codes used in the survey.

    Returns:
        result (DataFrame) : records having control codes.

    """

    recs = df[code_table['control'].isin(codebook['codes']['control'])]
    result = df.take(recs.index)
    return result


def benchmarks(df: pnd.DataFrame, code_table: pnd.DataFrame, codebook: dict) -> pnd.DataFrame:
    """Given a DataFrame return survey records with benchmark codes.

    Parameters:
        df (pandas.DataFrame) : survey data records.
        code_table (pandas.DataFrame) : survey data record properties extracted by parse function.
        codebook (dict) : a dict that describes the codes used in the survey.

    Returns:
        result (DataFrame) : records having benchmark codes.

    """

    recs = df[code_table['marker'].isin(codebook['codes']['marker'])]
    result = df.take(recs.index)
    return result
