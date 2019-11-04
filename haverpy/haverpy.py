# haverpy.py

# Load needed packages
import Haver
import numpy as np
import pandas as pd
import os.path

def set_path(dir='R:\\_appl\\HAVER\\DATA'):
    # Set the path to the Haver directory
    assert(os.path.exists(dir))
    Haver.path(dir)

def check_db(db):
    # Check that the database exists
    extension = '.DAT'
    fname = os.path.join(Haver.path(), db + extension)
    assert(os.path.isfile(fname))

def fetch(series):
    # Clean the series names
    split_series = series.split('@')
    code = split_series[0]
    db = split_series[1]
    check_db(db)
    
    # Get the data
    df = Haver.data(code, db)

    # Format the dates correctly
    freq = 'D'
    how = 'E'
    df.index = df.index.to_timestamp(freq, how)
    return df

def info(series):
    # Clean the series names
    split_series = series.split('@')
    code = split_series[0]
    db = split_series[1]
    check_db(db)

    # Get the metadata and conver to dictionary
    info = Haver.metadata(code, db)
    info_as_dict = info.to_dict('list')
    return info_as_dict
