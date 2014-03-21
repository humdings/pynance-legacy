
import pandas as pd

from . settings import CODE_DIR



class CodeDownloader(object):
    '''
    Downloads the Quandl codes for updating local copies.
    
    params:
        drop_inactive: False to keep inactive stocks, default True
        update_all: True to automatically save all codes, default False
    
    '''
    root = 'https://s3.amazonaws.com/quandl-static-content/Ticker+CSV%27s/'
    ext_root = root + 'Stock+Exchanges/'
    yahoo = root + 'Yahoo/'
    google = root + 'Google/'
    
    def __init__(self, update_all=False, drop_inactive=True):
        self.drop_inactive = drop_inactive
        if update_all:
            self.detailed_info().to_csv(
                CODE_DIR + 'stockinfo.csv', index_label='Ticker'
            )
            self.indicies().to_csv(
                CODE_DIR + 'Indicies.csv', index_label='Ticker'
            )
            self.etfs().to_csv(
                CODE_DIR + 'ETFs.csv', index_label='Ticker'
            )
            self.mutual_funds().to_csv(
                CODE_DIR + 'funds.csv', index_label='Ticker'
            )
            self.nasdaq().to_csv(
                CODE_DIR + 'NASDAQ.csv', index_label='Ticker'
            )
            self.nyse().to_csv(
                CODE_DIR + 'NYSE.csv', index_label='Ticker'
            )
            self.nyse_amex().to_csv(
                CODE_DIR + 'AMEX.csv', index_label='Ticker'
            )
            self.pink_sheets().to_csv(
                CODE_DIR + 'PINK.csv', index_label='Ticker'
            )
            self.otc().to_csv(
                CODE_DIR + 'OTC.csv', index_label='Ticker'
            )
            self.fundamentals().to_csv(
                CODE_DIR + 'quandl-stock-code-list.csv', index_label='Ticker'
            )
    
    def detailed_info(self):
        url = self.ext_root + 'stockinfo.csv'
        cols = ['Quandl Code', 'Company Name', 
                'Industry Name', 'Exchange Name', 'SIC Code']
        data = pd.read_csv(
            url, index_col=0, header=None, names=cols, skipinitialspace=True
        )
        if self.drop_inactive:
            data = data.T.to_dict()
            data = {
                sym: data[sym] for sym in data if 
                data[sym]['Exchange Name'] != 'Stock no longer trades'
            }
            data = pd.DataFrame(data).T
        return data
    
    def indicies(self):
        url = self.ext_root + 'Indicies.csv'
        return pd.read_csv(url, index_col='Ticker', skipinitialspace=True)
    
    def etfs(self):
        url = self.root + 'ETFs.csv'
        return pd.read_csv(url, index_col='Ticker', skipinitialspace=True)
    
    def mutual_funds(self):
        url = self.ext_root + 'funds.csv'
        return pd.read_csv(url, index_col='Ticker', skipinitialspace=True)
    
    def nasdaq(self):
        url = self.ext_root + 'NASDAQ.csv'
        codes = pd.read_csv(url, index_col='Ticker', skipinitialspace=True)
        codes.columns = pd.Index([u'Quandl Code', u'Name'], dtype=object)
        return codes
        
    def nyse(self):
        url = self.ext_root + 'NYSE.csv'        
        codes = pd.read_csv(url, index_col='Ticker', skipinitialspace=True)
        codes.columns = pd.Index([u'Quandl Code', u'Name'], dtype=object)
        return codes
    
    def nyse_amex(self):
        url = self.ext_root + 'AMEX.csv'
        codes = pd.read_csv(url, index_col='Ticker', skipinitialspace=True)
        codes.columns = pd.Index([u'Quandl Code', u'Name'], dtype=object)
        return codes
    
    def pink_sheets(self):
        url = self.ext_root + 'PINK.csv'
        codes = pd.read_csv(url, index_col='Ticker', skipinitialspace=True)
        codes.columns = pd.Index([u'Quandl Code', u'Name'], dtype=object)
        return codes
    
    def otc(self):
        url = self.ext_root + 'OTC.csv'
        codes = pd.read_csv(url, index_col='Ticker', skipinitialspace=True)
        codes.columns = pd.Index([u'Quandl Code', u'Name'], dtype=object)
        return codes
    
    def fundamentals(self):
        url = 'https://s3.amazonaws.com/quandl-static-content/quandl-stock-code-list.csv'
        data = pd.read_csv(url, index_col='Ticker', skipinitialspace=True)
        if self.drop_inactive:
            data = data.T.to_dict()
            data = {
                sym: data[sym] for sym in data if 
                data[sym]['In Market?'] == 'Active'
            }
            data = pd.DataFrame(data).T
        return data

