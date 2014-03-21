# -*- coding: utf-8 -*-
#
#Copyright (c) 2014 David Edwards
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

'''
Define where csv data will be saved and useful functions for 
working with them here.

The directory structure is used as an extra dimension so 2-d csv files 
can still be used to work with financial data that generally has 3 dimensions.
   1. Time 
   2. companies.
   3. Various values at each time

Assumes a directory named 'data' exists one level up with the following 
minimum structure.

data/
  companies/
    filename pattern: ticker_symbol.csv
  dates/
    filename pattern: YYYY-MM-DD.csv
  fields/
    filename pattern: financial_quantity.csv
     
other directories defined:
    
data/
  pickle/ ==> pickled objects 
  codes/ ==> quandl/yahoo codes for reference
'''


import os

import pickle

import pandas as pd


#########
# PATHS #
#########

ROOT = os.path.dirname(os.path.abspath(__file__))

# Data saved one level up
DATA_DIRNAME = 'data'

DATA_ROOT = os.path.join(os.sep.join(ROOT.split(os.sep)[:-1]), DATA_DIRNAME)

# Add trailing slashes for convienience 
COMPANY_DIR = os.path.join(DATA_ROOT, 'companies') + os.sep

DATE_DIR = os.path.join(DATA_ROOT,'dates') + os.sep

FIELD_DIR = os.path.join(DATA_ROOT, 'fields') + os.sep

PICKLE_DIR = os.path.join(DATA_ROOT, 'pickle') + os.sep

CODE_DIR = os.path.join(DATA_ROOT, 'codes') + os.sep

data_directories = [
    COMPANY_DIR, DATE_DIR, FIELD_DIR, CODE_DIR
]

########################################################


def all_files(directory, extension='.csv'):
    ''' Returns all filenames ending with 'extension' in a directory. '''
    files = []
    for f in os.listdir(directory):
        if f.endswith(extension):
            files.append(f)
    return files
    
def company_files():
    return all_files(COMPANY_DIR)

def date_files():
    return all_files(DATE_DIR)

def field_files():
    return all_files(FIELD_DIR)

def pickle_files():
    return all_files(PICKLE_DIR, extension='.p')

def get_csv(csv, **kwargs):
    if not csv.endswith('.csv'):
        csv += '.csv'
    for d in data_directories:
        if csv in all_files(d):
            return pd.read_csv(d + csv, **kwargs)
    raise IOError('%s could not be located'%csv)

def load_pickle(filename):
    if not filename.endswith('.p'):
        filename += '.p'
    for f in pickle_files():
        if f.endswith(filename):
            f = open(PICKLE_DIR + f, 'r')
            p = pickle.load(f)
            f.close()
            return p
    raise IOError('%s could not be located'%filename)

