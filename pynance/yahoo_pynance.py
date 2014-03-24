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



import os
import datetime
import cStringIO
import csv
import webbrowser

from urllib2 import Request, urlopen
from urllib import urlencode, urlretrieve

import pandas as pd



class HistoricalData(pd.DataFrame):
    
    def __init__(self, symbol, start_date, end_date, interval='d'):
        start_date = str(start_date)
        end_date = str(end_date)
        url = 'http://ichart.finance.yahoo.com/table.csv?' 
        url += 's={}&a={}&b={}&c={}&d={}&e={}&f={}&g={}'.format(  
            symbol,  
            str(int(start_date[5:7]) - 1),  
            str(int(start_date[8:10])),  
            str(int(start_date[0:4])),  
            str(int(end_date[5:7]) - 1),  
            str(int(end_date[8:10])),
            str(int(end_date[0:4])),
            interval,
        )  
        url += '&ignore=.csv'  
        data = pd.read_csv(url, index_col='Date', parse_dates=True).sort_index()
        super(HistoricalData, self).__init__(data)
        self.symbol = symbol        


class Stock(object):
    '''
    Most recent stock quote according to Yahoo.
    Most fields are included, all possible fields can be found at:
    
    https://code.google.com/p/yahoo-finance-managed/wiki/enumQuoteProperty

    NOTE: Yahoo csv data can be up to 15 min delayed.

    '''
    fields = {
        'price': 'l1', 
        'change':'c1', 
        'volume':'v',
        'avg_daily_volume': 'a2',
        'stock_exchange': 'x',
        'market_cap':'j1',
        'book_value': 'b4',
        'ebitda': 'j4', 
        'dividend_per_share': 'd',
        'dividend_yield': 'y',
        'earnings_per_share': 'e',
        'fifty_two_week_high': 'k',
        'fifty_two_week_low': 'j', 
        'fifty_day_moving_avg': 'm3',
        'two_hundred_day_moving_avg':'m4',
        'price_earnings_ratio':'r',
        'price_earnings_growth_ratio':'r5',
        'price_sales_ratio':'p5',
        'price_book_ratio': 'p6',
        'short_ratio': 's7', 
        'revenue': 's6',
        'pct_change_from_50_day_MA':'m8',
        'pct_change_from_200_day_MA': 'm6', 
        'one_yr_target_price': 't8',
    }
    def __init__(self, symbol):
        self.symbol = symbol
        self.all = self._all_quote_data()
        self.timestamp = datetime.datetime.now()
        for quote in self.all:
            self.__dict__[quote] = self.all[quote]

    def __getitem__(self,item):
        return self.all[item]

    def __iter__(self):
        return iter(self.all)

    def __repr__(self):
        return "<%s: %s>"%(self.symbol, self.timestamp)

    def _quote_request(self, stat):
        url = "http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=%s" %(
            self.symbol, 
            stat
        )
        req = Request(url)
        response = urlopen(req)
        return str(response.read().decode('utf-8').strip())

    def _all_quote_data(self):
        s = ''
        for i in self.fields.values():
            s += i 
        data = [i.strip('" ') for i in self._quote_request(s).split(',')]
        quotes = dict(zip(self.fields.keys(), data))
        for q in quotes:
            try:
                quotes[q] = float(quotes[q])
            except ValueError:
                pass
        return quotes

    def chart(self, **kwargs):
        return StockChart(self.symbol, **kwargs)

    def history(self, start_date, end_date, **kwargs):
        return HistoricalData(self.symbol, start_date, end_date, **kwargs)

    def update(self):
        self.__init__(self.symbol)


class StockChart():
    """
    A Yahoo Stock Chart. 
    Can be opened in browser or saved.
    
    required param: 
        ticker
    optional keyword args:
        
        tspan: '1d', '5d', '3m', '6m', '1y', '2y', '5y', 'my' (max years)
        
        type: 'l' ==> line,
              'b' ==> bar
              'c' ==> candle
              
        scale: 'on' ==> logarithmic
               'off' ==> linear
               
        size: 's', 'm', 'l'
        
        avgs: moving average indicators.
            pass a list of day lengths as strings prepended
            with 'e' for exponential and 'm' for simple.
            eg: avgs=['m5','m20','e5','e20']
            
        """
    def __init__(self, symbol, **kwargs):
        self.symbol = symbol
        self.kwargs = kwargs
        self.url = self._url()

    def open_in_browser(self):
        webbrowser.open_new(self.url)

    def save(self, path):
        urlretrieve(self.url, path)
        self.abspath = os.path.abspath(path)

    def _url(self):
        kwargs = self.kwargs
        symbol = self.symbol
        url = "http://chart.finance.yahoo.com/z?"
        params = urlencode({
            's': symbol,
            't': kwargs.get('tspan','6m'),
            'q': kwargs.get('type', 'l'),
            'l': kwargs.get('scale', 'off'),
            'z': kwargs.get('size', 's'),
            'p': ','.join(kwargs.get('avgs',''))
        })
        url += "%s"%params
        return url


"""
INDUSTRY SECTORS

Name                            page_id

Basic_Materials                 1
Conglomerates                   2
Consumer_Goods                  3
Financial                       4
Healthcare                      5
Industrial_Goods                6
Services                        7
Technology                      8
Utilities                       9

This was thrown together but seems to work.

For company data, sector_data(page_id='ID') works but
the url 'ID' pattern is a mystery.

Reference
http://code.google.com/p/yahoo-finance-managed/wiki/csvCompanyDownload
"""

def _sector_data(page_id='s_', sort_field='coname', sort_direction='u'):
    '''
    Gets raw csv data as a list of the rows.
    Further processing is required to put it in 
    more useful formats.
    '''
    url = 'http://biz.yahoo.com/p/csv/'
    url += '{page_id}{sort_field}{sort_direction}.csv'.format(
        page_id=str(page_id),
        sort_field=sort_field,
        sort_direction=sort_direction
    )    
    response = urlopen(url).read().strip('\x00')
    output = cStringIO.StringIO(response)
    return [row for row in csv.reader(output, dialect='excel')]

def sector_data(page_id='s_', sort_field='coname', sort_direction='u'):
    data = _sector_data(
        page_id=str(page_id), 
        sort_field=sort_field, 
        sort_direction=sort_direction
    )
    idx = data.pop(0)[1::]
    cols = [i.pop(0) for i in data]
    d = {
        cols[i]: {
            idx[j]: data[i][j] for j in range(len(idx))
        } for i in range(len(cols))
    }
    for i in d:
        for j in d[i]: 
            try:
                d[i][j] = float(d[i][j])
            except ValueError:
                pass
    return pd.DataFrame(d).T

def quote_request(symbol, stat):
    url = "http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=%s" %(
        symbol, 
        stat
    )
    req = Request(url)
    response = urlopen(req)
    data = str(response.read().decode('utf-8').strip())
    try:
        return float(data)
    except ValueError:
        return data
