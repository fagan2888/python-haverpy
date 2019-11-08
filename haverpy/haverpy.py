# py

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
    # Set the Haver Path
    set_path()

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
    return(df)


def info(series):
    # Set the Haver Path
    set_path()

    # Clean the series names
    split_series = series.split('@')
    code = split_series[0]
    db = split_series[1]
    check_db(db)

    # Get the metadata and conver to dictionary
    info = Haver.metadata(code, db)
    info_as_dict = info.to_dict('list')
    return info_as_dict


def merge(df1, df2, how='outer', check_freq=True):
    if check_freq:
        # Check the inputs have the same frequency
        freq1 = pd.infer_freq(df1.index)
        freq2 = pd.infer_freq(df2.index)
        assert(freq1 == freq2)

    # Perform an a join with 'how'
    df = df1.join(df2, how=how)
    return(df)


def trim(df, start_date='', end_date=''):

    trimmed = df

    if start_date:
        trimmed = trimmed.truncate(before=start_date)

    if end_date:
        trimmed = trimmed.truncate(after=end_date)

    return(trimmed)


def multiseries_function(df1, df2, type_function):
    # Check that at least one input is a dataframe
    assert(isinstance(df1, pd.DataFrame) or isinstance(df2, pd.DataFrame))

    # Create a dataframe out of a single int
    if isinstance(df1, int):
        nrows = len(df2.index)
        value = np.repeat(df1, nrows)
        df1 = pd.DataFrame(value, index=df2.index, columns=['value1'])

    if isinstance(df2, int):
        nrows = len(df1.index)
        value = np.repeat(df2, nrows)
        df2 = pd.DataFrame(value, index=df1.index, columns=['value2'])

    # Rename the variables coming in to allow for merge
    df1.columns = ['value1']
    df2.columns = ['value2']

    # Merge the two series together
    df = merge(df1, df2)

    # Perform the specified operation type
    if type_function == 'addition':
        dataseries = df['value1'].values + df['value2'].values
    elif type_function == 'subtraction':
        dataseries = df['value1'].values - df['value2'].values
    elif type_function == 'multiplication':
        dataseries = df['value1'].values * df['value2'].values
    elif type_function == 'division':
        dataseries = df['value1'].values / df['value2'].values
    else:
        print('The selected type_function "%s" is not supported' %
              (type_function))

    # Create a dataframe
    df_out = pd.DataFrame(dataseries, index=df.index, columns=['dataseries'])
    return(df_out)


def addition(df1, df2):
    # Pass to the multiseries_function
    df = multiseries_function(df1, df2, 'addition')
    return(df)


def subtraction(df1, df2):
    # Pass to the multiseries_function
    df = multiseries_function(df1, df2, 'subtraction')
    return(df)


def multiplication(df1, df2):
    # Pass to the multiseries_function
    df = multiseries_function(df1, df2, 'multiplication')
    return(df)


def division(df1, df2):
    # Pass to the multiseries_function
    df = multiseries_function(df1, df2, 'division')
    return(df)


def lag(df, periods=1):
    # Create a lag
    lagged = df.shift(periods)
    return(lagged)


def lead(df, periods=1):
    # Create a lead
    leaded = lag(df, periods=-periods)
    return(leaded)


def diff(df, periods=1):
    # Calculate the change
    df1 = df
    df2 = lag(df1, periods)
    diffed = subtraction(df1, df2)
    return(diffed)


def diff_bps(df, periods=1):
    # Calculate the change in basis points
    diffed = diff(df, periods)
    diffed_bps = multiplication(diffed, 100)
    return(diffed_bps)


def diff_pct(df, periods=1):
    # Calculate the change as a percent
    df1 = df
    df2 = lag(df1, periods)
    # diffed_pct = 100 * (df1 / df2 - 1)
    divided = division(df1, df2)
    subtracted = subtraction(divided, 1)
    diffed_pct = multiplication(100, subtracted)
    return(diffed_pct)


def movsum(df, window):






