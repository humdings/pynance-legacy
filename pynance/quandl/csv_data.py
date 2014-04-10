#The MIT License (MIT)
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


import time

import pandas as pd

from .. settings import (
    COMPANY_DIR, DATE_DIR, FIELD_DIR, all_files
)
from . fetchers import Fundamentals

class DataManager:
    '''
    Saves csv data to a directory.
    
    Note: 
    save_date_csv() and save_field_csv() will include all of 
    the companies currently in the companies directory.
    '''

    def __init__(self, tickers=None, 
                company_dir=COMPANY_DIR, 
                date_dir=DATE_DIR, field_dir=FIELD_DIR):

        self.tickers = tickers
        self.company_dir = company_dir
        self.date_dir = date_dir
        self.field_dir = field_dir        

    def update_all_files(self, **kwargs):
        self.save_companies(**kwargs)
        self.save_date_csv()
        self.save_field_csv()

    def save_companies(self, **kwargs):
        ''' 
        Saves a csv in the company directory for each ticker.
        Use keyword arg 'fields' to specify a field or list of fields, 
        defaults to all financial ratios.

        Note: This respects Quandl's 5000 calls/hour limit, it will pause
              at 4995 calls and wait out the remainder of the hour.
        '''
        tickers = self.tickers
        if 'fields' in kwargs:
            fields = kwargs.pop('fields')
        else:
            fields = 'ALLFINANCIALRATIOS'
        t0, count = time.time(), 0
        for sym in tickers:
            try:
                stock = Fundamentals(sym)
                data = stock.get(fields, **kwargs)
                path = self.company_dir + sym + '.csv'
                data.to_csv(path, index_label='Date')
                count += 1
            except:
                print "Failed to save %s"%sym
                pass
            if count > 4995:
                dt = time.time() - t0
                if dt < 3600:
                    time.sleep(3602 - dt)
                t0, count = time.time(), 0

    def save_date_csv(self):
        '''
        Saves a csv containing all company ratios for all
        companies in Root_C for each date.
        '''
        paths = {
            i.strip('.csv'): self.company_dir + i 
            for i in all_files(self.company_dir)
        }
        data = {
            i: pd.read_csv(paths[i], index_col='Date')
            for i in paths
        }
        dates = []
        for i in data:
            dates.extend(data[i].index)
        dates = list(set(dates))
        by_date = {d: {} for d in dates}
        for d in by_date:
            for sym in data:
                try:
                    by_date[d][sym] = data[sym].T[d]
                except:
                    pass
        for d in by_date:
            path = self.date_dir + d + '.csv'
            df = pd.DataFrame(by_date[d]).T
            df.to_csv(path, index_label='Ticker')

    def save_field_csv(self):
        '''
        Saves a csv for each ratio. 
        The csv has date cols and ticker rows. 
        '''
        paths = {
            i.strip('.csv'): self.company_dir + i 
            for i in all_files(self.company_dir)
        }
        data = {
            i: pd.read_csv(paths[i], index_col='Date').T
            for i in paths
        }
        idx = []
        for i in data:
            idx.extend(list(data[i].index))
        cols = list(set(idx))
        df = {c: {} for c in cols}
        for sym in data:
            for col in cols:
                try:
                    df[col][sym] = data[sym].T[col]
                except:
                    pass
        for i in df:
            path = self.field_dir + i + '.csv'
            dff = pd.DataFrame(df[i]).T
            dff.to_csv(path, index_label='Ticker')


