import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def get_offsets(df, coords):
    """
    Calulate the x,y,z offsets between a dataframe record, and an array of x,y,z coordinates.
    """
    if len(df) == 1:
        offsets = [coords[0].magnitude - df.iloc[0]['x'], coords[1].magnitude - df.iloc[0]['y'], coords[2].magnitude - df.iloc[0]['z']]
        return offsets
    else:
        logger.error('df can have only one record. df has {0} records.'.format(len(df)))


def translate(df, offsets):
    """
    Translate the x,y,z coordinates for records in a dataframe by an array of offsets.
    """
    df['x'] = df['x'] + offsets[0]
    df['y'] = df['y'] + offsets[1]
    df['z'] = df['z'] + offsets[2]
    return df
