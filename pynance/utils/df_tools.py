'''
Various functions to drop columns from DataFrames.

Most will requre tickers as the columns to work as intended.
'''

import pandas as pd


def keep_positive_values(df):
    ''' 
    Drops any series from df with negative values.
    ''' 
    keepers = {}
    for i in df:
        if df[i].sum() == df[i].abs().sum():
            keepers[i] = df[i]
    return pd.DataFrame(keepers)

def drop_inadequqte_data(df, n):
    ''' 
    Drops any series from df with less than n data points. 
    '''
    keepers = {}
    for i in df:
        if len(df[i].dropna()) >= n:
            keepers[i] = df[i]
    return pd.DataFrame(keepers)

def mean_within_range(df, lower, upper):
    ''' 
    Drops columns whose mean value is 
    outside the interval [lower, upper). 
    '''
    keepers = {}
    for i in df:
        mu = df[i].mean()
        if mu >= lower and mu < upper:
            keepers[i] = df[i]
    return pd.DataFrame(keepers)

def drop_zeros(df):
    ''' 
    Drop columns with all zeros.
    '''
    keepers = {}
    for i in df:
        if df[i].abs().sum() != 0:
            keepers[i] = df[i]
    return pd.DataFrame(keepers)
        
def drop_NA(df, field):
    ''' 
    Drops any rows that have 'N/A' as the field value, i.e. yahoo data.
    ''' 
    d = df[field].to_dict()
    d = {i: d[i] for i in d if d[i] != 'N/A'}
    return df.T[d.keys()].T
 
def keep_alpha(df):
    ''' 
    Drops elements with non-letters in their index.
    
    '''
    x = []
    for i in df.index:
        if str(i).isalpha():
            x.append(i)
    return (df.T[x]).T           
