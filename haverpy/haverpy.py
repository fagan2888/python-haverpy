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
    # Set the Haver Path
    haverpy.set_path()

    # Clean the series names
    split_series = series.split('@')
    code = split_series[0]
    db = split_series[1]
    haverpy.check_db(db)

    # Get the data
    df = Haver.data(code, db)

    # Format the dates correctly
    freq = 'D'
    how = 'E'
    df.index = df.index.to_timestamp(freq, how)
    return df


def info(series):
    # Set the Haver Path
    haverpy.set_path()

    # Clean the series names
    split_series = series.split('@')
    code = split_series[0]
    db = split_series[1]
    haverpy.check_db(db)

    # Get the metadata and conver to dictionary
    info = Haver.metadata(code, db)
    info_as_dict = info.to_dict('list')
    return info_as_dict


def merge(df1, df2, how='outer'):
    # Check the inputs are the same frequency
    freq1 = pd.infer_freq(df1.index)
    freq2 = pd.infer_freq(df2.index)
    assert(freq1 == freq2)

    # Perform an a join with 'how'
    df = df1.join(df2, how=how)
    return df


def multiseries_function(df1, df2, type_function):
    # Check that at least one input is a dataframe
    assert(isinstance(df1, pd.DataFrame) or isinstance(df2, pd.DataFrame))

    # Create a dataframe if adding just one value
    if isinstance(df1, int):
        nrows = len(df2.index)
        value = np.repeat(df1, nrows)
        df1 = pd.DataFrame(value, index=df2.index, columns=['value1'])

    if isinstance(df2, int):
        nrows = len(df1.index)
        value = np.repeat(df2, nrows)
        df2 = pd.DataFrame(value, index=df1.index, columns=['value2'])

    # Rename the variables coming in
    df1.columns = ['value1']
    df2.columns = ['value2']

    # Merge the two series together
    df = haverpy.merge(df1, df2)

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
    assert(np.sign(periods) == 1)
    df = df.shift(periods)
    return(df)


def lead(df, periods=-1):
    # Create a lead
    assert(np.sign(periods) == -1)
    df = df.shift(periods)
    return(df)
