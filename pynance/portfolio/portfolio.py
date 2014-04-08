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

from .. yahoo_pynance import HistoricalData, Stock

from . risk import Risk


class Portfolio():
    
    '''
    A portfolio over a given time period.
    
    params:
        tickers: (list)list of security ticker symbols
        start_date: (datetime obj/string) starting date 
        end_date: (datetime obj/string) ending date
        interval: (string) data frequency, default is daily
        benchmark: (string) a benchmark for market returns
    '''
    
    def __init__(self, tickers, start_date, end_date, interval='d', benchmark='SPY'):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.benchmark = benchmark
        self.__dict__[benchmark] = HistoricalData(
            benchmark, start_date, end_date, interval=interval
        )
        for sym in self.tickers:
            h =  HistoricalData(sym, start_date, end_date, interval=interval)
            self.__dict__[sym] = h
            time.sleep(.001) # Yahoo has a call rate limit
        
    def __getitem__(self, item):
        return self.__dict__[item]
            
    def _field(self, field):
        return pd.DataFrame({i: self[i][field] for i in self.tickers})
    
    def bm_prices(self, adj_close=True):
        ''' benchmark prices '''
        bm = self[self.benchmark]
        if adj_close:
            return bm['Adj Close']
        return bm.Close
    
    def bm_returns(self, adj_close=True):
        ''' benchmark returns '''
        prices = self.bm_prices(adj_close=adj_close)
        return prices.pct_change().dropna()
        
    @property
    def prices(self):
        return self._field('Adj Close')
        
    @property
    def close_prices(self):
        return self._field('Close')
        
    @property
    def open_prices(self):
        return self._field('Open')
        
    @property
    def highs(self):
        return self._field('High')
        
    @property
    def lows(self):
        return self._field('Low')
        
    @property
    def volumes(self):
        return self._field('Volume')
    
    @property 
    def quotes(self):
        data = [Stock(ticker) for ticker in self.tickers]
        return pd.DataFrame({i.symbol: i.all for i in data})
        
    def returns(self, adj_close=True):
        if adj_close:
            prices = self.prices
        else:
            prices = self.close_prices
        return prices.pct_change().dropna()
       
    def vwaps(self, days=None, adj_close=True):
        ''' Volume weighted average prices '''
        volume = self.volumes
        if adj_close:
            prices = self.prices
        else:
            prices = self.close_prices
        if days is not None:
            prices = prices.tail(days)
            volume = volume.tail(days)
        return (volume * prices).sum() / volume.sum()        
    
    def beta(self, adj_close=True, days=None):
        R = Risk(self.returns(adj_close=adj_close))
        Rm = self.bm_returns(adj_close=adj_close)
        return R.beta(Rm)
    
    def alpha(self, adj_close=True, rfr=.02):
        R = Risk(self.returns(adj_close=adj_close))
        Rm = self.bm_returns(adj_close=adj_close)
        return R.alpha(Rm, rfr)
