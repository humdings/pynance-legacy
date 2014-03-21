
import Quandl


class Fundamentals(object):
    '''
    Wrapper for the stock fundamentals portion
    of the Quandl API. Initialize with a ticker symbol and
    call .get('some ratio code') with a code or list of codes.
    '''
    
    def __init__(self, symbol):
        self.symbol = symbol
    
    def dataset_code(self, ratios):
        code = 'DMDRN/' + self.symbol
        codes = []
        if type(ratios) == list:
            for r in ratios:
                codes.append(code + '_' + r.upper())
            return codes
        else:
            return code + '_' + ratios.upper()
    
    def get(self, ratios, **kwargs):
        dataset_code = self.dataset_code(ratios)
        return Quandl.get(dataset_code, **kwargs)
        
    def all_stats(self, **kwargs):
        return self.get('ALLFINANCIALRATIOS', **kwargs)

        

        